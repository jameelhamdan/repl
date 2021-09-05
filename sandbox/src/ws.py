import json
from tornado import websocket, log
from .repl import LanguageRepl, Language

clients = []


class WsLanguageRepl(LanguageRepl):
    def __init__(self, write_message_callback, language=Language.PYTHON):
        super().__init__(language)
        self.write_message_callback = write_message_callback
        self.language = language
        log.gen_log.warning(f'INITIALIZE {self.language} REPL')

    def stdout_callback(self, msg):
        log.gen_log.warning('WS STDDOUT: %s' % msg)
        self.write_message_callback({
            'type': 'stdout',
            'data': msg,
        })

    def stderr_callback(self, msg):
        log.gen_log.warning('WS STDERR: %s' % msg)
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
            log.gen_log.warning('ERROR: invalid_input')
            self.write_message({
                'type': 'error',
                'data': 'invalid_request',
            })
            return

        if data['type'] == 'INPUT':
            self.repl.input_queue.put(data['input'])

        if data['type'] == 'SIGNAL':
            self.repl.signal_queue.put(data['signal'])
