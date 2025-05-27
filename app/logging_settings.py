import logging
from logging.handlers import RotatingFileHandler
import os

class SQLAlchemyFilter(logging.Filter):
    """
    Фильтр для отключения логирования SQLAlchemy
    (очень громоздко, можем просто возвращать traceback)
    """
    def filter(self, record):
        return not record.name.startswith('sqlalchemy.engine')
    
    
class SensitiveDataFilter(logging.Filter):
    """
    Фильтр для отключения логирования паролей
    """
    def filter(self, record):
        return not "hash_password" in record.getMessage()

def configure_logging(level=logging.DEBUG):
    """
    Конфигурация логирования
    """
    logging.getLogger('').handlers.clear()   
    
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "app.log")
    
    log_format = "[%(asctime)s] %(module)10s:%(lineno)-3d %(levelname)-7s %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    formatter = logging.Formatter(log_format, datefmt=date_format)
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1000000,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.addFilter(SQLAlchemyFilter())
    file_handler.addFilter(SensitiveDataFilter())
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logging.basicConfig(
        level=level,
        handlers=[file_handler, console_handler]
    )
    
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    sqlalchemy_logger.setLevel(logging.DEBUG)
    sqlalchemy_logger.propagate = False
    
    logger = logging.getLogger(__name__)
    return logger

# if __name__ == "__main__":
#     configure_logging()