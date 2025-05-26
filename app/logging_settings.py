import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(level=logging.INFO):
    
    dir = "logs"
    
    if not os.path.exists(dir):
        os.makedirs(dir)
        
    log_file = os.path.join(dir, "app.log")
    
    log_format = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Logging configured")
    return logger