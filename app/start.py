import os
import signal
import subprocess
import time

close_requested = False

def on_close(signum, frame):
    print("I'm done.")
    close_requested = True

def job():
    print("I'm working.")

def main():
    # Validate process id.
    if os.getpid() != 1:
        print('This script must be run as root process.')
        print('  pid: ', os.getpid())
    signal.signal(signal.SIGTERM, on_close)

    try:
        mtime = os.path.getmtime('requirements.inst')
    except:
        mtime = 0

    if mtime < os.path.getmtime('requirements.txt'):
        # Install requirements.
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
        subprocess.run(['touch', 'requirements.inst'])

    import schedule
    schedule.every(3).seconds.do(job)
    while not close_requested:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
