
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
        if not os.getenv('OPENAI_API_KEY'):
            st.error('⚠️ Erro: OPENAI_API_KEY não encontrada! Verifique os Secrets no Streamlit Cloud.')
            return
        
        #Quanto clicar no botão carrega um loader
        with st.spinner('Executando tarefas do Crew...'):
            try:
                crew_postagem = CrewPostagem()
                result = crew_postagem.kickoff(inputs={'topic': tema})
                st.success('Processo concluído!')
            except Exception as e:
                st.error(f'Erro ao executar o crew: {e}')
                return

        # Exibindo resultados
        st.subheader('Postagem Gerada')
        st.write(result)
