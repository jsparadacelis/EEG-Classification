import re

import mne

from eeg.domains import TimeDomain, FreqDomain


class EEGexam:

    def __init__(self, exam_path):
        self._edf_data = mne.io.read_raw_edf(
                exam_path, preload=True, stim_channel=None, verbose=True)
        self.channels = self._channels()
        self.freq = self._freq()

    def _is_eeg_channel(self, channel: str) -> bool:
        if channel.startswith("EEG") and channel.endswith("REF"):
            eeg_channel_rgx = r'^((F|C|P|O|A)((P\d|\d|Z)|(\d)))$|^T(3|4|5|6)$'
            # removing eeg and -ref strings
            channel = channel[4:-4]
            return re.compile(eeg_channel_rgx).search(channel)
        return False

    def _channels(self):
        return [
            channel
            for channel in self._edf_data.info.ch_names
            if self._is_eeg_channel(channel)]

    def _freq(self):
        return self._edf_data.info["sfreq"]

    def get_channel_data(self, channel_name: str):
        return self._edf_data[
            self._edf_data.ch_names.index(channel_name)][0][0]

    def plot_channel(self, channel_name: str, domain_type: str = "time"):

        channel_data = self.get_channel_data(channel_name)
        if domain_type == "freq":
            FreqDomain(channel_data).plot(self.freq)
        elif domain_type == "time":
            TimeDomain(channel_data).plot()
        else:
            raise Exception(f"{domain_type} is not a valid domain.")
