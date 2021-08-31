from tornado import websocket, web, ioloop
import json

cl = []


class WsHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        # TODO: Check if origin is same as domain
        return True

    def on_message(self, message):
        self.write_message(message)

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)


app = web.Application([
    (r'/ws', WsHandler),
])


if __name__ == '__main__':
    app.listen(8000)
    ioloop.IOLoop.current().start()
