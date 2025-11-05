import os

class Image:
    # Corrigindo os caminhos para usar o caminho absoluto do diretório atual
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    LOGO = os.path.join(BASE_DIR, "agentic_platform", "images", "logo_iep.png")
    POWERED = os.path.join(BASE_DIR, "agentic_platform", "images", "logo_remederi.png")
