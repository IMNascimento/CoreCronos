import argparse
import random
import time
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from core.cronos.manager import CronosManager
from core.utils.logger import log_info, log_error

def main() -> None:
    """
    Script para simular uma conversa entre dois participantes com suporte ao envio de mensagens com imagem.

    Funcionamento:
      1. Inicia as sessões para dois números usando o CronosManager.
      2. Cada participante envia mensagens alternadas para o contato do outro.
      3. Pode enviar texto e/ou imagem.
      4. Entre cada envio, espera um tempo aleatório para simular resposta.
      5. Encerra as sessões ao final.
    """

    parser = argparse.ArgumentParser(description="Simula conversa com envio de mensagens (texto + imagem).")
    parser.add_argument("--phone1", required=True, help="Número da sessão do primeiro participante")
    parser.add_argument("--chat1", required=True, help="Contato para o primeiro participante enviar mensagens")
    parser.add_argument("--phone2", required=True, help="Número da sessão do segundo participante")
    parser.add_argument("--chat2", required=True, help="Contato para o segundo participante enviar mensagens")
    parser.add_argument("--iterations", type=int, default=5, help="Número de trocas de mensagens")
    parser.add_argument("--image", type=str, help="Caminho da imagem a ser enviada (opcional)")
    parser.add_argument("--vpn", action="store_true", help="Habilitar VPN nas sessões")
    args = parser.parse_args()

    cronos1 = CronosManager()
    cronos2 = CronosManager()

    # Inicia sessões
    cronos1.get_session(args.phone1, use_vpn=args.vpn)
    cronos2.get_session(args.phone2, use_vpn=args.vpn)

    messages_phone1 = [
        "Olá, tudo certo?",
        "Você recebeu a imagem?",
        "O que achou?",
        "Legal né?",
        "Até a próxima!"
    ]
    messages_phone2 = [
        "Tudo sim! E aí?",
        "Sim, recebi sim.",
        "Achei muito boa!",
        "Gostei bastante!",
        "Valeu, até mais!"
    ]

    for i in range(args.iterations):
        # Participante 1 envia
        msg1 = messages_phone1[i % len(messages_phone1)]
        log_info(f"[{args.phone1}] Enviando para {args.chat1}: {msg1}", name="SimConversa")
        success = cronos1.send_complete_message(args.phone1, args.chat1, msg1, image_path=args.image)
        if not success:
            log_error(f"[{args.phone1}] Falha ao enviar mensagem", name="SimConversa")

        time.sleep(random.randint(1, 5))

        # Participante 2 responde
        msg2 = messages_phone2[i % len(messages_phone2)]
        log_info(f"[{args.phone2}] Enviando para {args.chat2}: {msg2}", name="SimConversa")
        success = cronos2.send_complete_message(args.phone2, args.chat2, msg2, image_path=args.image)
        if not success:
            log_error(f"[{args.phone2}] Falha ao enviar mensagem", name="SimConversa")

        time.sleep(random.randint(1, 5))

    cronos1.close_all_sessions()
    cronos2.close_all_sessions()
    log_info("Simulação de conversa encerrada.", name="SimConversa")

if __name__ == "__main__":
    main()

# cd cronosbot/core/
#python3 tests/test_heating.py \
#  --phone1 "5532988967108" \
#  --chat1 "Contato2" \
#  --phone2 "5532988765432" \
#  --chat2 "Contato1" \
#  --iterations 5 \
#  --image "/caminho/para/imagem.jpg" \
#  --vpn