import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import uniform, norm

STEP = 0.001
LABEL_UNIFORM = 'Равномерное распределение'
LABEL_NORMAL = 'Нормальное распределение'


def plot_uniform(a, b):
    if a > b:
        a, b = b, a
    d = (b - a) / 2
    x = np.arange(a-d, b+d, STEP)
    y_pdf = uniform.pdf(x, a, b-a)
    y_cdf = uniform.cdf(x, a, b-a)
    plot_distribution(x, y_pdf, y_cdf, LABEL_UNIFORM)


def plot_norm(mu, sigma, n_sigma=4):
    d = n_sigma*sigma
    x = np.arange(mu-d, mu+d, STEP)
    y_pdf = norm.pdf(x, mu, sigma)
    y_cdf = norm.cdf(x, mu, sigma)
    plot_distribution(x, y_pdf, y_cdf, LABEL_NORMAL)


def plot_axis(ax, x, y, xlabel='x', ylabel='y'):
    ax.plot(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(linewidth=0.4)


def plot_distribution(x, y_pdf, y_cdf, title=''):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
    fig.suptitle(title, y=0.95)

    plot_axis(ax1, x, y_pdf, 'x', 'f(x)')
    plot_axis(ax2, x, y_cdf, 'x', 'F(x)')
    plt.show()


def float_input(label):
    return float(input(label).strip())


if __name__ == '__main__':
    print(LABEL_UNIFORM, 'U(a,b)')
    try:
        a = float_input('a = ')
        b = float_input('b = ')
        plot_uniform(a, b)
    except:
        print('Wrong input!')

    print(LABEL_NORMAL, 'N(m,σ^2)')
    try:
        m = float_input('m = ')
        s = float_input('σ = ')
        plot_norm(m, s)
    except:
        print('Wrong input!')
