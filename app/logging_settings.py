import logging
from logging.handlers import RotatingFileHandler
import os

class SQLAlchemyFilter(logging.Filter):
    def filter(self, record):
        return not record.name.startswith('sqlalchemy.engine')

def configure_logging(level=logging.INFO):
    logging.getLogger('').handlers.clear()

    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "app.log")
    
    log_format = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s %(message)s"
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
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logging.basicConfig(
        level=level,
        handlers=[file_handler, console_handler]
    )
    
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    sqlalchemy_logger.setLevel(logging.INFO) 
    sqlalchemy_logger.handlers = [console_handler] 
    sqlalchemy_logger.propagate = False
    
    logger = logging.getLogger(__name__)
    return logger

if __name__ == "__main__":
    configure_logging()