import config


def receive_message(sock):
    message = sock.recv(config.RECV_BUFFER)[:-2]
    return message.decode("UTF-8")


def send_message(message, sock):
    if not type(message) == bytes:
        message = message.encode()
        try:
            sock.send(message)
        except Exception as e:
            print(e)
