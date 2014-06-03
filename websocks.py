import websocket
import json


class WSClient(object):
    def __init__(self, server):
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
                return msg
            elif msg['action'] == "nolaser":
                print("no laser connected")
                return None

				
class LaserClient(WSClient):
    def __init__(self, server="127.0.0.1"):
        self.connect("ws://%s:1134/socket" %server)

    def set_volt(self, V):
        V = round(float(V), 1)
        self.call("volt", volt=V)
        self.wait_for(action="piezo")

class ScantechClient(WSClient):
    def __init__(self, server="127.0.0.1"):
        self.connect("ws://%s:5544/socket" % server)

    def set_wave(self, wave):
        self.call("wave", wave=wave)
        self.wait_for(action="wave")

    def set_fine(self, t):
        self.call("setfinetune", tuning=t)
        self.wait_for(action="finetune")

    def power_mode(self, mode):
        self.call("powermode", mode=mode)
        self.wait_for(action="powermode")
		
    def check_ft(self):
        self.call("checkfinetune")
        return self.wait_for(action="ftret")


if __name__ == "__main__":
    l = LaserClient()

    import IPython
    IPython.embed()
