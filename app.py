import logging
import os

import streamlit as st
from streamlit_option_menu import option_menu

from core.env import bootstrap_environment
from images._my_images import Image
from menu.page_registry import list_page_icons, list_page_titles, load_page_renderer


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def _load_runtime_environment() -> None:
    try:
        bootstrap_environment(getattr(st, "secrets", None))
    except Exception as exc:
        LOGGER.exception("Falha ao carregar variaveis de ambiente: %s", exc)


def _show_api_key_status_once() -> None:
    if st.session_state.get("api_key_checked"):
        return

    st.session_state["api_key_checked"] = True
    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()

    if not api_key:
        st.sidebar.error("OPENAI_API_KEY nao configurada. Ajuste nos Secrets do Streamlit.")
    elif len(api_key) < 50:
        st.sidebar.warning("OPENAI_API_KEY parece curta. Verifique se a chave esta completa.")


def _render_page(selected_page: str) -> None:
    try:
        render_function = load_page_renderer(selected_page)
        render_function()
    except Exception as exc:
        LOGGER.exception("Erro ao renderizar pagina %s: %s", selected_page, exc)
        st.error(f"Falha ao abrir a pagina '{selected_page}'.")
        st.exception(exc)


def main() -> None:
    st.set_page_config(
        page_title="Agentic Platform",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    _load_runtime_environment()

    with st.sidebar:
        st.image(Image.LOGO, use_container_width=True)

        selected = option_menu(
            menu_title="Agentic Platform",
            options=list_page_titles(),
            icons=list_page_icons(),
            menu_icon="robot",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#4CAF50", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",
                    "--hover-color": "#66BB6A",
                },
                "nav-link-selected": {
                    "background-color": "#4CAF50",
                    "color": "white",
                },
            },
        )

        st.image(Image.POWERED, use_container_width=True)

    _show_api_key_status_once()
    _render_page(selected)


if __name__ == "__main__":
    main()
