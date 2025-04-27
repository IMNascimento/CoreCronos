from core.cronos.session import WhatsAppSession
from core.cronos.messaging import WhatsAppMessenger
from core.utils.logger import log_info, log_error
from core.configs.settings import CLOSE_TIMEOUT
import threading
import time

class CronosManager:
    """
    Gerencia as sessões do WhatsApp e abstrai as operações de envio de mensagens.
    
    Permite gerenciar múltiplas sessões, cada uma associada a um número de telefone,
    além de facilitar o envio de mensagens e o encerramento de sessões.
    """
    
    def __init__(self):
        """
        Inicializa o CronosManager com um dicionário vazio de sessões.
        """
        self.sessions: dict[str, WhatsAppSession] = {}
        self._timers: dict[str, threading.Timer] = {}


    def _schedule_close(self, phone: str):
        """Agenda o fechamento da sessão se ela ainda estiver pendente."""
        def _close_if_pending():
            sess = self.sessions.get(phone)
            if sess:
                log_info(f"Fechando sessão {phone} por timeout de login.", name="CronosManager")
                sess.close()
                self.sessions.pop(phone, None)
                self._timers.pop(phone, None)

        # cancela timer anterior (se existir)
        if phone in self._timers:
            self._timers[phone].cancel()

        t = threading.Timer(CLOSE_TIMEOUT, _close_if_pending)
        t.daemon = True
        t.start()
        self._timers[phone] = t

    def get_session(self, phone_number: str, use_vpn: bool = False) -> tuple[WhatsAppSession, dict]:
        """
        Recupera ou cria uma sessão do WhatsApp para o número fornecido.
        
        Se a sessão para o número ainda não existir, uma nova sessão será criada e
        o método ensure_logged_in() será chamado. Esse método retorna um dicionário
        com o status do login, que pode indicar que o QR Code precisa ser renderizado.
        
        :param phone_number: Número do telefone associado à sessão.
        :param use_vpn: Indica se a VPN deve ser aplicada para esta sessão.
        :return: Tupla com a instância de WhatsAppSession e um dicionário de status do login.
                 Exemplo: (session, {"status": "logged_in"}) ou (session, {"status": "qr_required", "qr_code": "<base64>"})
        :raises Exception: Caso ocorra erro na criação ou autenticação da sessão.
        """
        if phone_number not in self.sessions:
            log_info(f"Criando nova sessão para {phone_number}", name="CronosManager")
            session = WhatsAppSession(phone_number, use_vpn=use_vpn)
            status = session.ensure_logged_in()  # {'status': 'qr_required', 'qr_code': '<path>'} ou {'status':'logged_in'}
            self.sessions[phone_number] = session

            if status.get("status") == "qr_required":
                # agendar fechamento automático
                self._schedule_close(phone_number)
            else:
                # se já logado, não precisa de timer
                if phone_number in self._timers:
                    self._timers.pop(phone_number).cancel()
            return session, status

        else:
            session = self.sessions[phone_number]
            status = session.update_login_status()
            if status.get("status") == "logged_in":
                # login concluído, cancelar eventual timer
                if phone_number in self._timers:
                    self._timers.pop(phone_number).cancel()
            else:
                # reenfileirar timeout, caso ainda esteja pendente
                self._schedule_close(phone_number)
            return session, status


    def send_complete_message_to_non_contact(self, session_phone_number: str, target_phone_number: str, text_message: str = "", 
                                            image_path: str = None, audio_path: str = None, document_path: str = None,
                                            use_vpn: bool = False) -> bool:
        """
        Envia uma mensagem completa para um número que não está na lista de contatos,
        podendo incluir texto, imagem, áudio e/ou documento.

        Esse método recupera a sessão associada ao número (da sessão que vai enviar a mensagem),
        abre o chat para o número não contato, envia os anexos e/ou a mensagem de texto, e encerra o chat.

        :param session_phone_number: Número do telefone da sessão que será utilizada.
        :param target_phone_number: Número de telefone de destino (não contato, ex: 5511999998888).
        :param text_message: Mensagem de texto a ser enviada.
        :param image_path: Caminho para imagem (opcional).
        :param audio_path: Caminho para áudio (opcional).
        :param document_path: Caminho para documento (opcional).
        :param use_vpn: Indica se a VPN deve ser utilizada para essa sessão.
        :return: True se a mensagem completa foi enviada com sucesso; False caso contrário.
        """
        try:
            session, login_status = self.get_session(session_phone_number, use_vpn=use_vpn)
            if login_status.get("status") != "logged_in":
                log_error("Sessão não autenticada; não é possível enviar mensagem completa.", name="CronosManager")
                return False
            messenger = WhatsAppMessenger(session.driver)
            time.sleep(5)
            
            # Abre o chat para o número não contato.
            # Aqui você pode chamar um método específico, por exemplo: open_chat_non_contact(target_phone_number)
            # Se esse método não existir, você pode usar send_message_to_non_contact para abrir o chat sem enviar mensagem.
            messenger.open_chat_non_contact(target_phone_number)
            time.sleep(5)
            
            if image_path:
                messenger.send_image(image_path)
                time.sleep(5)
            if text_message:
                messenger.send_message(text_message)
                time.sleep(5)
            if audio_path:
                messenger.send_audio(audio_path)
                time.sleep(5)
            if document_path:
                messenger.send_document(document_path)
                time.sleep(5)
            
            messenger.exit_chat()
            log_info(f"Mensagem completa enviada para o número não contato {target_phone_number} usando o número {session_phone_number}", name="CronosManager")
            return True
        except Exception as e:
            log_error(f"Erro ao enviar mensagem completa para o número não contato {target_phone_number} usando {session_phone_number}: {e}", name="CronosManager")
            return False
        

    def send_complete_message(self, phone_number: str, chat_id: str, text_message: str = "", 
                              image_path: str = None, audio_path: str = None, document_path: str = None,
                              use_vpn: bool = False) -> bool:
        """
        Envia uma mensagem completa que pode incluir texto, imagem, áudio e/ou documento.
        
        :param phone_number: Número do telefone da sessão que será utilizada.
        :param chat_id: Identificador ou nome do contato para envio.
        :param text_message: Mensagem de texto a ser enviada.
        :param image_path: Caminho para imagem (opcional).
        :param audio_path: Caminho para áudio (opcional).
        :param document_path: Caminho para documento (opcional).
        :param use_vpn: Indica se a VPN deve ser utilizada para esta sessão.
        :return: True se a mensagem completa foi enviada com sucesso; False caso contrário.
        """
        try:
            session, login_status = self.get_session(phone_number, use_vpn=use_vpn)
            if login_status.get("status") != "logged_in":
                log_error("Sessão não autenticada; não é possível enviar mensagem completa.", name="CronosManager")
                return False
            messenger = WhatsAppMessenger(session.driver)
            time.sleep(5)
            messenger.open_chat(chat_id)
            
            if image_path:
                messenger.send_image(image_path)
                time.sleep(5)
            if text_message:
                messenger.send_message(text_message)
                time.sleep(5)
            if audio_path:
                messenger.send_audio(audio_path)
                time.sleep(5)
            if document_path:
                messenger.send_document(document_path)
                time.sleep(5)
                
            messenger.exit_chat()
            log_info(f"Mensagem completa enviada para {chat_id} usando o número {phone_number}", name="CronosManager")
            return True
        except Exception as e:
            log_error(f"Erro ao enviar mensagem completa para {chat_id} usando {phone_number}: {e}", name="CronosManager")
            return False

    def close_all_sessions(self):
        """
        Encerra todas as sessões ativas e limpa o dicionário de sessões.
        
        Para cada sessão, tenta encerrar o driver de forma segura e registra o sucesso
        ou eventuais erros ocorridos durante o encerramento.
        """
        for phone, session in self.sessions.items():
            try:
                session.close()
                log_info(f"Encerrada sessão para o número {phone}", name="CronosManager")
            except Exception as e:
                log_error(f"Erro ao encerrar sessão para {phone}: {e}", name="CronosManager")
        self.sessions.clear()
        log_info("Todas as sessões foram encerradas.", name="CronosManager")

    def close_session(self, phone_number: str):
        """Método público para encerrar manualmente a sessão."""
        sess = self.sessions.pop(phone_number, None)
        timer = self._timers.pop(phone_number, None)
        if timer:
            timer.cancel()
        if sess:
            sess.close()
            log_info(f"Sessão {phone_number} fechada manualmente.", name="CronosManager")
