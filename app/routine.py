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

@parallel
def job():
    logger.info("I'm working.")

def assign():
    # Assign jobs here.
    schedule.every(3).seconds.do(job)
