# CRONOS
<h1 align="center">
  <br>
  <a href="#"><img src="https://github.com/IMNascimento/DVR/assets/28989407/84028706-5a9e-4d00-af2c-2935e5604035" alt="Nascimento" width="200"></a>
  <br>
  Nascimento
  <br>
</h1>

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

## Introdução

Core Cronos é um protótipo de “core” multiplataforma, compatível com Linux e Windows. Seu desenvolvimento não teve como prioridade a alta escalabilidade, mas sim oferecer uma solução gratuita, de rápida implantação e com configuração mínima, permitindo que qualquer negócio comece a utilizar imediatamente, sem necessidade de ajustes complexos.

## Funcionalidades

- Envio de mensagens para contatos
- Envio de Imagens
- Envio de Audio
- Envio de Documentos
- Envio de mensagem para não contatos
- Autenticação da sessão.

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas:

- [python] versão 3.12

## Instalação

Siga as etapas abaixo para configurar o projeto em sua máquina local:

1. Clone o repositório:
    ```bash
    git clone https://github.com/IMNascimento/CoreCronos.git
    ```
2. Navegue até o diretório do projeto:
    ```bash
    cd CoreCronos
    ```
3. Crie e ative o ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/MacOS
    .\venv\Scripts\activate  # Para Windows
    ```
4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Após a instalação, você pode iniciar a aplicação com o seguinte comando:

```bash
cd core
python3 tests/test_messaging.py \
    --session-phone "5532987869808" \
    --chat-id "Igor Nascimento" \
    --non-contact-phone "5532991463109" \
    --text "Olá, sou o Cronos o melhor disparador!" \
    --image "C:/Users/Igor/Downloads/qr_code-sophia.png" \
    --audio "/caminho/para/audio.mp3" \
    --document "/caminho/para/documento.pdf"
```

O projeto vai logar seu whatsapp web e vai funcionar normalmente.

## Dicas 

- O arquivo STRUCT.md apresenta, de forma comentada, a organização de pastas e arquivos do projeto, facilitando qualquer alteração ou customização que você deseje realizar.

- Para consultar a documentação dos métodos internos do core, abra o arquivo docs/index.html em seu navegador. Lá você encontrará a descrição de cada método, seus parâmetros de entrada e os valores de retorno esperados.

## Dicas de Configuração

### 1. Arquivo de Tags (`tags.py`)
- **O que é:** agrupa todos os _patches_ de seletores (XPath, CSS selectors) que apontam para os campos do WhatsApp Web (caixa de mensagem, botões, lista de contatos etc.).  
- **Quando alterar:** somente após uma atualização do WhatsApp Web que modifique a estrutura do DOM.  
- **Como atualizar:**  
  1. Abra o WhatsApp Web no navegador e pressione **F12** para abrir o DevTools.  
  2. Na aba **Elements**, localize o elemento que deseja atualizar (por exemplo, o campo de entrada de texto).  
  3. Clique com o botão direito sobre o elemento e escolha **Copy ▶ Copy XPath**.  
  4. No seu arquivo de tags, substitua o valor antigo pelo novo XPath, mantendo a chave correspondente (ex.: `"inputMessage": "/html/body/…/div"`).  
  5. Salve o arquivo e reinicie o serviço para que a nova definição seja carregada.

### 2. Arquivo de Configurações (`settings.py`)
- **O que é:** centraliza parâmetros de toda a aplicação — níveis de log, formatos de output, caminhos de armazenamento, limites de retry, timeouts, configurações de proxy/VPN etc.  
- **Ponto de partida:** já vem pré-configurado com valores sensatos para a maioria dos cenários.  
- **Ajustes comuns:**  
  - **Nível de log** (`logLevel`): `DEBUG` para desenvolvimento, `INFO` ou `WARN` em produção.  
  - **Output de logs** (`logFile`, `console`): caminho de arquivo, rotação diária, compressão.  
  - **Timeouts gerais** (`requestTimeout`, `connectTimeout`): ajuste conforme a latência da sua rede.  
  - **Parâmetros de fila** (`maxRetries`, `queueSize`): defina de acordo com o volume esperado de mensagens.  
- **Como editar:**  
  1. Abra o `settings.py` no seu editor de texto.  
  2. Altere os valores conforme necessário, mantendo a estrutura válida.  
  3. Salve o arquivo e reinicie o serviço — a aplicação valida a sintaxe no boot e notificará qualquer erro de configuração.

---

**Mantendo sempre atualizados** esses dois arquivos, você garante que:  
1. Seus seletores de interface continuam apontando para os elementos corretos no WhatsApp Web, mesmo após atualizações de layout.  
2. Seu ambiente de execução (logs, timeouts, retries) permanece alinhado às necessidades de produção, com mínimo esforço de configuração.  
3. A extração de novos _XPaths_ é um processo rápido e repetível — bastam alguns cliques no DevTools!


## Contribuindo

Contribuições são bem-vindas! Por favor, siga as diretrizes em CONTRIBUTING.md para fazer um pull request.

## Licença

Distribuído sob a licença MIT. Veja LICENSE para mais informações.

## Autores

Igor Nascimento - Desenvolvedor Principal - [Perfil GitHub](https://github.com/IMNascimento)

## Agradecimentos
Agradeço à SophiaLabs pela oportunidade de compartilhar este protótipo de estudo de caso de envio de mensagens via WhatsApp. Para quem busca uma solução empresarial de larga escala, recomendo conhecer o [Cronos](https://cronos.sophialabs.com.br) da [SophiaLabs](https://sophialabs.com.br).


O Cronos foi desenvolvido como uma plataforma intuitiva e prática, projetada para manter seus disparos 100% online e totalmente escaláveis, colocando você em operação de forma rápida e sem complicações. Além disso, conta com mecanismos avançados para minimizar o risco de bloqueios no WhatsApp, por meio de gestão inteligente de filas, proxies e VPNs. Com opções de aquisição de números aquecidos e gerenciamento centralizado de campanhas, ele oferece:

- Interface intuitiva: dashboards claros e fluxos de trabalho guiados para todas as operações.

- Antiban integrado: controles automáticos de envio e rotatividade de linhas para manter alta taxa de entrega e compliance.

- Disparos para milhares: envie mensagens para milhares de leads sem sofrer interrupções e, em caso de eventual queda, conte com a rotatividade automática de números.

Descubra como o Cronos pode elevar a comunicação da sua empresa, unindo simplicidade de uso e proteção contra bloqueios de plataforma, levando-a a um novo patamar de desempenho e confiabilidade.
