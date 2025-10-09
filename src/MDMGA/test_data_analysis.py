import pytest
import numpy

from data_analysis import bin_samples


def test_binning():
    n_bins = 20
    bin_size = 5
    binned_samples = numpy.arange(n_bins, dtype=float) * bin_size + numpy.arange(bin_size, dtype=float).mean()
    for n_samples in range(n_bins * bin_size, (n_bins + 1) * bin_size):
        samples = numpy.arange(n_samples, dtype=float)
        assert numpy.all(binned_samples == bin_samples(samples, n_bins))
