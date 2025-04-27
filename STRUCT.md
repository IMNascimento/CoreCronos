CronosBot
|
├── core/    # core do sistema cronos
|   ├── config/  # pasta de configuração
|   |   ├── __init__.py 
|   |   ├── settings.py
|   |   └── tags.py
|   |   
|   ├── cronos/ #pasta com metodos de envio e sessões do whatsapp aqui estão todos os metodos da core
|   |   ├── __init__.py 
|   |   ├── manager.py          # classe de gerenciamento dos metodos para envio de mensagem e etc. Nessa classe consumimos todas as outras classes.
|   |   ├── messaging.py        #classe para envio de mensagens como texto, imagem, audio e etc e abertura de chat e fechamento.
|   |   ├── proxy_manager.py   #classe para manipular a vpn e proxy para sessoes de navegação
|   |   └── session.py         # classe para manipular a sessão do whatsapp
|   |
|   ├── tests/
|   |   └── test_messaging.py  # arquivo de teste para envio de mensagem para verificar se a core está funcionando normalmente.
|   |
|   └── utils/
|       ├── __init__.py
|       └── logger.py  # Classe que gerencia o log do sistema
|
| 
├── docs/   # documentação do projeto
|   ├── core/   # documentação do projeto core com pdoc
|   ├── index.html 
|   └── core.html   
|
├── logs/
|   └── app.log         # Arquivo de logs da core 
|
├── sessions/      # pasta com os arquivos da sessão do navegador e cookies do selenium
|   └── 5532999898733/
|
├── qrcode/                                 # pasta para guarda os qrcode para autenticação
|   └── 553299989843_qrcode.png           # imagens do qrcode
│
├── README.md                      # Arquivo de introdução ao sistemas
├── requirements.txt    # arquivos de dependencias de instalação python
└── .env               # Ponto de configuração de servidor e etc