import argparse
import logging
import time
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from core.cronos.manager import CronosManager


def main():
    """"
    Teste de envio de mensagens via CronosManager. Esse teste simula o envio de mensagens para uma pessoa já existente
    na lista de contatos e para um número que não está na lista de contatos. O teste também verifica o status de login
    da sessão e renderiza o QR Code se necessário.
    O teste é realizado através de argumentos passados via linha de comando, permitindo que o usuário especifique
    o número da sessão, o contato para envio de mensagem, o número de um não contato e o texto da mensagem.
    O teste também permite o envio de imagens, áudios e documentos, embora esses parâmetros sejam opcionais.
    """
    parser = argparse.ArgumentParser(description="Teste de envio de mensagens via CronosManager")
    parser.add_argument("--session-phone", type=str, required=True,
                        help="Número do telefone da sessão (ex: 5511999998888)")
    parser.add_argument("--chat-id", type=str, required=True,
                        help="Nome ou identificador do contato para enviar mensagem")
    parser.add_argument("--non-contact-phone", type=str, required=True,
                        help="Número de telefone de um não contato (ex: 5511888887777)")
    parser.add_argument("--text", type=str, default="Esta é uma mensagem de teste.",
                        help="Texto da mensagem a ser enviada")
    parser.add_argument("--image", type=str,
                        help="Caminho para a imagem (opcional)")
    parser.add_argument("--audio", type=str,
                        help="Caminho para o áudio (opcional)")
    parser.add_argument("--document", type=str,
                        help="Caminho para o documento (opcional)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    manager = CronosManager()

    # Verifica o status de login da sessão e renderiza o QR Code se necessário.
    try:
        session, login_status = manager.get_session(args.session_phone)
        if login_status.get("status") == "qr_required":
            print("Sessão não autenticada. QR Code necessário para login.")
            qr_file = login_status.get("qr_code")
            print(f"QR Code salvo em '{qr_file}'. Faça o scan para autenticar.")
            # Mantém o script rodando para manter a sessão aberta.
            while True:
                # Aqui você pode, por exemplo, atualizar o status a cada 10 segundos
                status = session.update_login_status()
                if status.get("status") == "logged_in":
                    print("Sessão autenticada com sucesso!")
                    break
                else:
                    print("Aguardando autenticação... (QR Code atualizado)")
                time.sleep(10)
        else:
            print("Sessão autenticada com sucesso!")
    except Exception as e:
        print("Erro ao obter sessão:", e)
        return


    # Teste: Envio de mensagem de texto e imagem para um numero não contato.
    logging.info("Teste: Enviando mensagem de texto com imagem para não contatos.")
    result_text = manager.send_complete_message_to_non_contact(args.session_phone, args.non_contact_phone, args.text, args.image)
    print("Envio de mensagem de texto:", "Sucesso" if result_text else "Falhou")
    
    time.sleep(5)


    # Teste: Envio de mensagem de texto e imagem para um contato já existente.
    logging.info("Teste: Enviando mensagem de texto para contato existente com imagem.")
    result_text = manager.send_complete_message(args.session_phone, args.chat_id, args.text, args.image)
    print("Envio de mensagem de texto:", "Sucesso" if result_text else "Falhou")
    
    time.sleep(5)


    # Teste: Envio de mensagem de texto para um numero não contato.
    logging.info("Teste: Enviando mensagem de texto para não contatos.")
    result_text = manager.send_complete_message_to_non_contact(args.session_phone, args.non_contact_phone, args.text)
    print("Envio de mensagem de texto:", "Sucesso" if result_text else "Falhou")
    
    time.sleep(5)


    # Teste: Envio de mensagem de texto  para um contato já existente.
    logging.info("Teste: Enviando mensagem de texto para contato existente.")
    result_text = manager.send_complete_message(args.session_phone, args.chat_id, args.text)
    print("Envio de mensagem de texto:", "Sucesso" if result_text else "Falhou")
    
    time.sleep(5)


   

    # Encerra todas as sessões ativas.
    manager.close_all_sessions()
    logging.info("Teste concluído.")

if __name__ == "__main__":
    main()


#python3 tests/test_messaging.py \
#  --session-phone "5532988967108" \
#  --chat-id "Junior Souza" \
#  --non-contact-phone "5532991463109" \
#  --text "Olá, classe de teste de envio Cronos!" \
#  --image "C:/Users/Igor/Downloads/qr_code-sophia.png" \
#  --audio "/caminho/para/audio.mp3" \
#  --document "/caminho/para/documento.pdf"
