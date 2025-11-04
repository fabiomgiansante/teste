import streamlit as st
from streamlit_option_menu import option_menu
from images._my_images import Image
from paginas.welcome import render_welcome
from paginas.post import render_post_page
from paginas.upload_pdf import render_upload_page
from paginas.upload2_pdf import render_upload_page2

st.sidebar.image(
    Image.LOGO,
    use_container_width=True,
    width=200
)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Agentic Platform",  # Título do menu
        options=["Home", "Post Agent", "Summary PDF", "Pesquisador PDF"],  # Opções do menu
        icons=['house','file-earmark-text','cloud-upload', 'cloud-upload'],
        menu_icon='robot',
        default_index=0,
        orientation="vertical" #teste com "horizontal"
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
    