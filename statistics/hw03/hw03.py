import numpy as np
import math
import matplotlib.pyplot as plt


def generate_uniform_sample(theta, size):
    return np.random.uniform(0, theta, size)


def generate_exp_sample(theta, size):
    return np.random.exponential(theta, size)


def sample_moment(sample, k):
    return np.sum(sample ** k) / sample.size


def uniform_estimator_generator(sample, k):
    return ((k + 1) * sample_moment(sample, k)) ** (1 / k)


def exp_estimator_generator(sample, k):
    return (sample_moment(sample, k) / math.factorial(k)) ** (1 / k)


def generate_estimators(generator, samples, k):
    return list(map(lambda sample: generator(sample, k), samples))


def standard_deviation(sample, mean):
    return np.sum(list(map(lambda x: (x - mean) ** 2, sample))) / len(sample)


def main():
    size = (100, 100)
    theta = 1
    k_range = range(1, 100)

    uniform_samples = generate_uniform_sample(theta, size)
    uniform_deviations = []
    for k in k_range:
        estimators = generate_estimators(uniform_estimator_generator, uniform_samples, k)
        uniform_deviations.append(standard_deviation(estimators, theta))

    exp_samples = generate_exp_sample(theta, size)
    exp_deviations = []
    for k in k_range:
        estimators = generate_estimators(exp_estimator_generator, exp_samples, k)
        exp_deviations.append(standard_deviation(estimators, theta))

    plt.subplot(211)
    plt.plot(k_range, uniform_deviations)
    plt.grid(True)
    plt.xlabel('k')
    plt.ylabel('uniform deviation')
    plt.text(20,
             .0015,
             r'$\theta={},\ estimators\ count={},\ sample\ size={}$'
             .format(theta, size[0], size[1]))

    plt.subplot(212)
    plt.plot(k_range, exp_deviations)
    plt.grid(True)
    plt.xlabel('k')
    plt.ylabel('exp deviation')
    plt.text(20,
             .2,
             r'$\theta={},\ estimators\ count={},\ sample\ size={}$'
             .format(theta, size[0], size[1]))

    plt.show()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
