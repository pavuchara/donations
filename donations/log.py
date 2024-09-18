import logging
import sys

from loguru import logger


class LogurugHandler(logging.Handler):
    def emit(self, record):
        # Попытка найти аналогичный уровень логирования в loguru.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
