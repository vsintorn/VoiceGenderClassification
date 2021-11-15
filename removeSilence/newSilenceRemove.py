import os # kaggle OS
import numpy as np # linear algebra
import pandas as pd # data processing
from tqdm import tqdm_notebook as tqdm # progress bar
import IPython.display as ipd # .wav visualizations
from scipy.io import wavfile # return sample rate (in samples/sec) and data from a WAV file
import matplotlib.pyplot as plt # plots

% matplotlib inline

train_ids = next(os.walk("../input/audio_train/"))[2]
test_ids = next(os.walk("../input/audio_test/"))[2]

ipd.Audio("../input/audio_train/31440023.wav")

sample_rate, audio = wavfile.read("../input/audio_train/31440023.wav")

plt.plot(audio); # plot the audio chart with MatPlot



def normalize_audio(audio):
    # audio = (audio + 32768) / 65535 (only if bits were correct)
    audio = audio / max(np.abs(audio))
    return audio


def divide_audio(audio, resolution=100, window_duration=0.1, minimum_power=0.001, sample_rate=44100):
    duration = len(audio) / sample_rate # in samples/sec
    iterations = int(duration * resolution)
    step = int(sample_rate / resolution)
    window_length = np.floor(sample_rate * window_duration)
    audio_power = np.square(normalize_audio(audio)) / window_length #Normalized power to window duration

    start = np.array([])
    stop = np.array([])
    is_started = False

    for n in range(iterations):
        power = 10 * np.sum(audio_power[n * step : int(n * step + window_length)]) # sensitive
        if not is_started and power > minimum_power:
            start = np.append(start, n * step + window_length / 2)
            is_started = True
        elif is_started and (power <= minimum_power or n == iterations-1):
            stop = np.append(stop, n * step + window_length / 2)
            is_started = False

    if start.size == 0:
        start = np.append(start, 0)
        stop = np.append(stop, len(audio))

    start = start.astype(int)
    stop = stop.astype(int)

    # We don't want to eliminate EVERYTHING that's unnecessary
    # There should be a little boundary...
    # 200 frame buffer before and after

    # minus = ?
    if start[0] > 200:
        minus = 200
    else:
        minus = start[0]

    # plus = ?
    if (len(audio) - stop[0]) > 200:
        plus = 200
    else:
        plus = len(audio) - stop[0]

    return (start - minus), (stop + plus)


start, stop =  divide_audio(audio)
print(start)
print(stop)
plt.plot(audio[start[0]:stop[0]]);
