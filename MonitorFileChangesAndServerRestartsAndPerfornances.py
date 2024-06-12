from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = subprocess.Popen(self.command, shell=True)

    def on_any_event(self, event):
        if event.is_directory:
            return None
        else:
            self.process.terminate()
            self.process = subprocess.Popen(self.command, shell=True)


if __name__ == "__main__":
    path = "."
    command = "flask run"
    event_handler = ChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
