# src/package/logger.py
import logging
import os
import colorlog

APP_ENV = os.environ.get("APP_ENV")


class Logger:
    def __init__(
        self, name: str, log_to_file: bool = True, log_to_console: bool = True
    ):
        self.logger = logging.getLogger(name)
        self._configure_logging(log_to_file, log_to_console)

    def _configure_logging(self, log_to_file: bool, log_to_console: bool):
        # Logger ayarlarını burada yapın
        self.logger.setLevel(logging.DEBUG)

        if log_to_file:
            log_file_path = f"logs/{APP_ENV}/{self.logger.name}.log"
            if not os.path.exists(os.path.dirname(log_file_path)):
                os.makedirs(os.path.dirname(log_file_path))
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                "%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s"
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = colorlog.ColoredFormatter(
                "%(asctime)s\t%(log_color)s%(name)s\t%(levelname)s\t%(reset)s%(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
