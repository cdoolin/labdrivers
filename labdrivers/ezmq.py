"""
easy zmq drivers
"""

import zmq

context = zmq.Context()

class ZmqConnection(object):
    def __init__(self, server, port):
        self.sock = context.socket(zmq.REQ)
        self.sock.connect("tcp://%s:%d" % (server, port))
    
    def ask(self, q):
        self.sock.send(q)
        return self.sock.recv()

class Megadaq(ZmqConnection):
    def __init__(self, server, port=6497):
        ZmqConnection.__init__(self, server, port)

    def acquire(self, desc=""):
        return self.ask("acquire;%s" % desc)



class QDaq(ZmqConnection):
    def __init__(self, server="localhost", port=1619):
        ZmqConnection.__init__(self, server, port)

    def start(self):
        return self.ask("startdaq")

    def stop(self):
        return self.ask("stopdaq")

    def save(self, name=""):
        msg = "savedaq"
        if len(name) > 0:
            msg += ";" + name
        return self.ask(msg)


if __name__ == "__main__":
    print("QDaq(server) or Megadaq(server) or ZmqConnection(server, port)")

    import IPython
    IPython.embed()

