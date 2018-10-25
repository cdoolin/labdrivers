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
       # print "1" 
        self.call("goto", wave=wave)
      #  print "2"
        time.sleep(.05)
        self.wait_for("ready")
        #return

    def sense_wave(self):
        self.call("checklaser")
        msg = self.wait_for("laser")
        return msg['wave']
    
    def wavelength_input_mode(self):
        self.call("wl_input_mode")
        
    def interrupt(self):
        self.call("interrupt")
            


class ScantechClient(WSClient):
    def __init__(self, server="127.0.0.1", port=5544):
        self.connect("ws://%s:%d/socket" % (server, int(port)))

    def set_wave(self, wave):
        self.call("wave", wave=wave)
        self.wait_for(action="wave")

    def set_fine(self, t):
        self.call("setfinetune", tuning=t)
        self.wait_for(action="finetune")

    def power_mode(self, mode):
        self.call("powermode", mode=mode)
        self.wait_for(action="powermode")
        
    def power(self, pwr):
        self.call("power", power=pwr)
        self.wait_for(action="set_power")
		
    def attenuation(self, attn):
		self.call("attenuation", attenuation = attn)
		self.wait_for(action="set_attenuation")
		
    def check_ft(self):
        self.call("checkfinetune")
        return self.wait_for(action="ftret")

    def scan(self, start, stop, speed):#, save=False):
        self.call("scan", start=start, stop=stop, speed=speed)#, save=save) Might need this for other computers
        return self.wait_for(action="scan_stopped")

    def tell_all(self):
        self.call("tell_all")
        return self.wait_for(action="tell_all")
        
    def chk_wave(self):
        self.call("chk_wave")
        return self.wait_for(action="chk_wave")
        
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
