import logging
import threading

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
