

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

try:
    from zmqq import QDaq, SA
except ImportError:
    print("couldn't load zmq")
    QDaq = mock('start', 'stop')
    SA = mock('save', 'endsave')

