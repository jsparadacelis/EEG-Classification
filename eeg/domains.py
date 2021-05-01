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

        channel_freq = np.fft.fft(self.data)
        len_channel = len(channel_freq)
        k_array = [i for i in range(0, len_channel)]
        f_values = [((sfreq*i)/len_channel) for i in k_array]
        channel_freq = abs(channel_freq)
        return f_values, channel_freq
