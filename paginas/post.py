import streamlit as st

from core.env import ensure_openai_api_key
from core.execution_guard import SessionExecutionGuard
from services.crew_factory import create_crew


def render_post_page():
    st.title("Sistema de Postagem com CrewAI")

    tema = st.text_input("Digite o topico para a postagem")
    guard = SessionExecutionGuard("post_agent")

    if guard.is_running():
        st.info("Ha uma execucao em andamento. Aguarde a finalizacao.")

    if st.button("Iniciar Processo", disabled=guard.is_running()):
        topic = (tema or "").strip()
        if not topic:
            st.error("Digite um topico antes de iniciar o processo.")
            return

        try:
            ensure_openai_api_key()
        except ValueError as exc:
            st.error(f"Erro de configuracao da OPENAI_API_KEY: {exc}")
            st.info("Ajuste a chave nos Secrets do Streamlit Cloud e reinicie o app.")
            return

        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            with guard.running():
                with st.spinner("Executando tarefas do Crew..."):
                    status_text.text("Inicializando crew...")
                    progress_bar.progress(15)
                    crew_postagem = create_crew("post_agent")

                    status_text.text("Executando pesquisa e redacao...")
                    progress_bar.progress(45)
                    result = crew_postagem.kickoff(inputs={"topic": topic})

                    progress_bar.progress(100)
                    status_text.text("Processo concluido.")
                    st.success("Processo concluido.")
        except Exception as exc:
            st.error(f"Erro ao executar o crew: {exc}")
            return

        st.subheader("Postagem Gerada")
        st.write(result)
