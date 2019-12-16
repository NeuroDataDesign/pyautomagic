import pytest

from pyautomagic.src.rateQuality import rateQuality


def test_basic_input():
    quality_metrics = {'overall_high_amp': 0.15, 'times_high_var': 0.19, 'ratio_bad_chans': 0.27, 'chan_high_var': 0.2}
    expected_rating = {'dataset_qualification': 50}
    calculated_rating = rateQuality(quality_metrics)

    assert (expected_rating['dataset_qualification'] == pytest.approx(calculated_rating['dataset_qualification'], .001))


def test_no_input():
    with pytest.raises(TypeError):
        calculated_rating = rateQuality()


def incorrect_input():
    quality_metrics = {'overall_high_amp': True, 'times_high_var': "Yes", 'ratio_bad_chans': False, 'chan_high_var': -1}
    calculated_rating = rateQuality(quality_metrics)

    assert (calculated_rating[quality_metrics] == {'overall_high_amp': 0.15, 'times_high_var': 0.19, 'ratio_bad_chans': 0.27, 'chan_high_var': 0.2})
