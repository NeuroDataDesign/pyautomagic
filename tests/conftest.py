import pytest


@pytest.fixture(scope="class")
def eegts():
    """
    Creating a pytest fixture for a fake EEG Time series init.

    :return:
    """
    eegts = []
    # eegts = EEGTimeSeries(rawdata, times, contacts, samplerate, modality)
    return eegts
