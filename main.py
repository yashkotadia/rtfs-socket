from flask import Flask
from flask_sockets import Sockets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjjvtlhfl1232#'
sockets = Sockets(app)

@sockets.route('/websocket')
def handle_frame(ws):
    while not ws.closed:
        message = ws.receive()
        if message is None:  # message is "None" if the client has closed.
            continue
        from detect import get_face_detect_data
        image_data = get_face_detect_data(message)   
        # Send the message to all clients connected to this webserver
        # process. (To support multiple processes or instances, an
        # extra-instance storage or messaging system would be required.)
        clients = ws.handler.server.clients.values()
        for client in clients:
            #print(client.address, client.ws)
            client.ws.send(image_data)

if __name__ == '__main__':
    print("""
This can not be run directly because the Flask development server does not
support web sockets. Instead, use gunicorn:
gunicorn -b 127.0.0.1:8080 -k flask_sockets.worker main:app
""")