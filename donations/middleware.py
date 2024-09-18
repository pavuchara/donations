import logging

from django.conf import settings

from loguru import logger

from donations.log import LogurugHandler


class CustomLoguruMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self._prepare_loguru_config()

    def _prepare_loguru_config(self):
        logging.basicConfig(handlers=[LogurugHandler()], level=0, force=True)
        logger.add(
            f'{settings.BASE_DIR}/log/loguru_logs.json',
            level='INFO',
            serialize=True,
            backtrace=False,
            diagnose=False,
            **settings.LOGURU_CONFIG,
        )
        logger.add(
            f'{settings.BASE_DIR}/log/loguru_info.log',
            level='INFO',
            **settings.LOGURU_CONFIG,
        )
        logger.add(
            f'{settings.BASE_DIR}/log/loguru_warning.log',
            level='WARNING',
            **settings.LOGURU_CONFIG,
        )
        logger.add(
            f'{settings.BASE_DIR}/log/loguru_error.log',
            level='ERROR',
            **settings.LOGURU_CONFIG,
        )

    def __call__(self, request):
        logger.info(f'{request.method} {request.get_full_path()}')
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f"{exception} http_path={request.get_full_path()}")
