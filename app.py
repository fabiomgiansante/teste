import streamlit as st
import os

# CRÍTICO: Carregar Secrets ANTES de importar qualquer crew
# Isso garante que as variáveis de ambiente estejam disponíveis quando os crews são inicializados

# PRIORIDADE 1: Carregar do Streamlit Secrets (produção) - MAIS IMPORTANTE
try:
    if hasattr(st, 'secrets'):
        # Carregar OPENAI_API_KEY dos secrets
        try:
            api_key = None
            # Tentar diferentes formas de acessar
            if 'OPENAI_API_KEY' in st.secrets:
                api_key = st.secrets['OPENAI_API_KEY']
            elif hasattr(st.secrets, 'get'):
                api_key = st.secrets.get('OPENAI_API_KEY')
            
            if api_key:
                # Limpar apenas quebras de linha, NÃO remover espaços (chave pode ter espaços válidos)
                api_key = str(api_key).strip().replace('\n', '').replace('\r', '')
                # Sempre definir a variável de ambiente
                os.environ['OPENAI_API_KEY'] = api_key
        except Exception as e:
            pass
        
        # Carregar SERPER_API_KEY dos secrets
        try:
            serper_key = None
            if 'SERPER_API_KEY' in st.secrets:
                serper_key = st.secrets['SERPER_API_KEY']
            elif hasattr(st.secrets, 'get'):
                serper_key = st.secrets.get('SERPER_API_KEY')
            
            if serper_key:
                serper_key = str(serper_key).strip().replace('\n', '').replace('\r', '')
                os.environ['SERPER_API_KEY'] = serper_key
        except Exception as e:
            pass
except Exception as e:
    pass

# PRIORIDADE 2: Carregar do .env (desenvolvimento local) - APENAS se não estiver nos secrets
if not os.getenv('OPENAI_API_KEY'):
    try:
        from dotenv import load_dotenv
        load_dotenv(override=False)  # NÃO sobrescrever se já existe
    except:
        pass

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

# Debug: Verificar se a chave foi carregada (após sidebar estar disponível)
if not hasattr(st.session_state, 'api_key_checked'):
    st.session_state.api_key_checked = True
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == "":
        st.sidebar.error("❌ OPENAI_API_KEY não configurada! Configure nos Secrets do Streamlit Cloud.")
    elif len(api_key) < 20:
        st.sidebar.warning("⚠️ OPENAI_API_KEY parece inválida (muito curta).")

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
    