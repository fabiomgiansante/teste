
import os
import time  # Adicionado para simular um tempo de processamento
import streamlit as st
from crews.pesquisador_crew import CrewPDFResumo

# Configuração do diretório temporário
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


def render_upload_page2():

    # Título da aplicação
    st.title("Pesquisador de PDF")

    # Instruções para o usuário
    st.write("Faça upload de um arquivo PDF para resumir seu conteúdo.")

    # Elemento de upload de arquivo
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

    if uploaded_file is not None:
        try:
            # Salvando o arquivo no diretório temporário
            temp_file_path = os.path.join(TEMP_DIR, uploaded_file.name)
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"Upload Realizado com sucesso: {uploaded_file.name}")

            st.info("Pesquisador PDF com agentes")
            
            # Validar se a chave da API está disponível
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
            
            # Loader durante a execução da tarefa
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            with st.spinner('Executando tarefas do Crew...'):
                try:
                    status_text.text('Inicializando crew...')
                    progress_bar.progress(10)
                    crew = CrewPDFResumo(temp_file_path)
                    
                    status_text.text('Analisando PDF e gerando template...')
                    progress_bar.progress(30)
                    resultado = crew.kickoff()
                    
                    progress_bar.progress(100)
                    status_text.text('Análise concluída!')
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

            st.text_area("pesquisador via agentes:", resultado, height=300)

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")


