import numpy as np
import pytest

from pyautomagic.preprocessing import performFilter


def test_basic_input():
    # Generate 20s dummy EEG data(sampling freq 1kHz)
    # composed of low freq sinusoid signal(10Hz), high freq sinusoid signal(80Hz), power freq sinusoid signal(60Hz),
    times = np.arange(0, 20, .001)
    sfreq = 1000
    low_freq_signal = 5*np.sin(2*np.pi*10*times)
    high_freq_signal = np.cos(2*np.pi*80*times)
    power_freq_noise = 2*np.sin(2*np.pi*60*times)
    input_signal = low_freq_signal + high_freq_signal + power_freq_noise

    output_lowpass_filt = performFilter.performFilter(input_signal, sfreq, 'low', 30)
    output_highpass_filt = performFilter.performFilter(input_signal, sfreq, 'high', 50)
    output_notch_filt = performFilter.performFilter(input_signal, sfreq, 'notch', 60)

    # Test 30Hz low pass filter, the output should only include 10Hz sinusoid signal
    lowpass_error = output_lowpass_filt - low_freq_signal
    assert (np.sqrt(np.mean(lowpass_error**2)) < 0.1)
    # Test 50Hz high pass filter, the output should only include 60Hz and 80Hz sinusoid signal
    highpass_error = output_highpass_filt - (high_freq_signal + power_freq_noise)
    assert (np.sqrt(np.mean(highpass_error**2)) < 0.1)
    # Test 60Hz notch filter, the output should only include 10Hz and 80Hz sinusoid signal
    notch_error = output_notch_filt - (high_freq_signal + low_freq_signal)
    assert (np.sqrt(np.mean(notch_error**2)) < 0.1)


def test_no_input():
    with pytest.raises(TypeError):
        performFilter.performFilter()


def test_lack_filter_input():
    """
    If filter_type is not specified, no filtering will be done, the output should be exactly the same with the input

    """
    times = np.arange(0, 20, .001)
    sfreq = 1000
    input_signal = np.random.normal(0.5, size=np.size(times))
    assert np.array_equal(performFilter.performFilter(input_signal, sfreq), input_signal)

