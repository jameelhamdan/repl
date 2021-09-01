#!/usr/bin/env python
import sys
import argparse
from tornado.ioloop import IOLoop
from tornado.web import Application
from src.ws import WsHandler

app = Application([
    (r'/', WsHandler),
])

parser = argparse.ArgumentParser(description='Run the Websocket service.')
parser.add_argument(
    '-H', '--host', help='Host Address', default='0.0.0.0',
)
parser.add_argument(
    '-p', '--port', help='Host Port', default=8000,
)

if __name__ == '__main__':
    options = parser.parse_args(sys.argv[1:])

    print(f'Running Server at http://{options.host}:{options.port}/')
    print(f'Quit the server with CTRL-BREAK.')
    app.listen(options.port, options.host)

    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        IOLoop.instance().stop()
