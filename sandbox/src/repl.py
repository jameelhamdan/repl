"""
Run code with language specific commands
"""
import asyncio
import time
from enum import Enum
from queue import Queue
from typing import List


class Language(Enum):
    PYTHON = 'python'
    NODE = 'node'

    def command(self) -> List[str]:
        return {
            self.PYTHON: ['python3'],
            self.NODE: ['node', '-i'],
        }[self]


class Repl:
    """
    Class to wrap subprocess read write communication
    """

    cycle_speed = 0.01  # while loop speed lower is faster

    def __init__(self, command: List[str]):
        self.command = command

        # Initialize Input and Signals Queues
        self.input_queue = Queue()
        self.signal_queue = Queue()

        # Run Subprocess
        self.proc = None
        self.task = asyncio.create_task(self.run(self.command))

    async def _read_stream(self, stream, callback):
        while True:
            line = await stream.readline()
            if not line:
                break
            callback(line)
            time.sleep(self.cycle_speed)

    async def _write_stream(self, stream):
        while True:
            if not self.input_queue.empty():
                line = self.input_queue.get()
                stream.write(line)

            time.sleep(self.cycle_speed)

    async def _send_signal_stream(self):
        while True:
            if not self.signal_queue.empty():
                signal = self.signal_queue.get()
                self.proc.send_signal(signal)

            time.sleep(self.cycle_speed)

    async def run(self, command):
        self.proc = await asyncio.create_subprocess_exec(
            *command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        await asyncio.wait([
            self._send_signal_stream(),
            self._write_stream(self.proc.stdin),
            self._read_stream(self.proc.stdout, self.stdout_callback),
            self._read_stream(self.proc.stderr, self.stderr_callback)
        ])

        return await self.proc.wait()

    def stdout_callback(self, msg):
        print('STDDOUT: %s' % msg)

    def stderr_callback(self, msg):
        print('STDERR: %s' % msg)

    def kill(self):
        self.task.cancel()
        self.proc.kill()


class LanguageRepl(Repl):
    def __init__(self, language: Language):
        self.language = language
        super().__init__(language.command())
