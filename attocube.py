import serial

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

if __name__ == "__main__":
    port = raw_input("serial port: ")
    a = Attocube(port)

    import IPython
    IPython.embed()
