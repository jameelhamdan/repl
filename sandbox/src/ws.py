import json
from tornado import websocket
from .repl import LanguageRepl, Language


class WsLanguageRepl(LanguageRepl):
    def __init__(self, write_message_callback):
        self.write_message_callback = write_message_callback
        super().__init__(language=Language.PYTHON)

    def stdout_callback(self, msg):
        print('WS STDDOUT: %s' % msg)
        self.write_message_callback({
            'type': 'stdout',
            'data': msg,
        })

    def stderr_callback(self, msg):
        print('WS STDERR: %s' % msg)
        self.write_message_callback({
            'type': 'stderr',
            'data': msg,
        })


class WsHandler(websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.repl = WsLanguageRepl(self.write_message)

    def check_origin(self, origin):
        # TODO: Check if origin is same as domain
        return True

    def on_message(self, message):
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            return

        if data['type'] == 'INPUT':
            self.repl.input_queue.put(data['input'])

        if data['type'] == 'SIGNAL':
            self.repl.signal_queue.put(data['signal'])
