import visa
import time



class Vl63(object):
    def __init__(self, port=9):
        self.l = visa.instrument("GPIB::%d" % port)

        self.idn = self.l.ask("*IDN?")
        if self.idn.find("NewFocus 63") < 0:
            self.connected = False
            del self.l
        else:
            self.connected = True
            self.set_remote()
            # make sure wavelength tracking is off
            self.l.ask(":OUTP:TRAC OFF")

    def ok(self):
        return self.connected

    def identity(self):
        return self.idn

    def set_piezo(self, v):
        r = self.l.ask(":VOLT %.1f" % v)
        if r != "OK":
            print("error: %s (%f)" % (r, v))

    def get_piezo(self):
        return float(self.l.ask(":VOLT?"))

    def sense_piezo(self):
        return float(self.l.ask(":SENS:VOLT:PIEZ"))

    def sense_wave(self):
        return float(self.l.ask(":SENS:WAVE"))

    def set_wave(self, wave):
        self.l.write(":WAVE %.2f" % float(wave))

    def sense_current(self):
        return float(self.l.ask(":SENS:CURR:DIOD"))

    def set_current(self, current):
        self.l.write(":CURR %.1f" % float(current))

    def set_local(self):
        self.l.write(":SYST:MCON EXT")

    def set_remote(self):
        self.l.write(":SYST:MCON INT")

    def set_start(self, start):
        return self.l.ask(":WAVE:STAR %s" % start)

    def get_start(self):
        return self.l.ask(":WAVE:STAR?")

    def set_stop(self, stop):
        return self.l.ask(":WAVE:STOP %s" % stop)

    def get_stop(self):
        return self.l.ask(":WAVE:STOP?")

    def set_slew_f(self, slew):
        self.l.ask(":WAVE:SLEW:FORW %s" % slew)

    def get_slew_f(self):
        return self.l.ask(":WAVE:SLEW:FORW?")

    def set_slew_r(self, slew):
        self.l.ask(":WAVE:SLEW:RET %s" % slew)

    def set_slew(self, f, r):
        self.l.ask(":WAVE:SLEW:FORW %s" % f)
        self.l.ask(":WAVE:SLEW:RET %s" % r)

    def reset(self):
        self.l.write(":OUTP:SCAN:RESE")

    def start(self):
        self.l.write(":OUTP:SCAN:STAR")

    def stop(self):
        self.l.write(":OUTP:SCAN:STOP")

    def ready(self):
        return int(self.l.ask("*OPC?")) == 1

    def wait(self):
        while int(self.l.ask("*OPC?")) is 0:
            time.sleep(.010)

    def set_power(self, on):
        self.l.write(":OUTP %d" % int(on))

    def powered(self):
        return int(self.l.ask(":OUTP?")) == 1
        
        

class WlMeter(object):
    def __init__(self, port=4):
        self.i = visa.instrument("GPIB::%d" % port)

        self.i.write(":INIT:CONT OFF")

    def wl(self):
        return float(self.i.ask(":MEAS:SCAL:POW:WAV?"))


if __name__ == "__main__":
    l = Vl63()
    l.set_local()
