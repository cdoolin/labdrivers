import zmq

context = zmq.Context()
s = context.socket(zmq.REQ)
SERVER = "142.244.195.14"
print("connecting to megadaq at %s" % SERVER)
s.connect("tcp://%s:6497" % SERVER)
print("connected.")

def acquire(desc):
	s.send("acquire;%s" % desc)
	s.recv()
