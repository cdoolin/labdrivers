
class BadDriver:
    def __init__(self, *args, **kwargs):
        pass

    def ok(self):
        return False

    def start(self):
        pass

    def stop(self):
        pass

try:
    from visaa import Vl63, WlMeter
except ImportError:
    print("no visa")
    Vl63 = BadDriver
    WlMeter = BadDriver

try:
    from zmqq import QDaq, SA
except ImportError:
    print("couldn't load zmq")
    QDaq = BadDriver
    SA = BadDriver

