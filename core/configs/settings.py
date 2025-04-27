from pathlib import Path
from core.configs.tags import *
import os
import time

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

CLOSE_TIMEOUT = 5 * 60  # 5 minutos
METADATA_FILENAME = "_session_metadata.json"
COOKIES_FILENAME = "_whatsapp_cookies.pkl"

# Diretório para armazenar qr-codes para sessões
QR_CODE_DIR = BASE_DIR / "qrcodes"
if not QR_CODE_DIR.exists():
    os.makedirs(QR_CODE_DIR)

# Diretório para armazenar sessões (cookies, metadados, etc.)
COOKIE_DIR = BASE_DIR / "sessions"
if not COOKIE_DIR.exists():
    os.makedirs(COOKIE_DIR)

# Diretório para armazenar arquivos de log
LOG_DIR = BASE_DIR / "logs"
if not LOG_DIR.exists():
    os.makedirs(LOG_DIR)

# Arquivo de log padrão para a aplicação
LOG_FILE = LOG_DIR / "app.log"

# Configuração da VPN
VPN_CONFIG = {
    "use_vpn": False,               # Defina True se deseja habilitar VPN para as sessões
    "vpn_server": "vpn.example.com",  # Exemplo de servidor VPN
    "vpn_username": "vpn_user",         # Nome de usuário da VPN
    "vpn_password": "vpn_password"      # Senha da VPN
}