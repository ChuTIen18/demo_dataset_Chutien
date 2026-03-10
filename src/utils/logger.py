import logging, sys, os
from datetime import datetime

def get_logger() -> logging.Logger:

    # Format và nơi lưu trữ log
    file_name = f"./log/{datetime.now().strftime('%Y%m%d')}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    os.makedirs(os.path.dirname(file_name),exist_ok=True)

    log_format = '%(asctime)s - %(name)s - %(levelname)s - [Line %(lineno)d] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Config file log
    file_handler = logging.FileHandler(file_name, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

    # Config xuất log ra console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = get_logger()