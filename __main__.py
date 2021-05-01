from eeg_exam import EEGexam


if __name__ == "__main__":
    path = "<edf_path>"
    eeg_exam = EEGexam(path)
    eeg_exam.plot_channel(eeg_exam.channels[0])
