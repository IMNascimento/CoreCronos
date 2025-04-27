import logging
from logging.handlers import RotatingFileHandler
import os
from core.configs import settings

class LoggerManager:
    """
    Gerencia a criação e o acesso a múltiplos loggers, permitindo gerar
    logs para diferentes módulos, sessões ou contextos (por exemplo, logs
    específicos para cada número ou requisição).
    """
    def __init__(self):
        # Dicionário para armazenar loggers por nome
        self.loggers = {}

    def get_logger(self, name: str, log_file: str = None, level: int = logging.DEBUG) -> logging.Logger:
        """
        Retorna um logger configurado para o nome especificado. Se o logger já
        existir, retorna o mesmo.

        :param name: Nome único para o logger (ex.: "core", "session_5511999999999", etc.)
        :param log_file: Caminho para o arquivo de log. Se None ou string vazia, utilizará apenas o console.
        :param level: Nível de logging (DEBUG, INFO, etc.).
        :return: Instância de logging.Logger configurada.
        """
        if name in self.loggers:
            return self.loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Remove quaisquer handlers já existentes para evitar duplicidade
        if logger.hasHandlers():
            logger.handlers.clear()

        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler para o console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Se for especificado um arquivo de log e for um caminho válido, cria e adiciona um RotatingFileHandler
        if log_file and log_file.strip():
            log_dir = os.path.dirname(log_file)
            if log_dir:  # Verifica se há um diretório definido
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        self.loggers[name] = logger
        return logger

    def log_info(self, name: str, message: str, log_file: str = None):
        """
        Registra uma mensagem de INFO usando o logger identificado por 'name'.
        
        :param name: Nome do logger.
        :param message: Mensagem de log.
        :param log_file: Opcional. Caminho para o arquivo de log específico para esse logger.
        """
        # Se log_file não for fornecido, usa o arquivo padrão definido em settings
        final_log_file = log_file if log_file and log_file.strip() else str(settings.LOG_FILE)
        logger = self.get_logger(name, log_file=final_log_file)
        logger.info(message)

    def log_error(self, name: str, message: str, log_file: str = None):
        """
        Registra uma mensagem de ERROR usando o logger identificado por 'name'.
        
        :param name: Nome do logger.
        :param message: Mensagem de log.
        :param log_file: Opcional. Caminho para o arquivo de log específico para esse logger.
        """
        final_log_file = log_file if log_file and log_file.strip() else str(settings.LOG_FILE)
        logger = self.get_logger(name, log_file=final_log_file)
        logger.error(message)

# Instância global para uso em todo o sistema
logger_manager = LoggerManager()

# Funções auxiliares para facilitar o uso sem acessar diretamente a instância
def log_info(message: str, name: str = "app", log_file: str = None):
    """
    Registra uma mensagem de INFO utilizando o logger padrão ou um especificado.
    
    :param message: Mensagem a ser registrada.
    :param name: Nome do logger (padrão: "app").
    :param log_file: Opcional. Caminho para o arquivo de log.
    """
    logger_manager.log_info(name, message, log_file)

def log_error(message: str, name: str = "app", log_file: str = None):
    """
    Registra uma mensagem de ERROR utilizando o logger padrão ou um especificado.
    
    :param message: Mensagem a ser registrada.
    :param name: Nome do logger (padrão: "app").
    :param log_file: Opcional. Caminho para o arquivo de log.
    """
    logger_manager.log_error(name, message, log_file)
