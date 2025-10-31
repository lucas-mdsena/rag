import sys
import logging



def setup_logger() -> logging.Logger:
    """Configures logger utility.

    :return: logger object.
    """
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - [%(filename)s:%(lineno)s - %(funcName)s()] - %(levelname)s - %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    if len(root.handlers) == 0:
        root.addHandler(handler)
    
    logger = logging.getLogger('RAG')
    logger.setLevel(logging.INFO)

    return logger

logger = setup_logger()