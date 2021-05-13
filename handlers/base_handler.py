# -*- coding: utf-8 -*-

import tornado.web
import tornado.gen
import json
from typing import Optional, Awaitable
from utils.log import logger


class BaseRequestHandler(tornado.web.RequestHandler):
    def prepare(self) -> Optional[Awaitable[None]]:
        if 'application/json' in self.request.headers.get('Content-Type', ''):
            try:
                self.body_args = json.loads(self.request.body)
            except json.decoder.JSONDecodeError as e:
                self.set_status(400)
                self.write('request body "{}" decode error: {}.\n'.format(
                    self.request.body.decode('utf-8'), e.msg))
                self.finish()
        else:
            logger.debug('request header Content-Type is not \
                contains "application/json".')
            self.body_args = None

    def write(self, response_body):
        pretty = [p.lower() for p in self.get_arguments('pretty')]
        response = response_body
        if pretty and 'false' not in pretty:
            response = json.dumps(response, indent=2)
            self.set_header('Content-Type', 'application/json')
        super().write(response)
