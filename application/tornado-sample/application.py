# -*- coding: utf-8 -*-

import functools
from tornado.options import define, options, parse_command_line
import tornado.web
import tornado.ioloop
from tornado.ioloop import PeriodicCallback
from handlers.sample_handler import SampleHandler
from tasks.sample_tasks import sample_task
from utils.log import logger

define(
    'port', default=9000, type=int,
    help='The port that server will listen on.'
)
define(
    'apm', default=False, type=bool,
    help='enable application apm.'
)
define(
    'apm_server', default='http://localhost:8200', type=str,
    help='apm erver address.'
)
define(
    'debug', default=False, type=bool,
    help='The server run in development mode or not.'
)


def main():
    handlers = [
        tornado.web.URLSpec(
            r'/example', SampleHandler,
            dict(args1='args1')
        )
    ]
    url = f'http://localhost:{options.port}/example'
    backup_tasks = PeriodicCallback(
        functools.partial(sample_task, url),
        10 * 1000
    )
    backup_tasks.start()
    current = tornado.ioloop.IOLoop.current()
    application = tornado.web.Application(
        handlers=handlers,
        application_settings='default settings',
        debug=options.debug,
    )
    if options.apm:
        from elasticapm.contrib.tornado import ElasticAPM
        application.settings['ELASTIC_APM'] = {
            'SERVER_URL': options.apm_server,
            'SERVICE_NAME': 'tornado-sample_apm',
            'SECRET_TOKEN': 'tornado-sample_secret-token'
        }
        apm = ElasticAPM(application)
    logger.info(f'start server, listen on {options.port}.')
    application.listen(options.port)
    current.start()


if __name__ == '__main__':
    try:
        parse_command_line()
        main()
    except KeyboardInterrupt:
        logger.info("exit, close server.")
    except Exception as e:
        logger.error(str(e))
