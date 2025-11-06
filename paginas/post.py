
import streamlit as st
from crews.post_crew import CrewPostagem  


def render_post_page():

    # Configuração do Streamlit
    st.title('Sistema de Postagem com CrewAI')

    tema = st.text_input('Digite o tópico para a postagem', )


    # Botão para iniciar o processo
    if st.button('Iniciar Processo'):
        
        # Validar se a chave da API está disponível
        import os
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            st.error('⚠️ Erro: OPENAI_API_KEY não encontrada! Verifique os Secrets no Streamlit Cloud.')
            return
        
        # Validar formato da chave
        if not api_key.startswith('sk-'):
            st.error(f'⚠️ Erro: OPENAI_API_KEY parece inválida! Deve começar com "sk-". Primeiros caracteres: {api_key[:10]}...')
            st.info('💡 Dica: Verifique se a chave está completa nos Secrets do Streamlit Cloud.')
            return
        
        if len(api_key) < 50:
            st.warning(f'⚠️ Aviso: OPENAI_API_KEY parece muito curta ({len(api_key)} caracteres). Chaves OpenAI normalmente têm 100+ caracteres.')
        
        #Quanto clicar no botão carrega um loader
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner('Executando tarefas do Crew...'):
            try:
                status_text.text('Inicializando crew...')
                progress_bar.progress(10)
                crew_postagem = CrewPostagem()
                
                status_text.text('Executando pesquisa...')
                progress_bar.progress(30)
                result = crew_postagem.kickoff(inputs={'topic': tema})
                
                progress_bar.progress(100)
                status_text.text('Processo concluído!')
                st.success('Processo concluído!')
            except ValueError as e:
                # Erro de validação da API key
                st.error(f'⚠️ Erro de validação: {e}')
                st.info('💡 Verifique se a OPENAI_API_KEY está correta nos Secrets do Streamlit Cloud.')
                return
            except Exception as e:
                error_msg = str(e)
                if '401' in error_msg or 'invalid_api_key' in error_msg or 'Incorrect API key' in error_msg:
                    st.error('❌ Erro: API Key da OpenAI está incorreta ou inválida!')
                    st.info('''
                    **Como corrigir:**
                    1. Acesse: https://platform.openai.com/account/api-keys
                    2. Crie uma nova chave ou copie a chave existente
                    3. No Streamlit Cloud: "Manage app" → "Settings" → "Secrets"
                    4. Cole a chave completa no formato:
                       ```
                       OPENAI_API_KEY = "sk-proj-sua-chave-completa-aqui"
                       ```
                    5. Salve e reinicie o app
                    ''')
                else:
                    st.error(f'Erro ao executar o crew: {e}')
                return

        # Exibindo resultados
        st.subheader('Postagem Gerada')
        st.write(result)
