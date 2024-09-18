import logging

from loguru import logger
from django.conf import settings

from donations.log_handler import LogurugHandler


class CustomLoguruMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self._prepare_config()

    def _prepare_config(self):
        logger.remove()
        logging.basicConfig(handlers=[LogurugHandler()], level=0, force=True)

        if settings.DEBUG:
            logger.add(
                f'{settings.BASE_DIR}/log/debug_mode.log',
                level='DEBUG',
                **settings.LOGURU_CONFIG,
            )

        logger.add(
            f'{settings.BASE_DIR}/log/info.log',
            level='INFO',
            **settings.LOGURU_CONFIG,
        )

        logger.add(
            f'{settings.BASE_DIR}/log/warning.log',
            level='WARNING',
            **settings.LOGURU_CONFIG,
        )

        logger.add(
            f'{settings.BASE_DIR}/log/ERROR.log',
            level='ERROR',
            **settings.LOGURU_CONFIG,
        )

    def __call__(self, request):
        response = self.get_response(request)
        logger.info(f'{request.method} {request.get_full_path()}')
        return response

    def process_exception(self, request, exception):
        logger.error(f"{exception} http_path={request.get_full_path()}")
