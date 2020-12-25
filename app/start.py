import datetime
import os
import signal
import subprocess
import threading
import time

close_requested = False

def on_close(signum, frame):
    print("I'm done.")
    close_requested = True

def parallel(func):
    def pre_hook(*argv):
        t = threading.Thread(target=func)
        t.start()
    return pre_hook

@parallel
def job():
    isotime = datetime.datetime.now().strftime('%H:%M:%S')
    print("{} | I'm working.".format(isotime))

def main():
    # Validate process id.
    if os.getpid() != 1:
        print('This script must be run as root process.')
        print('  pid: ', os.getpid())
    signal.signal(signal.SIGTERM, on_close)

    try:
        mtime = os.path.getmtime('/tempvol/requirements.inst')
    except:
        mtime = 0

    if mtime < os.path.getmtime('requirements.txt'):
        # Install requirements.
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
        subprocess.run(['touch', '/tempvol/requirements.inst'])

    import schedule
    schedule.every(10).seconds.do(job)
    print("I'm started.")
    while not close_requested:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
