#
# visa drivers that can be used remotely via rpyc
#
import time


class WlMeter(object):
    def __init__(self, address):
        # address should be like "server/GPIB::PORT" if remote,
        # or "GPIB::PORT" if local
        a = address.split("/")
        if len(a) > 1:
            import rpyc
            self.conn = rpyc.classic.connect(a[0])
#            self.i = self.conn.modules.visa.instrument(a[1])
            rm = self.conn.modules.visa.ResourceManager()
        else:
            import visa
            rm = visa.ResourceManager()
        self.i = rm.open_resource(a[0])

    def wl(self):
        return float(self.i.ask(":MEAS:SCAL:POW:WAV?"))


    def power(self):
        return float(self.i.ask("MEAS:POW?"))
		

    def ok(self):
        return self.connected



if __name__ == "__main__":
    import IPython
    IPython.embed()
