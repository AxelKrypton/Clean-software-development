import numpy


def bin_samples(samples: numpy.ndarray, n_bins: int):
    n_samples = samples.shape[0]
    bin_size, samples_rest = divmod(n_samples, n_bins)
    return samples[:n_samples - samples_rest].reshape((n_bins, bin_size)).mean(axis=1)


def main():
    pass


if __name__ == "__main__":
    main()
