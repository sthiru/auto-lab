import matplotlib.pyplot as plt
import numpy as np
from struct import unpack
import pyvisa as visa

class osciloscope:
    def __init__(self):
        pass

    def acquire(self, channel):
        try:
            rm = visa.ResourceManager()
            resources =rm.list_resources()
            self.scope = rm.open_resource(resources[0])
            
            self.scope.write("DATA:SOURCE CH{0}".format(channel))
            self.scope.write('DATA:WIDTH 2')
            self.scope.write('DATA:ENC SRI')

            ymult = float(self.scope.query('WFMPRE:YMULT?'))
            yzero = float(self.scope.query('WFMPRE:YZERO?'))
            yoff = float(self.scope.query('WFMPRE:YOFF?'))
            xincr = float(self.scope.query('WFMPRE:XINCR?'))

            xzero = float(self.scope.query('WFMPRE:XZERO?'))
            pre_trig_record = int(self.scope.query('WFMPRE:PT_OFF?')) 

            self.scope.write('CURVE?')
            data = self.scope.read_raw()
            self.scope.close()
            rm.close()

            headerlen = 2 + int(data[1])
            header = data[:headerlen]
            ADC_wave = data[headerlen:-1]
            ADC_wave = np.frombuffer(ADC_wave, dtype=np.int16)

            Volts = (ADC_wave - yoff) * ymult  + yzero

            total_time = xincr * len(Volts)
            t_start = (-pre_trig_record * xincr) + xzero
            t_stop = t_start + total_time
            Time = np.linspace(t_start, t_stop, num=len(Volts), endpoint=False)

            return Time,Volts
        except IndexError:
            return 0,0
    
    def get_min_max(self, channel):
        t,v = self.acquire(channel)
        # get the maximum and minium of v
        y_max = max(v)
        y_min = min(v)
        avg= np.average(v)
        return y_max,y_min, avg
    
    def close(self):
        self.scope.close()