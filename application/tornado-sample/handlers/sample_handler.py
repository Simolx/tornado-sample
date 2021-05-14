# -*- coding: utf-8 -*-

from handlers.base_handler import BaseRequestHandler
from utils.log import logger


class SampleHandler(BaseRequestHandler):
    def initialize(self, args1, **kwargs):
        self.args1 = args1

    async def get(self):
        logger.info('sample handler, GET')
        self.write(f'hello world, {self.args1}.')

    async def post(self):
        logger.info('sample handler, POST')
        logger.info(
            f'application settings: '
            f'{self.application.settings.get("application_settings", None)}'
        )
        result = self.body_args if self.body_args else self.request.body
        self.write(result)
