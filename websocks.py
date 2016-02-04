import websocket
import json
import time


class WSClient(object):
    def __init__(self, server):

        self.connect(server)

    def connect(self, url):
        try:
            self.ws = websocket.create_connection(url)
        except Exception as e:
            print("could not connect to %s" % url)
            raise e


    def ok(self):
        return self.ws is not None

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
        V = float(V)
        self.call("volt", volt=V)
        self.wait_for(action="piezo")

    def get_volt(self):
        self.call("get_volt")
        msg = self.wait_for(action="piezo")
        return msg['now']

    def scan(self, start, stop, slew, save=False):
        self.call("scanonce", start=start, stop=stop, slew=slew, save=save)
        while True:
            msg = self.wait_for("status")
            if msg['text'] == "scan in progress":
                print("scan already in progress :(")
                return None
            elif msg['text'] == "done scan":
                return msg

    def set_wave(self, wave):
        self.call("goto", wave=wave)
        time.sleep(.05)
        self.wait_for("ready")

            


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

    def scan(self, start, stop, speed, save=False):
        self.call("scan", start=start, stop=stop, speed=speed, save=save)
        return self.wait_for(action="scan_stopped")


class OpticsControl(WSClient):
    def __init__(self, server="127.0.0.1"):
        self.connect("ws://%s:8847/socket" % server)

    def set_switch(self, name, state):
        self.call("switch", name=name, state=state)
        self.wait_for(action="switched")

    def set_switches(self, **kwargs):
        for name, state in kwargs.iteritems():
            self.set_switch(name=name, state=state)

    def set_analog(self, volt):
        volt = float(volt)
        if volt < 0. or volt > 5.:
            msg = "voltage (%g) outside 0-5 V" % volt
            raise ValueError(msg)

        self.call("analog", volt=volt)
        self.wait_for(action="analoged")
        




if __name__ == "__main__":
    import IPython
    IPython.embed()
