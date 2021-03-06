from abc import abstractmethod

import matplotlib.pyplot as plt
import numpy as np


class Domain:

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def plot(self, sfreq=None):
        pass


class TimeDomain(Domain):

    def __init__(self, data):
        super().__init__(data)

    def plot(self, sfreq=None):
        plt.plot(self.data)
        plt.show()
        return


class FreqDomain(Domain):

    def __init__(self, data):
        super().__init__(data)

    def plot(self, sfreq=None):

        if not sfreq:
            raise Exception("Sample frequency is mandatory")

        f_values, channel_freq = self.sampling_data(sfreq)
        plt.plot(f_values, channel_freq)
        plt.show()
        return

    def sampling_data(self, sfreq=None):
        
        if not sfreq:
            raise Exception("Sample frequency is mandatory")

        channel_freq = np.fft.fft(self.data)
        len_channel = len(channel_freq)
        k_array = [i for i in range(0, len_channel)]
        f_values = [((sfreq*i)/len_channel) for i in k_array]
        channel_freq = abs(channel_freq)
        return f_values, channel_freq
    
    def freq_bands(self, sfreq):
        
        freq_bands_list = []
        f_values, channel_freq = self.sampling_data(sfreq)
        get_index = lambda x : f_values.index(x)
    
        band_width = {
            "delta" : np.mean(channel_freq[0:get_index(4)]),
            "tetha" : np.mean(channel_freq[get_index(4):get_index(8)]),
            "alpha" : np.mean(channel_freq[get_index(8):get_index(13)]),
            "beta" : np.mean(channel_freq[get_index(13):get_index(30)]),
            "class" : 1
        }
        band_width = [v*10 if k!='class' else v for k,v in band_width.items()]
        freq_bands_list.append(band_width)
        return freq_bands_list
