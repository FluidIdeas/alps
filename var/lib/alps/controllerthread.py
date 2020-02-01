from threading import Thread
import os
import time

class ControllerThread:
    def __init__(self, process):
        self.process = process

    def check_and_terminate(self):
        while self.process.poll() == None:
            if os.path.exists('/tmp/alps-run'):
                with open('/tmp/alps-run') as fp:
                    action = fp.read().strip()
                if action == 'TERM':
                    self.process.terminate()
                os.remove('/tmp/alps-run')
            time.sleep(1)

    def start(self):
        thread = Thread(target=self.check_and_terminate)
        thread.start()