import streamlit as st

from core.execution_guard import SessionExecutionGuard


@st.cache_data(ttl=1800, show_spinner=False)
def _search_pubmed(theme: str, pathology: str, max_results: int):
    from crews.pubmed_agent_crew import scrape_pubmed_central

    return scrape_pubmed_central(theme=theme, pathology=pathology, max_results=max_results)


def render_pubmed_page():
    st.title("Pesquisador PubMed")
    st.write("Digite tema e patologia para buscar estudos cientificos no PubMed.")
    guard = SessionExecutionGuard("pubmed_search")

    col1, col2 = st.columns(2)

    with col1:
        theme = st.text_input("Tema principal do estudo", placeholder="Ex: cannabinoides")

    with col2:
        pathology = st.text_input("Patologia", placeholder="Ex: demencia")

    max_results = st.slider("Quantidade maxima de estudos", min_value=3, max_value=20, value=8)

    if guard.is_running():
        st.info("Ha uma busca em andamento. Aguarde a finalizacao.")

    if st.button("Buscar Estudos", disabled=guard.is_running()):
        normalized_theme = (theme or "").strip()
        normalized_pathology = (pathology or "").strip()

        if not normalized_theme or not normalized_pathology:
            st.error("Preencha ambos os campos: tema e patologia.")
            return

        try:
            with guard.running():
                with st.spinner("Buscando estudos no PubMed..."):
                    studies = _search_pubmed(normalized_theme, normalized_pathology, max_results)
                    st.success("Busca concluida.")

                    if not studies:
                        st.warning("Nenhum estudo encontrado para os filtros informados.")
                        return

                    st.subheader(f"Resultados: {normalized_theme} + {normalized_pathology}")
                    st.write(f"**Total de estudos exibidos:** {len(studies)}")

                    for idx, estudo in enumerate(studies, start=1):
                        with st.container():
                            st.markdown(f"### Estudo {idx}")
                            st.write(f"**Titulo:** {estudo.get('title', 'Nao disponivel')}")
                            st.write(f"**Autores:** {estudo.get('authors', 'Nao disponivel')}")

                            conclusion = estudo.get("conclusion")
                            if conclusion and conclusion != "Informacao nao disponivel":
                                st.write(f"**Conclusao:** {conclusion}")

                            if estudo.get("link"):
                                st.markdown(f"[Acessar artigo completo]({estudo['link']})")

                            st.divider()
        except Exception as exc:
            st.error(f"Erro ao processar a busca: {exc}")
