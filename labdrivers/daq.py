from nidaqmx import AnalogInputTask

class SimpleDaq(object):
    def __init__(self, channel, rate, n,maxv=3.):
        self.n = n
        
        self.task = AnalogInputTask()

        if isinstance(channel, str):
            channel = [channel]
        for c in channel:
            self.task.create_voltage_channel(
                c, terminal = 'diff',
                min_val=-maxv, max_val=maxv)

        self.task.configure_timing_sample_clock(
            rate=rate, sample_mode='finite', samples_per_channel=n)

    def read(self):
        self.task.start()
        data = self.task.read(self.n, fill_mode='group_by_channel')
        self.task.stop()
        return data


if __name__ == "__main__":
    print("reading from /dev1...")
	
    daq = SimpleDaq(["/dev1/ai%d" % i for i in range(3)], 1000, 10)
	
    print(daq.read())

