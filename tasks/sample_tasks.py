# -*- coding: utf-8 -*-

from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
from utils.log import logger


async def sample_task(url):
    logger.info('run sample task')
    client = AsyncHTTPClient()
    try:
        request = HTTPRequest(url, method='GET')
        response = await client.fetch(request)
        logger.info(f'run tasks successed, result: {response.body}')
    except HTTPError as e:
        logger.error(f'run tasks get request failed, result: {str(e)}')
    except Exception as e:
        logger.error(f'run tasks get other failed, result: {str(e)}')
    finally:
        client.close()
