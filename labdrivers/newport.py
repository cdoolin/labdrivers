import newpdll
import time



class Vl67:
    def __init__(self):
        self.connect()

    def connect(self):
        self.l = newpdll.Device()
        # self.l.verbose = True

        self.idn = self.l.ask("*IDN?")
        if self.idn.find("6700") < 0:
            self.connected = False
        else:
            self.connected = True
            self.set_remote()
            # use constant current mode
            self.l.ask("SOUR:CPOW 0")
            # make sure wavelength tracking is off
            self.l.ask("OUTP:TRAC 0")


    def ok(self):
        return self.connected

    def identity(self):
        return self.idn

    def set_piezo(self, v):
        v = float(v)
        r = self.l.ask("SOUR:VOLT:PIEZ %.2f" % v)
        if r != "OK":
            print("error: %s (%f)" % (r, v))

    def get_piezo(self):
        return float(self.l.ask("SOUR:VOLT:PIEZ?"))

    def sense_piezo(self):
        return float(self.l.ask("SENS:VOLT:PIEZ"))

    def sense_wave(self):
        return float(self.l.ask("SENS:WAVE"))

    def set_wave(self, wave):
        self.l.ask("SOUR:WAVE %.2f" % float(wave))
        self.l.ask("OUTP:TRAC 1")
        time.sleep(.01)
        self.wait()
        self.l.ask("OUTP:TRAC 0")

    def sense_current(self):
        #print self.l
        return self.l.ask("SENS:CURR:DIOD")
        #return float(curr)

    def set_current(self, current):
        self.l.ask("SOUR:CURR:DIOD %.1f" % float(current))

    def set_local(self):
        self.l.ask("SYST:MCON LOC")

    def set_remote(self):
        self.l.ask("SYST:MCON REM")

    def set_start(self, start):
        return self.l.ask("SOUR:WAVE:START %s" % start)

    def get_start(self):
        return self.l.ask("SOUR:WAVE:START?")

    def set_stop(self, stop):
        return self.l.ask("SOUR:WAVE:STOP %s" % stop)

    def get_stop(self):
        return self.l.ask("SOUR:WAVE:STOP?")

    def set_slew_f(self, slew):
        self.l.ask("SOUR:WAVE:SLEW:FORW %s" % slew)

    def get_slew_f(self):
        return self.l.ask("SOUR:WAVE:SLEW:FORW?")

    def set_slew_r(self, slew):
        self.l.ask("SOUR:WAVE:SLEW:RET %s" % slew)

    def set_slew(self, f, r):
        self.l.ask("SOUR:WAVE:SLEW:FORW %s" % f)
        self.l.ask("SOUR:WAVE:SLEW:RET %s" % r)

    def reset(self):
        # reset command seems to not work,  so manually set wavelength
        self.l.ask("OUTP:SCAN:STOP")
        start = self.l.ask("SOUR:WAVE:START?")
        self.l.ask("SOUR:WAVE " + start)
        #self.l.ask("OUTP:SCAN:RESET")

    def start(self):
        self.l.ask("OUTP:SCAN:START")

    def stop(self):
        self.l.ask("OUTP:SCAN:STOP")

    def ready(self):
        return int(self.l.ask("*OPC?")) == 1

    def wait(self):
        while int(self.l.ask("*OPC?")) is 0:
            time.sleep(.01)

    def set_power(self, on):
        self.l.ask("OUTP:STAT %d" % int(on))

    def powered(self):
        return int(self.l.ask("OUTP:STAT?")) == 1
        
    def set_track(self, track):
        self.l.ask("OUTP:TRAC %d" % (bool(track)))

        


if __name__ == "__main__":
    l = Vl67()
    #l.set_local()
    import IPython
    IPython.embed()
