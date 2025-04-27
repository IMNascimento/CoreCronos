import random
from selenium.webdriver.chrome.options import Options

class ProxyManager:
    """
    Gerencia a rotação e configuração de proxies (ou VPN via proxy) para o navegador.

    Permite definir uma lista de proxies, selecionar um proxy aleatoriamente ou de forma cíclica,
    e configurar as opções do Chrome para utilizar o proxy escolhido.
    """
    def __init__(self, proxies=None):
        """
        Inicializa o ProxyManager com uma lista de proxies.

        :param proxies: Lista de strings de proxy no formato "http://username:password@proxy_server:port".
                        Se None, inicia com uma lista vazia.
        """
        if proxies is None:
            proxies = []
        self.proxies = proxies
        self.current_index = 0

    def add_proxy(self, proxy: str):
        """
        Adiciona um proxy à lista de proxies.

        :param proxy: String de proxy.
        """
        self.proxies.append(proxy)

    def remove_proxy(self, proxy: str):
        """
        Remove um proxy da lista, se existir.

        :param proxy: String de proxy.
        """
        if proxy in self.proxies:
            self.proxies.remove(proxy)

    def get_random_proxy(self) -> str:
        """
        Retorna um proxy aleatório da lista.

        :return: String do proxy selecionado.
        :raises Exception: Se a lista de proxies estiver vazia.
        """
        if not self.proxies:
            raise Exception("Nenhum proxy disponível.")
        return random.choice(self.proxies)

    def get_next_proxy(self) -> str:
        """
        Retorna o próximo proxy da lista de forma cíclica.

        :return: String do proxy selecionado.
        :raises Exception: Se a lista de proxies estiver vazia.
        """
        if not self.proxies:
            raise Exception("Nenhum proxy disponível.")
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy

    def configure_chrome_options(self, options: Options, proxy: str = None) -> Options:
        """
        Configura as opções do Chrome para utilizar um proxy específico.

        :param options: Instância do Chrome Options.
        :param proxy: Proxy a ser usado. Se None, será selecionado um proxy aleatoriamente.
        :return: A instância de options configurada.
        """
        if proxy is None:
            proxy = self.get_random_proxy()
        options.add_argument(f'--proxy-server={proxy}')
        return options

    def __str__(self):
        return f"ProxyManager(proxies={self.proxies})"


"""
# Exemplo de uso com interface CLI simples para testes.
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gerenciador de Proxies para Bot")
    parser.add_argument("--list", action="store_true", help="Exibe a lista de proxies disponíveis")
    parser.add_argument("--random", action="store_true", help="Exibe um proxy aleatório")
    parser.add_argument("--next", action="store_true", help="Exibe o próximo proxy de forma cíclica")
    args = parser.parse_args()

    # Exemplo de proxies (estes podem vir de um arquivo de configuração ou banco de dados)
    proxies = [
        "http://user:pass@proxy1.example.com:8080",
        "http://user:pass@proxy2.example.com:8080",
        "http://user:pass@proxy3.example.com:8080",
    ]

    manager = ProxyManager(proxies=proxies)

    if args.list:
        print("Proxies disponíveis:")
        for p in manager.proxies:
            print(p)
    elif args.random:
        print("Proxy aleatório:")
        print(manager.get_random_proxy())
    elif args.next:
        print("Próximo proxy:")
        print(manager.get_next_proxy())
    else:
        parser.print_help()
"""