import streamlit as st
import os

# CRÍTICO: Carregar Secrets ANTES de importar qualquer crew
# Isso garante que as variáveis de ambiente estejam disponíveis quando os crews são inicializados

# Carregar variáveis de ambiente do Streamlit Secrets (produção) ou .env (local)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Se estiver no Streamlit Cloud, usar secrets
try:
    if hasattr(st, 'secrets'):
        # Carregar OPENAI_API_KEY
        if 'OPENAI_API_KEY' in st.secrets:
            os.environ['OPENAI_API_KEY'] = str(st.secrets['OPENAI_API_KEY'])
        # Carregar SERPER_API_KEY
        if 'SERPER_API_KEY' in st.secrets:
            os.environ['SERPER_API_KEY'] = str(st.secrets['SERPER_API_KEY'])
except Exception as e:
    # Se houver erro ao ler secrets, tentar usar variáveis de ambiente
    st.error(f"Erro ao carregar Secrets: {e}")
    pass

# Verificar se as chaves foram carregadas (para debug)
if not os.getenv('OPENAI_API_KEY'):
    st.warning("⚠️ OPENAI_API_KEY não encontrada! Verifique os Secrets no Streamlit Cloud.")

from streamlit_option_menu import option_menu
from images._my_images import Image
from paginas.welcome import render_welcome
from paginas.post import render_post_page
from paginas.upload_pdf import render_upload_page
from paginas.upload2_pdf import render_upload_page2
from paginas.pubmed import render_pubmed_page

# CSS customizado para alterar a cor do menu de vermelho para verde médio-escuro
# Usando CSS e JavaScript para garantir que funcione
st.markdown("""
<style>
    /* Cor verde médio (#4CAF50) para substituir vermelho (#FF4B4B) */
    
    /* Seletores genéricos para qualquer elemento no sidebar */
    div[data-testid="stSidebar"] a[class*="active"],
    div[data-testid="stSidebar"] button[class*="active"],
    div[data-testid="stSidebar"] [class*="active"],
    div[data-testid="stSidebar"] [aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    
    /* Override para elementos com estilo inline vermelho */
    div[data-testid="stSidebar"] a[style*="rgb(255, 75, 75)"],
    div[data-testid="stSidebar"] a[style*="rgb(255,75,75)"],
    div[data-testid="stSidebar"] a[style*="#FF4B4B"],
    div[data-testid="stSidebar"] button[style*="rgb(255, 75, 75)"],
    div[data-testid="stSidebar"] button[style*="#FF4B4B"] {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    
    /* Cor de hover */
    div[data-testid="stSidebar"] a:hover,
    div[data-testid="stSidebar"] button:hover {
        background-color: #66BB6A !important;
    }
</style>

<script>
    // JavaScript para forçar a mudança de cor após o carregamento
    function changeMenuColor() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            // Procurar todos os elementos com cor vermelha e substituir
            const allElements = sidebar.querySelectorAll('a, button, div');
            allElements.forEach(el => {
                const style = window.getComputedStyle(el);
                const bgColor = style.backgroundColor;
                // Verificar se é vermelho (rgb(255, 75, 75) ou similar)
                if (bgColor.includes('255, 75') || bgColor.includes('255,75') || 
                    bgColor === 'rgb(255, 75, 75)' || bgColor === 'rgb(255,75,75)') {
                    el.style.backgroundColor = '#4CAF50';
                    el.style.color = 'white';
                }
                // Verificar estilo inline
                if (el.getAttribute('style') && el.getAttribute('style').includes('255, 75')) {
                    el.style.backgroundColor = '#4CAF50';
                    el.style.color = 'white';
                }
            });
        }
    }
    
    // Executar quando a página carregar
    window.addEventListener('load', changeMenuColor);
    // Executar após um pequeno delay para garantir que o Streamlit renderizou
    setTimeout(changeMenuColor, 500);
    setTimeout(changeMenuColor, 1000);
    setTimeout(changeMenuColor, 2000);
    
    // Observar mudanças no DOM
    const observer = new MutationObserver(changeMenuColor);
    if (document.body) {
        observer.observe(document.body, { childList: true, subtree: true });
    }
</script>
""", unsafe_allow_html=True)

st.sidebar.image(
    Image.LOGO,
    use_container_width=True,
    width=200
)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Agentic Platform",  # Título do menu
        options=["Home", "Post Agent", "Summary PDF", "Pesquisador PDF", "PubMed Agent"],  # Opções do menu
        icons=['house','file-earmark-text','cloud-upload', 'cloud-upload', 'search'],
        menu_icon='robot',
        default_index=0,
        orientation="vertical",  # teste com "horizontal"
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
        }
    )

st.sidebar.image(
    Image.POWERED, 
    use_container_width=True,
    width=200
)


# Conteúdo baseado na opção selecionada
if selected == "Home":
    render_welcome()

elif selected == "Post Agent":
    render_post_page()

elif selected == "Summary PDF":
    render_upload_page()

elif selected == "Pesquisador PDF":
    render_upload_page2()

elif selected == "PubMed Agent":
    render_pubmed_page()
    