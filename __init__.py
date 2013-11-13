

def mock(*args):
    class Mock(object):
        def __init__(self, *args, **kwargs):
            pass

        def ok(self):
            return False

    def dummy(self, *args, **kwargs):
        pass

    for a in args:
        setattr(Mock, str(a), dummy)

    return Mock



try:
    from visaa import Vl63, WlMeter
except ImportError:
    print("no visa")
    Vl63 = mock()
    WlMeter = mock('wl')


SAMock = mock('save', 'endsave')

try:
    from zmqq import QDaq, SA
except ImportError:
    print("no zmq")
    QDaq = mock('start', 'stop')
    SA = SAMock



try:
    from websocks import LaserClient
except ImportError:
    print("no websocket-client")
    LaserClient = mock()

try:
    from daq import SimpleDaq
except ImportError:
    print("no nidaqmx")
    SimpleDaq = mock('read')
