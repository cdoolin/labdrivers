import websocket
import json

class LaserClient(object):
    def __init__(self, server="127.0.0.1"):
        self.connect(server)

    def connect(self, server):
        url = "ws://%s:1134/socket" % server
        try:
            self.ws = websocket.create_connection(url)
        except:
            self.ws = None

    def ok(self):
        return self.ws is not None


    def set_volt(self, V):
        V = round(float(V), 1)
        self.call("volt", volt=V)
        self.wait_for(action="piezo")

    def call(self, action, **kwargs):
        kwargs.update(action=action)
        self.ws.send(json.dumps(kwargs))

    def wait_for(self, action):
        waiting = True
        while waiting:
            msg = self.ws.recv()
            msg = json.loads(msg)

            if msg['action'] == action:
                waiting = False
            elif msg['action'] == "nolaser":
                print("no laser connected")
                waiting = False


if __name__ == "__main__":
    l = LaserClient()

    import IPython
    IPython.embed()
