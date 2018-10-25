import serial

#def linspace(a, b, n):
#    dx = (float(b) - float(a)) / (n - 1.)
#    x = a
#    while n > 0:
#        yield x
#        x += dx
#        n -= 1

def stepto(a, b, d):
    d = abs(d) if b > a else -abs(d)
    while abs(b - a) > abs(d):
        a += d
        yield a
    yield b

class Attocube(object):
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(port, timeout=1)

        if self.ask("echo off") is not '':
            print("attocube controller not working")

    def ask(self, q):
        # give command to attocube controller and get response.
        self.ser.write(q + "\r\n")
        resp = ""
        last = ""
        while True:
            last = self.ser.readline()
            if last == "OK\r\n":
                # message finished OK
                return resp
            elif last == "ERROR\r\n":
                return "error"
            elif last == "":
                # serialport timedout
                return "timeout"
            else:
                # record the response
                resp += last

    def get_offset(self, axis):
        return float(self.ask("geta %d" % int(axis)).split()[2])

    def step_up(self, axis):
        self.ask("stepu %d" % int(axis))

    def step_down(self, axis):
        self.ask("stepd %d" % int(axis))

    def set_offset(self, axis, volt):
        self.ask("seta %d %f" % (axis, volt))

    def slideto(self, axis, offset, dx=.1):
        for offset in stepto(self.get_offset(axis), offset, dx):
            self.set_offset(axis, offset)


if __name__ == "__main__":
    port = raw_input("serial port: ")
    a = Attocube(port)

    import IPython
    IPython.embed()
