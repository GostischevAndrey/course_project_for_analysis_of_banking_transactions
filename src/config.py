import logging


def setup_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """Настройка логгера с указанным именем и файлом"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            "%(levelname)s: %(filename)s: %(funcName)s %(lineno)s: %(asctime)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
