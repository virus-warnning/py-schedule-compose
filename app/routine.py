import logging
import os
import threading

import requests
import schedule

logger = logging.getLogger('Routine')
logger.setLevel(logging.INFO)

def parallel(func):
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.start()
    return wrapper

def handle_unexpected(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as ex:
            logger.error('Job "%s()" throws an unexpected exception.', func.__name__)
            logger.error('  * Type: %s', type(ex).__name__)
            logger.error('  * Message: %s', str(ex))

            bot = os.getenv('TG_BOT')
            to = os.getenv('TG_TO')
            if bot == '' or to == '':
                return

            # TODO:
            # * message in markdown format
            # * handle network exception
            # * seperate it as a new function
            message = 'Job "%s()" throws an unexpected exception.\n' % func.__name__
            message += '  * Type: %s\n' % type(ex).__name__
            message += '  * Message: %s' % str(ex)
            api = 'https://api.telegram.org/bot{}/sendMessage'.format(bot)
            params = {
                'chat_id': to,
                'text': message,
                # 'parse_mode': 'markdown'
            }
            resp = requests.post(api, data=params)
            if resp.headers['Content-Type'] != 'application/json':
                return

            result = resp.json()
            if result['ok'] == False:
                logger.error('Cannot send telegram message.')

    return wrapper

# Run a job in parallel.
@parallel
def good_job():
    logger.info("I'm working.")

# Handle unexpected exceptions.
# !!! @handle_unexpected must be placed under @parallel.
@parallel
@handle_unexpected
def bad_job():
    i = 1 / 0

# Assign jobs here.
def assign():
    schedule.every(3).seconds.do(good_job)
    schedule.every(10).seconds.do(bad_job)
