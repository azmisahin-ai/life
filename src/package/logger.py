# src/package/logger.py
import logging
import os
import colorlog

APP_ENV = os.environ.get("APP_ENV")

application_log_function = None


def logger_event(log_function):
    global application_log_function
    application_log_function = log_function


class Logger:
    def __init__(
        self,
        name: str,
        log_to_file: bool = False,
        log_to_console: bool = False,
        log_to_event: bool = True,
    ):
        self.logger = logging.getLogger(name)
        self._configure_logging(log_to_file, log_to_console)
        self.log_to_event = log_to_event

    def _configure_logging(self, log_to_file: bool, log_to_console: bool):
        self.logger.setLevel(logging.DEBUG)

        if log_to_file:
            log_file_path = f"logs/{APP_ENV}/{self.logger.name}.log"
            if not os.path.exists(os.path.dirname(log_file_path)):
                os.makedirs(os.path.dirname(log_file_path))
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                "%(asctime)23s\t%(name)-20s\t%(levelname)-8s\t%(message)s"
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

    def _send_to_event(self, type, message):
        if self.log_to_event:
            # send application log signal
            if application_log_function is not None:
                # uygulama log sinyalini gönder
                application_log_function(type, message)

    def info(self, message, *args, **kwargs):
        self.logger.info(message)
        self._send_to_event("info", message)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(message)
        self._send_to_event("warning", message)

    def error(self, message, *args, **kwargs):
        self.logger.error(message)
        self._send_to_event("error", message)

    def debug(self, message, *args, **kwargs):
        self.logger.debug(message)
        self._send_to_event("debug", message)

    def critical(self, message, *args, **kwargs):
        self.logger.critical(message)
        self._send_to_event("critical", message)

    def exception(self, message, *args, exc_info=True, **kwargs):
        self.logger.exception(message)
        self._send_to_event("exception", message)

    def get_logger(self):
        # our logger
        return self

        # orjinal logger
        return self.logger


# Log ayarlarını yapılandırma
logger = Logger(name="application").get_logger()

# Example Usage
if __name__ == "__main__":
    logger.info("Bu bir bilgi mesajıdır.")
    logger.warning("Bu bir uyarı mesajıdır.")
    logger.error("Bu bir hata mesajıdır.")
