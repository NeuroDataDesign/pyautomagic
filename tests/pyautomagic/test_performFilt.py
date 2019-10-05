import mne
import numpy as np
import pytest
from pyautomagic.preprocessing import performFilter


times = np.arange(0,.001,20)
low_freq_signal = 2*np.sin(2*np.pi*10*times)
high_freq_signal = np.cos(2*np.pi*80*times)
power_freq_noise = 5*np.sin(2*np.pi*60*times)
white_noise = np.random.normal(0.5,size=np.size(times))
