import os
import json
import pickle
from time import sleep
from pathlib import Path
from typing import Any, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from core.configs import settings
from core.utils.logger import log_info, log_error
from pathlib import Path


class WhatsAppSession:
    """
    Gerencia a sessão do WhatsApp Web utilizando Selenium, com suporte a:
      - Salvar e carregar cookies e metadados (incluindo proxy)
      - Aplicar VPN se necessário (simulado)
      - Login e logout do WhatsApp Web
      - Configuração do driver para parecer uma aplicação legítima
      - Alteração de proxy e destruição da sessão
    
    Cada sessão é associada a um identificador (número ou nome) e os dados são salvos
    em um diretório dedicado para esse identificador.
    """
    
    def __init__(self, phone_number: str, use_vpn: bool = False, proxy: Optional[str] = None) -> None:
        """
        Inicializa a sessão do WhatsApp.
        
        :param phone_number: Número ou identificador associado à sessão.
        :param use_vpn: Se True, tenta aplicar VPN (simulado).
        :param proxy: Proxy a ser usado (ex.: "http://user:pass@proxy_server:port"). Se None, sem proxy.
        """
        self.phone_number: str = phone_number
        self.use_vpn: bool = use_vpn
        self.proxy: Optional[str] = proxy
        self.profile_path: Path = Path(settings.COOKIE_DIR) / phone_number
        self.driver: Optional[webdriver.Chrome] = None
        self.metadata: Dict[str, Any] = {}
        self.wait_time: int = 50  # Tempo máximo para espera explícita de elementos (em segundos)
        self._load_metadata()

    def _apply_vpn(self) -> None:
        """
        Aplica configurações de VPN se habilitado.
        Essa implementação é simulada. Em uma implementação real, utilize chamadas a
        bibliotecas ou comandos externos.
        """
        if self.use_vpn and settings.VPN_CONFIG.get("use_vpn"):
            log_info(f"Aplicando VPN para o número {self.phone_number}")
            # Exemplo: subprocess.run(["vpnclient", "connect", settings.VPN_CONFIG["vpn_server"], ...])
            sleep(1)

    def _get_chrome_options(self) -> Options:
        """
        Configura as opções do Chrome para a sessão, incluindo perfil, proxy e ajustes
        para disfarçar a automação.
        
        :return: Instância configurada de Options.
        """
        options = Options()
        options.add_argument(f"--user-data-dir={self.profile_path}")
        options.add_argument("--profile-directory=Default")
        # Configurações para parecer uma aplicação legítima:
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        #options.add_argument("--headless")  # Modo headless: sem interface gráfica para servidores
        options.add_argument('--no-sandbox')  # Esse argumento desativa o sandbox de segurança do Chrome.
        options.add_argument('--disable-dev-shm-usage') #Esse argumento faz com que o Chrome não use o diretório /dev/shm para armazenamento temporário compartilhado.
        #options.add_argument('--disable-gpu') # Esse argumento desativa o uso da GPU para aceleração gráfica.
        options.add_argument('--disable-extensions') # Desativa todas as extensões do navegador.
        options.add_argument('--disable-infobars') # Impede que sejam exibidas infobars (barras de informação) no navegador.
        # Se um proxy estiver definido, adiciona a opção:
        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')
        return options

    def _setup_driver(self) -> None:
        """
        Configura e inicia o driver do Chrome com as opções necessárias.
        """
        self._apply_vpn()
        options = self._get_chrome_options()
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            # Remover a flag de automação
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
            log_info(f"Driver iniciado para o número {self.phone_number}")
        except Exception as e:
            log_error(f"Erro ao iniciar o driver para {self.phone_number}: {e}")
            raise

    def _load_cookies(self) -> None:
        """
        Carrega os cookies salvos de uma sessão anterior, se disponíveis.
        """
        cookies_file = self.profile_path / (self.phone_number + settings.COOKIES_FILENAME)
        if cookies_file.exists() and self.driver:
            try:
                self.driver.delete_all_cookies()
                with open(cookies_file, "rb") as file:
                    cookies = pickle.load(file)
                for cookie in cookies:
                    try:
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        log_error(f"Erro ao adicionar cookie: {e}")
                log_info("Cookies carregados com sucesso.")
            except Exception as e:
                log_error(f"Erro ao carregar cookies: {e}")

    def _save_cookies(self) -> None:
        """
        Salva os cookies atuais da sessão em um arquivo para uso futuro.
        """
        if not self.driver:
            log_error("Driver não inicializado. Não é possível salvar cookies.")
            return
        try:
            cookies = self.driver.get_cookies()
            self.profile_path.mkdir(parents=True, exist_ok=True)
            cookies_file = self.profile_path / (self.phone_number + settings.COOKIES_FILENAME)
            with open(cookies_file, "wb") as file:
                pickle.dump(cookies, file)
            log_info("Cookies salvos para uso futuro.")
        except Exception as e:
            log_error(f"Erro ao salvar cookies: {e}")
            raise

    def _save_metadata(self) -> None:
        """
        Salva os metadados da sessão (por exemplo, proxy e outras configurações) em um arquivo JSON.
        """
        try:
            self.metadata["phone_number"] = self.phone_number
            self.metadata["proxy"] = self.proxy
            self.metadata["use_vpn"] = self.use_vpn
            self.profile_path.mkdir(parents=True, exist_ok=True)
            metadata_file = self.profile_path / (self.phone_number + settings.METADATA_FILENAME)
            with open(metadata_file, "w", encoding="utf-8") as file:
                json.dump(self.metadata, file, indent=4)
            log_info("Metadados salvos com sucesso.")
        except Exception as e:
            log_error(f"Erro ao salvar metadados: {e}")
            raise

    def _load_metadata(self) -> None:
        """
        Carrega os metadados da sessão, se existentes.
        """
        metadata_file = self.profile_path / (self.phone_number + settings.METADATA_FILENAME)
        if metadata_file.exists():
            try:
                with open(metadata_file, "r", encoding="utf-8") as file:
                    self.metadata = json.load(file)
                # Atualiza parâmetros da instância a partir dos metadados
                self.proxy = self.metadata.get("proxy", self.proxy)
                self.use_vpn = self.metadata.get("use_vpn", self.use_vpn)
                log_info("Metadados carregados com sucesso.")
            except Exception as e:
                log_error(f"Erro ao carregar metadados: {e}")


    def ensure_logged_in(self) -> dict:
        """
        Garante que a sessão do WhatsApp esteja autenticada.

        Caso existam cookies/metadados salvos e a sessão esteja ativa, utiliza-os para evitar um novo login.
        Se a página apresentar o QR Code para login manual, captura o QR Code e retorna imediatamente
        para o usuário, mantendo a sessão aberta.

        :return: Dicionário com o status da sessão.
                Exemplo: {"status": "logged_in"} ou {"status": "qr_required", "qr_code": "<base64>"}
        :raises Exception: Se ocorrer um erro crítico na autenticação.
        """
        self._setup_driver()
        self.driver.get("https://web.whatsapp.com/")
        
        # Se existirem cookies salvos, carrega-os e atualiza a página.
        cookies_file = self.profile_path / (self.phone_number + settings.COOKIES_FILENAME)
        if cookies_file.exists():
            self._load_cookies()
            self.driver.refresh()
        
        try:
            # Aguarda até 10 segundos para que apareça OU o painel autenticado OU o QR Code.
            WebDriverWait(self.driver, self.wait_time).until(
                lambda d: d.find_elements(By.XPATH, settings.LOGGED_IN) or d.find_elements(By.XPATH, settings.QR_CODE)
            )
            # Agora, verifica qual elemento foi encontrado.
            if self.driver.find_elements(By.XPATH, settings.LOGGED_IN):
                log_info("Sessão já autenticada. Utilizando cookies/metadados salvos.", name="WhatsAppSession")
                self._save_cookies()
                self._save_metadata()
                return {"status": "logged_in"}
            elif self.driver.find_elements(By.XPATH, settings.QR_CODE):
                log_info("Login page detectada (QR Code exibido).", name="WhatsAppSession")
                # Captura o QR Code imediatamente e retorna o caminho do arquivo.
                qr_file = self.capture_qr_code_to_file(self.phone_number + "_qr_code.png")
                return {"status": "qr_required", "qr_code": qr_file}
            else:
                raise Exception("Nenhum elemento esperado foi encontrado.")
        except Exception as e:
            log_error(f"Erro ao verificar status de login: {e}", name="WhatsAppSession")
            raise
        
    
    def update_login_status(self) -> dict:
        """
        Verifica se a sessão já foi autenticada, atualizando o QR Code se necessário.
        Se a sessão não estiver autenticada, captura o QR Code novamente.

        :return: Dicionário com o status atualizado.
                Exemplo: {"status": "logged_in"} ou {"status": "qr_required", "qr_code": "<base64>"}
        """
        try:
            # Tenta aguardar por um curto intervalo (por exemplo, 5 segundos)
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, settings.LOGGED_IN))
            )
            log_info("Login efetuado com sucesso.", name="WhatsAppSession")
            self._save_cookies()
            self._save_metadata()
            return {"status": "logged_in"}
        except Exception:
            try:
                qr_code = self.capture_qr_code_to_file(self.phone_number + "_qr_code.png")  # Captura nova versão do QR Code
            except Exception as e:
                log_error(f"Erro ao atualizar QR Code: {e}", name="WhatsAppSession")
                return {"status": "error", "error": str(e)}
            return {"status": "qr_required", "qr_code": qr_code}


    def logout(self) -> None:
        """
        Realiza o logout do WhatsApp Web.
        
        Exclui os cookies atuais (para forçar um novo login na próxima vez) e fecha o driver.
        """
        if not self.driver:
            log_error("Driver não inicializado, não é possível realizar logout.")
            return
        try:
            self.driver.delete_all_cookies()
            log_info("Cookies removidos; logout efetuado.")
        except Exception as e:
            log_error(f"Erro ao remover cookies para logout: {e}")
        finally:
            self.close()

    def change_proxy(self, new_proxy: str) -> None:
        """
        Altera o proxy utilizado na sessão.
        
        Encerra o driver atual, atualiza os metadados com o novo proxy, e reinicializa o driver.
        
        :param new_proxy: Novo proxy a ser utilizado (ex.: "http://user:pass@proxy_server:port").
        """
        log_info(f"Alterando proxy para {new_proxy}")
        self.proxy = new_proxy
        self._save_metadata()
        self.close()
        self._setup_driver()
        # Após reinicialização, recarrega cookies para preservar a sessão, se possível.
        self.driver.get("https://web.whatsapp.com/")
        sleep(5)
        self._load_cookies()
        self.driver.refresh()

    def destroy_session(self) -> None:
        """
        Destrói a sessão atual.
        
        Encerra o driver e remove todo o diretório da sessão (cookies, metadados, etc.).
        Cuidado: essa operação é irreversível.
        """
        self.close()
        try:
            if self.profile_path.exists():
                for item in self.profile_path.iterdir():
                    item.unlink()
                self.profile_path.rmdir()
                log_info(f"Dados da sessão '{self.phone_number}' removidos com sucesso.")
        except Exception as e:
            log_error(f"Erro ao destruir a sessão '{self.phone_number}': {e}")

    def close(self) -> None:
        """
        Encerra a sessão do driver.
        """
        if self.driver:
            try:
                self.driver.quit()
                log_info(f"Driver encerrado para o número {self.phone_number}")
            except Exception as e:
                log_error(f"Erro ao encerrar o driver para {self.phone_number}: {e}")
            finally:
                self.driver = None


    def capture_qr_code_to_file(self, filename: str = "qr_code.png") -> str:
        """
        Captura o QR Code exibido na página de login do WhatsApp (elemento canvas)
        e salva a imagem em um arquivo PNG na pasta definida.
        
        :param filename: Nome do arquivo onde a imagem será salva.
        :return: Caminho absoluto do arquivo salvo.
        :raises Exception: Se não for possível localizar ou capturar o QR Code.
        """
        try:
            # Define a pasta onde os QR Codes serão salvos.
            qr_folder = Path(settings.QR_CODE_DIR) if hasattr(settings, "QR_CODE_DIR") else Path("qrcodes")
            qr_folder.mkdir(parents=True, exist_ok=True)
            
            # Gera o caminho completo para o arquivo
            file_path = qr_folder / filename

            # Usa a condição de visibilidade para garantir que o canvas esteja renderizado.
            canvas = self.driver.find_element(By.XPATH, settings.QR_CODE)
            png_data = canvas.screenshot_as_png
            with open(file_path, "wb") as f:
                f.write(png_data)
            log_info(f"QR Code salvo em '{file_path}'.", name="WhatsAppSession")
            return str(file_path)
        except Exception as e:
            log_error(f"Erro ao capturar QR Code: {e}", name="WhatsAppSession")
            raise