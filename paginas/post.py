
import streamlit as st
from crews.post_crew import CrewPostagem  


def render_post_page():

    # Configuração do Streamlit
    st.title('Sistema de Postagem com CrewAI')

    tema = st.text_input('Digite o tópico para a postagem', )


    # Botão para iniciar o processo
    if st.button('Iniciar Processo'):
        
        #Quanto clicar no botão carrega um loader
        with st.spinner('Executando tarefas do Crew...'):
            crew_postagem = CrewPostagem()
            result = crew_postagem.kickoff(inputs={'topic': tema})
            st.success('Processo concluído!')

        # Exibindo resultados
        st.subheader('Postagem Gerada')
        st.write(result)
