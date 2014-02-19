"""Usage: wsgi-supervisor [options] <file>

Options:
    -e, --extensions=exts    only file with those extensions will be watched
                             [default: py]
    -w, --watch=folders      folders to watch
    -a, --app=appname        app name to import [default: app]
    -d, --pwd=path           path to app folder
    -p, --port=port          port to bind [default: 3000]
    --python=python          python excutable [default: python]

Examples:
    wsgi-supervisor app.py
    wsgi-supervisor -e js,py -w public/js,controllers app.py
"""

import os
import sys
import signal

from datetime import datetime
from subprocess import Popen
from threading import Thread
from time import sleep

from pyinotify import ProcessEvent, Notifier, WatchManager, IN_MODIFY
from docopt import docopt


class AppRunner():

    def __init__(self, file_name, app_name, port, pwd, python):
        self.params = [python,
                    os.path.join(os.path.dirname(__file__), 'server.py'),
                    file_name, app_name, port, pwd]

    def respawn(self):
        self.kill()
        self.spawn()

    def spawn(self):
        self.ps = Popen(self.params)

    def kill(self):
        self.ps.kill()

    def poll(self):
        return self.ps.poll()


class Supervisor(Thread):
    """"supervise the spawned application, spawn it when crashed"""

    def __init__(self, runner):
        Thread.__init__(self)
        self.should_stop = False
        self.runner = runner

    def run(self):
        delay = 0
        interval = 0.1
        while not self.should_stop:
            sleep(interval)
            delay -= interval
            if delay > 0:
                continue
            delay = 1
            if self.runner.poll():
                print(get_time() + "restaring on crash")
                self.runner.spawn()

    def stop_asap(self):
        self.should_stop = True


class Handler(ProcessEvent):

    def my_init(self, extensions):
        self.extensions = extensions

    def process_IN_MODIFY(self, event):
        _, ext = os.path.splitext(os.path.basename(event.pathname))
        if ext in self.extensions:
            print("%s changed" % event.pathname)
            print(get_time() + "restaring on file change")
            app_runner.respawn()


def watch(pathes, extensions):
    manager = WatchManager()
    handler = Handler(extensions=extensions)
    notifier = Notifier(manager, default_proc_fun=handler)
    for path in pathes:
        manager.add_watch(path, IN_MODIFY, rec=True, auto_add=True)
    notifier.loop()

def signal_handler(signal, frame):
    supervisor.stop_asap()
    while supervisor.isAlive():
        sleep(.1)
    print("")
    print(get_time() + "stopping")
    app_runner.kill()
    sys.exit(0)

def get_time():
    return datetime.now().strftime("%a, %d-%b-%Y %H:%M:%S ")


args = docopt(__doc__, version='0.0.1')

exts = [e if e.startswith('.') else '.' + e
        for e in args['--extensions'].split(',')]

app_runner = AppRunner(
    file_name=args['<file>'],
    app_name=args['--app'],
    python=args['--python'],
    pwd=args['--pwd'] or os.getcwd(),
    port=args['--port'],
)
supervisor = Supervisor(app_runner)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    app_runner.spawn()
    supervisor.start()

    folders = args['--watch'] or os.getcwd()
    watch(folders.split(','), exts)
