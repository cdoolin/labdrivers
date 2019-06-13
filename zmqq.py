# import socket
from gevent import socket
import zmq 
# if socket.socket.__module__ == "gevent.socket":
#     from gevent.coros import RLock
#     print("MANKEY PATCHD")
# else:
#     print("dummy lock")
#     class RLock:
#         def acquire(self):
#             pass
#         def release(self):
#             pass

from gevent.lock import Semaphore
glock = Semaphore()

context = zmq.Context()

def lock(func):
    def lockedfunc(*args, **kwargs):
        # with args[0].lock:
        print("in %s" % func.__name__)
        with glock:
            r = func(*args, **kwargs)
        #args[0].lock.release()
        print("out %s" % func.__name__)
        return r
    return lockedfunc

class ZMQConnector(object):
    def __init__(self, timeout=200):
        self.timeout = timeout
        self.sock = None
        self.lock = Semaphore()

    @lock
    def connect(self, server, port):
        self.server = server

        if self.sock is not None:
            self.sock.close()
        self.sock = context.socket(zmq.REQ)
        self.sock.LINGER = 0
        self.sock.RCVTIMEO = self.timeout

        try:
            self.sock.connect("tcp://%s:%d" % (server, int(port)))
            con = True
        except zmq.ZMQError:
            self.sock.close()
            con = False


        return con


    @lock
    def ok(self):
        #return False
        if self.sock.closed:
            return False
        connected = False
        self.sock.RCVTIMEO = 200
        try:
            self.sock.send('ping', zmq.NOBLOCK)

            m = self.sock.recv()
            if str(m) == "pong":
                connected = True
        except zmq.ZMQError:
            try:
                self.sock.recv()
            except zmq.Again:
                pass
        except zmq.Again:
            print "zmqq: again"
        self.sock.RCVTIMEO = self.timeout
        return connected

    @lock
    def ask(self, msg):
        print self.sock.RCVTIMEO
        try:
            self.sock.send(msg)
            response = self.sock.recv()
        except Exception as e:
            #print("couldn't send '%s': %s" % (msg, e))
            response = None
        return response


class SA(ZMQConnector):
    def __init__(self, server="localhost", port=6634):
        ZMQConnector.__init__(self, timeout=60000)
        self.connect(server, port)

    def save(self, ntimes=1, info=""):
        return self.ask("save;%d;%s" % (ntimes, info))

    def endsave(self):
        return self.ask("endsave")


class QDaq(ZMQConnector):
    def __init__(self, server="localhost", port=1619):
        ZMQConnector.__init__(self, timeout=60000)
        self.connect(server, port)

    def start(self):
        return self.ask("startdaq")

    def stop(self):
        return self.ask("stopdaq")


    def save(self, name=""):
        msg = "savedaq"
        if len(name) > 0:
            msg += ";" + name
        return self.ask(msg)
