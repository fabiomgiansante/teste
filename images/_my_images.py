import os

class Image:
    # Usar caminho relativo ao diretório do arquivo para funcionar em qualquer ambiente
    BASE_DIR = os.path.dirname(__file__)

    LOGO = os.path.join(BASE_DIR, "logo_iep.png")
    POWERED = os.path.join(BASE_DIR, "logo_remederi.png")
