import scipy
from scipy.stats import norm, chi2
import numpy as np
import matplotlib.pyplot as plt


def generate_standard_normal_sample(n):
    return np.random.normal(0, 1, n)


def standard_normal_quantile(p):
    return scipy.stats.distributions.norm.ppf(p)


def chi2_quantile(p, n):
    return scipy.stats.distributions.chi2.ppf(p, n)


def sum_k(sample, k):
    return np.sum(sample ** k)


def sample_mean(sample):
    return np.sum(sample) / len(sample)


def main():
    gamma = 0.75
    m_range = range(1, 100)
    n_range = range(1, 100)

    res_a = []
    for n in n_range:
        res = []
        for m in m_range:
            sample = generate_standard_normal_sample(n)
            sum_2 = sum_k(sample, 2)
            res.append(sum_2 / chi2_quantile((1 - gamma) / 2, n) -
                       sum_2 / chi2_quantile((1 + gamma) / 2, n))
        res_a.append(sample_mean(res))

    res_b = []
    for n in n_range:
        res = []
        for m in m_range:
            sample = generate_standard_normal_sample(n)
            mean = sample_mean(sample)
            n_mean2 = n * (mean ** 2)
            res.append(n_mean2 / (standard_normal_quantile((3 - gamma) / 4) ** 2) -
                       n_mean2 / (standard_normal_quantile((3 + gamma) / 4) ** 2))
        res_b.append(sample_mean(res))

    plt.subplot(211)
    plt.plot(n_range, res_a)
    plt.grid(True)
    plt.xlabel('n')
    plt.ylabel('a) mean length')

    plt.title(r'$\gamma={}$'.format(gamma))

    plt.subplot(212)
    plt.plot(n_range, res_b)
    plt.grid(True)
    plt.xlabel('n')
    plt.ylabel('b) mean length')

    plt.show()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
