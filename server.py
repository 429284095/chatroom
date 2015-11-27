import tornado.web
import tornado.ioloop
import tornado.websocket
import json
import random

class Room(tornado.web.RequestHandler):
    def get(self):
          self.render('temp/msg.html')


class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    @staticmethod
    def send_to_all(message):
        for usr in SocketHandler.clients:
           usr.write_message(json.dumps(message))

    def open(self):
        self.write_message(json.dumps({
           'type': 'info',
           'message': '!System: Welcome to chatroom! Your ID :' + str(id(self))[-5:-3] ,
        }))
        SocketHandler.send_to_all({
           'type': 'info',
           'message': '!System: User'+ str(id(self))[-5:-3] + ' has joined',
        })
        SocketHandler.clients.add(self)
 
    def on_close(self):
        SocketHandler.clients.remove(self)
        SocketHandler.send_to_all({
           'type': 'info',
           'message': '!System: User'+ str(id(self))[-5:-3] + ' has left',
        })

    def on_message(self, message):
        SocketHandler.send_to_all({
           'type': 'user',
           'message': message,
           'id': 'User'+str(id(self))[-5:-3],
        })

if __name__ == '__main__':

    app = tornado.web.Application([
        ('/', Room),
        ('/msg', SocketHandler),
    ])
    app.listen(8001)
    tornado.ioloop.IOLoop.instance().start()

