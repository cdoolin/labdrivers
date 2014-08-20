import zmq

context = zmq.Context()

class ZMQConnector(object):
    def __init__(self, server="localhost"):
        self.sock = None
        self.connect(server)
        
    def connect(self, server, port, timeout=200):
        self.server = server

        if self.sock is not None:
            self.sock.close()
        self.sock = context.socket(zmq.REQ)
        self.sock.RCVTIMEO = timeout
        self.sock.LINGER = 0

        try:    
            self.sock.connect("tcp://%s:%d" % (server, int(port)))
            con = True
        except zmq.ZMQError:
            self.sock.close()
            con = False

        return con


    def ok(self):
        if self.sock.closed:
            return False
        connected = False
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
            print "again"

        return connected


class SA(ZMQConnector):
    def __init__(self, server="localhost", port=6634):
        self.sock = None
        self.connect(server, port, timeout=60000)

    def save(self, ntimes=1, info=""):
        msg = "save;%d;%s" % (ntimes, info)
        try:    
            self.sock.send(msg)
            self.sock.recv()
        except:
            pass

    def endsave(self):
        msg = "endsave"
        try:    
            self.sock.send(msg)
            self.sock.recv()
        except:
            pass

class QDaq(ZMQConnector):
    def __init__(self, server="localhost", port=1619):
        self.sock = None
        self.connect(server, port)

    def start(self):
        msg = "startdaq"
        try:    
            self.sock.send(msg)
            self.sock.recv()
        except:
            pass

    def stop(self):
        msg = "stopdaq"
        try:    
            self.sock.send(msg)
            self.sock.recv()
        except:
            pass

    def save(self, name=""):
        msg = "savedaq"
        if len(name) > 0:
            msg += ";" + name
        try:    
            self.sock.send(msg)
            self.sock.recv()
        except:
            pass
