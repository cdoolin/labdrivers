# from nidaqmx import AnalogInputTask
import nidaqmx

# uses old libnidaqmx library
class SimpleDaq_old(object):
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

class SimpleDaq(object):
    def __init__(self, channel, rate, n,maxv=3., terminal='diff',):
        self.n = n
        
        self.task = nidaqmx.Task()

        configtable = {
            'default': nidaqmx.constants.TerminalConfiguration.DEFAULT,
            'diff': nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL,
        }
        

        if isinstance(channel, str):
            channel = [channel]
        for c in channel:
            self.task.ai_channels.add_ai_voltage_chan(
                c, terminal_config=configtable[terminal],
                min_val=-maxv, max_val=maxv)

        self.task.timing.cfg_samp_clk_timing(
            rate=rate, 
            sample_mode=nidaqmx.constants.AcquisitionType.FINITE, 
            samps_per_chan=n)

    def read(self, n=None):
        if n is None:
            n = self.n
            
        self.task.start()
        data = self.task.read(self.n)
        self.task.stop()
        return data




if __name__ == "__main__":
    print("reading from /dev1...")
	
    daq = SimpleDaq(["/dev1/ai%d" % i for i in range(3)], 1000, 10)
	
    print(daq.read())

