import datetime
import logging
import os
import signal
import subprocess
import time

logging.basicConfig(format='%(asctime)s | %(name)7s | %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger('Core')
logger.setLevel(logging.INFO)

def main():
    # Validate process id.
    if os.getpid() != 1:
        logger.error('This script must be run as root process (pid=1).')
        logger.error('  pid: %d', os.getpid())
        return

    # Run pip install when:
    # * First execution
    # * requirement.txt modified
    #
    # !!! Modules schedule & routine must be imported after this section.
    try:
        mtime = os.path.getmtime('/tempvol/requirements.inst')
    except:
        mtime = 0
    if mtime < os.path.getmtime('requirements.txt'):
        logger.info('pip install -r requirements.txt')
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
        subprocess.run(['touch', '/tempvol/requirements.inst'])

    # Handle ```docker-compose down```
    def on_close(signum, frame):
        # !!! Local variable would be assigned without the following definition.
        nonlocal close_requested 
        logger.info("Received `docker-compose down`.")
        close_requested = True
    close_requested = False
    signal.signal(signal.SIGTERM, on_close)

    # Load .env
    from dotenv import load_dotenv
    load_dotenv(verbose=True)

    # Setup jobs.
    import routine
    routine.assign()

    # Run scheduled jobs.
    logger.info("Scheduler started.")
    import schedule
    while not close_requested:
        retval = schedule.run_pending()
        time.sleep(1)
    logger.info("Scheduler stopped.")

if __name__ == '__main__':
    main()
