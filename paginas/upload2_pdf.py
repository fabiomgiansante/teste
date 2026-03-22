from pathlib import Path

import streamlit as st

from core.env import build_temp_upload_path, ensure_openai_api_key
from core.execution_guard import SessionExecutionGuard
from services.crew_factory import create_crew


TEMP_DIR = Path("temp")


def render_upload_page2():
    st.title("Pesquisador de PDF")
    st.write("Faca upload de um arquivo PDF para analisar o artigo.")
    guard = SessionExecutionGuard("pdf_research")

    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf", key="research_pdf_uploader")

    if uploaded_file is None:
        return

    if guard.is_running():
        st.info("Ha uma execucao em andamento. Aguarde a finalizacao.")
        return

    temp_file_path = None

    try:
        ensure_openai_api_key()

        temp_file_path = build_temp_upload_path(TEMP_DIR, uploaded_file.name)
        temp_file_path.write_bytes(uploaded_file.getbuffer())

        st.success(f"Upload realizado com sucesso: {uploaded_file.name}")
        st.info("Analisando PDF com agentes...")

        progress_bar = st.progress(0)
        status_text = st.empty()

        with guard.running():
            with st.spinner("Executando tarefas do Crew..."):
                status_text.text("Inicializando crew...")
                progress_bar.progress(15)
                crew = create_crew("pdf_research", pdf_path=str(temp_file_path))

                status_text.text("Extraindo dados do PDF...")
                progress_bar.progress(45)
                resultado = crew.kickoff()

                progress_bar.progress(100)
                status_text.text("Analise concluida.")

        st.text_area("Pesquisador via agentes:", resultado, height=350)

    except ValueError as exc:
        st.error(f"Erro de validacao: {exc}")
        st.info("Verifique OPENAI_API_KEY nos Secrets do Streamlit Cloud.")
    except Exception as exc:
        st.error(f"Erro ao processar o arquivo: {exc}")
    finally:
        if temp_file_path and temp_file_path.exists():
            temp_file_path.unlink(missing_ok=True)
