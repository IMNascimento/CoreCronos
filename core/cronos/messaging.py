import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.configs import settings


class WhatsAppMessenger:
    def __init__(self, driver, wait_time=10):
        """
        Inicializa o objeto WhatsAppMessenger com um driver do Selenium e tempo de espera padrão.
        
        :param driver: Instância do webdriver do Selenium
        :param wait_time: Tempo máximo para espera explícita de elementos (em segundos)
        """
        self.driver = driver
        self.wait_time = wait_time
        self.logger = logging.getLogger(self.__class__.__name__)
    
    
    def open_chat(self, contact_name):
        """
        Abre o chat com o contato especificado.

        :param contact_name: Nome do contato conforme exibido na interface do WhatsApp.
        :raises Exception: Se o chat não puder ser aberto.
        """
        try:
            # Limpa a barra de pesquisa
            search_box = self.driver.find_element(By.XPATH, settings.CAIXA_RESEARCH_CONTACT)
            search_box.send_keys(Keys.CONTROL + 'a')
            search_box.send_keys(Keys.DELETE)
            
            # Digita o nome do contato
            search_box.send_keys(contact_name)
            self.logger.info(f"Buscando contato: {contact_name}")
            
            # Aguarda que o resultado da pesquisa apareça
            wait = WebDriverWait(self.driver, self.wait_time)
            #search_result_xpath = settings.FIND_CONTACT.format(contact_name=contact_name)
            search_result_xpath = settings.CONTACT_ROW.format(contact_name=contact_name)
            wait = WebDriverWait(self.driver, self.wait_time)
            chat = wait.until(EC.presence_of_element_located((By.XPATH, search_result_xpath)))
            
            try:
                chat.click()
            except Exception as click_error:
                self.logger.warning(f"Click interceptado: {click_error}. Usando ENTER fallback.")
                # rola até o elemento
                elems = self.driver.find_elements(By.XPATH, search_result_xpath)
                if not elems:
                    raise Exception(f"Contato '{contact_name}' não encontrado; abortando ENTER fallback")
                
                # 4b) só aí mando o ENTER
                self.logger.info("Contato confirmado, usando ENTER para abrir")
                search_box.send_keys(Keys.RETURN)
                
            
            settings.time.sleep(3)
            self.logger.info(f"Chat aberto para: {contact_name}")
        except Exception as e:
            self.logger.error(f"Erro ao abrir chat para {contact_name}: {e}")
            raise

    def open_chat_non_contact(self, phone_number: str):
        """
        Abre a conversa para um número que não está na lista de contatos.

        Este método clica no botão "Nova conversa", preenche o campo com o número
        e confirma para abrir o chat.

        :param phone_number: Número do telefone (com código do país, ex: 5511999998888)
        :raises Exception: Se ocorrer erro ao abrir a conversa.
        """
        try:
            wait = WebDriverWait(self.driver, self.wait_time)
            # Clica no botão "Nova conversa" usando o atributo aria-label (ou outro seletor definido)
            new_chat_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, settings.NEW_CHAT_NEXT_BUTTON))
            )
            new_chat_button.click()
            self.logger.info("Botão 'Nova conversa' clicado.")

            # Aguarda o campo para digitar o número
            phone_input = wait.until(
                EC.presence_of_element_located((By.XPATH, settings.NEW_CHAT_PHONE_INPUT))
            )
            phone_input.send_keys(phone_number)
            self.logger.info(f"Número digitado: {phone_number}")
            settings.time.sleep(2)
            
            # Pressiona ENTER para confirmar o número e iniciar o chat
            phone_input.send_keys(Keys.RETURN)
            self.logger.info("ENTER pressionado para confirmar o número.")
            settings.time.sleep(2)
        except Exception as e:
            self.logger.error(f"Erro ao abrir chat para número não contato: {e}")
            raise

    def send_message(self, message):
        """
        Envia uma mensagem para o chat atualmente aberto.
        
        :param message: Texto da mensagem a ser enviada
        :raises Exception: Se houver erro no envio da mensagem
        """
        try:
            wait = WebDriverWait(self.driver, self.wait_time)
            message_box = wait.until(EC.presence_of_element_located((By.XPATH, settings.MESSAGE_TEXT_BOX)))
            message_box.send_keys(message)
            settings.time.sleep(1)
            message_box.send_keys(Keys.RETURN)
            settings.time.sleep(20)
            self.logger.info("Mensagem enviada com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao enviar mensagem: {e}")
            raise

    def send_document(self, document_path):
        """
        Envia um documento para o chat atualmente aberto.
        
        :param document_path: Caminho completo do documento a ser enviado
        :raises Exception: Se houver erro no envio do documento
        """
        try:
            wait = WebDriverWait(self.driver, self.wait_time)
            
            # Clica no botão de anexar
            attach_button = wait.until(EC.element_to_be_clickable((By.XPATH, settings.ATTACH_BUTTON)))
            attach_button.click()
            self.logger.info("Botão de anexar clicado.")
            
            # Encontra o input para enviar arquivos e envia o caminho do documento
            document_input = wait.until(EC.presence_of_element_located((By.XPATH, settings.DOCUMENT_INPUT)))
            document_input.send_keys(document_path)
            self.logger.info(f"Documento selecionado: {document_path}")
            
            # Aguarda e clica no botão de enviar
            send_button = wait.until(EC.element_to_be_clickable((By.XPATH, settings.SEND_BUTTON)))
            send_button.click()
            self.logger.info("Documento enviado com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao enviar documento: {e}")
            raise

    def send_image(self, document_path):
        """
        Envia uma imagem para o chat atualmente aberto.
        
        :param document_path: Caminho completo da imagem a ser enviado
        :raises Exception: Se houver erro no envio do imagem
        """
        try:
            wait = WebDriverWait(self.driver, self.wait_time)
            
            # Clica no botão de anexar
            attach_button = wait.until(EC.element_to_be_clickable((By.XPATH, settings.ATTACH_BUTTON)))
            attach_button.click()
            self.logger.info("Botão de anexar clicado.")
            
            # Encontra o input para enviar arquivos e envia o caminho da imagem
            document_input = wait.until(EC.presence_of_element_located((By.XPATH, settings.IMAGE_INPUT)))
            document_input.send_keys(document_path)
            self.logger.info(f"Imagem selecionada: {document_path}")
            
            # Aguarda e clica no botão de enviar
            send_button = wait.until(EC.element_to_be_clickable((By.XPATH, settings.SEND_BUTTON)))
            send_button.click()
            self.logger.info("Imagem enviada com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao enviar Imagem: {e}")
            raise

    def send_audio(self, audio_path):
        """
        Envia um áudio para o chat atualmente aberto.
        
        :param audio_path: Caminho completo do arquivo de áudio a ser enviado.
        :raises Exception: Se houver erro no envio do áudio.
        """
        try:
            wait = WebDriverWait(self.driver, self.wait_time)
            # Clica no botão de anexar
            attach_button = wait.until(EC.element_to_be_clickable((By.XPATH, settings.ATTACH_BUTTON)))
            attach_button.click()
            self.logger.info("Botão de anexar clicado para áudio.")
            
            # Encontra o input para enviar áudio (defina settings.AUDIO_INPUT no seu settings)
            audio_input = wait.until(EC.presence_of_element_located((By.XPATH, settings.AUDIO_INPUT)))
            audio_input.send_keys(audio_path)
            self.logger.info(f"Áudio selecionado: {audio_path}")
            
            # Aguarda e clica no botão de enviar
            send_button = wait.until(EC.element_to_be_clickable((By.XPATH, settings.SEND_BUTTON)))
            send_button.click()
            self.logger.info("Áudio enviado com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao enviar áudio: {e}")
            raise

    def exit_chat(self):
        """
        Sai do chat atual, limpando a barra de pesquisa e enviando o comando de escape.
        
        :raises Exception: Se houver erro ao sair do chat
        """
        try:
            search_box = self.driver.find_element(By.XPATH, settings.CAIXA_RESEARCH_CONTACT)
            search_box.send_keys(Keys.CONTROL + 'a')
            search_box.send_keys(Keys.DELETE)
            search_box.send_keys(Keys.ESCAPE)
            self.logger.info("Saída do chat realizada.")
        except Exception as e:
            self.logger.error(f"Erro ao sair do chat: {e}")
            raise
