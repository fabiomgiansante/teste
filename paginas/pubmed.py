import streamlit as st
from crews.pubmed_agent_crew import scrape_pubmed_central


def render_pubmed_page():
    
    # Título da aplicação
    st.title("Pesquisador PubMed")
    
    # Instruções para o usuário
    st.write("Digite o tema e a patologia para buscar estudos científicos no PubMed.")
    
    # Inputs do usuário
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.text_input('Tema principal do estudo', placeholder='Ex: cannabinoides')
    
    with col2:
        pathology = st.text_input('Patologia', placeholder='Ex: demência')
    
    # Botão para iniciar o processo
    if st.button('Buscar Estudos'):
        
        # Validação dos inputs
        if not theme or not pathology:
            st.error('Por favor, preencha ambos os campos: tema e patologia.')
            return
        
        # Loader durante a execução
        with st.spinner('Buscando estudos no PubMed...'):
            try:
                studies = scrape_pubmed_central(theme, pathology)
                st.success('Busca concluída!')
                
                # Exibindo resultados
                if not studies:
                    st.warning('Nenhum estudo foi encontrado para a combinação fornecida.')
                else:
                    st.subheader(f'Resultados da Pesquisa: {theme} e {pathology}')
                    st.write(f'**Total de estudos encontrados:** {len(studies)}')
                    
                    # Exibindo cada estudo
                    for idx, estudo in enumerate(studies, start=1):
                        with st.container():
                            st.markdown(f"### Estudo {idx}")
                            st.write(f"**Título:** {estudo.get('title', 'Título não disponível')}")
                            st.write(f"**Autores:** {estudo.get('authors', 'Autores não disponíveis')}")
                            
                            if estudo.get('np') and estudo.get('np') != "Informação não disponível":
                                st.write(f"**Número de Participantes:** {estudo.get('np')}")
                            
                            if estudo.get('criteria') and estudo.get('criteria') != "Informação não disponível":
                                st.write(f"**Critérios:** {estudo.get('criteria')}")
                            
                            if estudo.get('conclusion') and estudo.get('conclusion') != "Informação não disponível":
                                st.write(f"**Conclusão:** {estudo.get('conclusion')}")
                            
                            if estudo.get('link'):
                                st.markdown(f"[🔗 Acessar artigo completo]({estudo.get('link')})")
                            
                            st.divider()
                
            except Exception as e:
                st.error(f"Erro ao processar a busca: {e}")

