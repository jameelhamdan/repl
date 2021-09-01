"""
Run code with language specific commands
"""
import subprocess
import sys
import threading
from enum import Enum
from typing import List


class Language(Enum):
    PYTHON = 'python'
    NODE = 'node'

    @classmethod
    def command(cls) -> List[str]:
        return {
            cls.PYTHON: ['python3'],
            cls.NODE: ['node', '-i'],
        }[cls.value]


class Repl:
    # TODO: Fix and Hook this to websocket

    @staticmethod
    def timed_user_input(timer, wait, buffer_in, buffer_out, buffer_target):
        # we'll be using a separate thread and a timed event to request the user input

        while True:
            timer.wait(wait)
            if not timer.is_set():
                print("> ", end="", file=buffer_out, flush=True)
                print(buffer_in.readline(), file=buffer_target, flush=True)
            timer.clear()

    def __init__(self, language: Language):
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.language = language
        self.proc = subprocess.Popen(
            self.language.command(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True
        )

        self.timer = threading.Event()
        self.input_thread = threading.Thread(
            target=self.timed_user_input,
            args=(self.timer, 1.0, self.stdin, self.stdout, self.proc.stdin)
        )
        self.input_thread.daemon = True
        self.input_thread.start()
        # now we'll read the `rasa` STDOUT line by line, forward it to output_buffer and reset
        # the timer each time a new line is encountered
        for line in self.proc.stdout:
            self.stdout.write(line)  # forward the STDOUT line
            self.stdout.flush()  # flush the output buffer
            self.timer.set()  # reset the timer

    def kill(self):
        self.proc.kill()

    def __del__(self):
        self.kill()
