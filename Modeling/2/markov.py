import numpy as np
from random import random, randrange
from matplotlib import pyplot as plt

EPS = 1e-3
DT = 1e-3


class Markov:
    MaxSize = 10

    def __init__(self):
        self.graph = np.array([])
        self.result = np.array([])

    def gen_state_graph(self, size):
        size = size if size < self.MaxSize else self.MaxSize
        self.result = np.zeros((size, 3))
        self.graph = np.random.randint(10, size=(size, size), dtype=np.int)
        for i in range(size):
            if random() > 0.2:
                self.graph[i, i] = 0
            # randomly reduce number of edges
            self.graph[randrange(size), randrange(size)] = 0

    def solve(self, axs=[]):
        m = self.graph
        n = m.shape[0]

        coeff_kolmogorov = m.copy().T
        for i in range(n):
            coeff_kolmogorov[i, i] -= sum(m[i])

        p_stable = self.solve_p(m, coeff_kolmogorov.copy())
        self.result[:, 0] = p_stable.round(5)

        p_init = np.array([1] + [0] * (n - 1), dtype=float)
        t1, p1 = self.solve_t(coeff_kolmogorov.copy(), p_stable, p_init)
        self.result[:, 1] = p_stable.round(3)

        p_init = np.array([1 / n] * n)
        tn, pn = self.solve_t(coeff_kolmogorov.copy(), p_stable, p_init)
        self.result[:, 2] = p_stable.round(3)

        if len(axs) == 2:
            label = list(range(1, n + 1))

            n = p1.shape[0]
            t = np.linspace(0, DT * n, n)
            self.plot(t, p1, axs[0], label=label)
            axs[0].scatter(t1, p_stable, s=8, c='m')
            n = pn.shape[0]
            t = np.linspace(0, DT * n, n)
            axs[1].scatter(tn, p_stable, s=8, c='m')
            self.plot(t, pn, axs[1], label=label)

    @staticmethod
    def plot(x, y, axs, *, label=None):
        lines = axs.plot(x, y)
        plt.legend(lines, label, loc='upper left', fontsize='small')

    @staticmethod
    def solve_p(graph, coeff_kolmogorov) -> np.ndarray:
        n = graph.shape[0]
        a = coeff_kolmogorov
        b = np.zeros(n)

        s0 = sum(graph[0])
        b[0] = s0
        for i in range(n):
            a[0, i] += s0
        return np.linalg.solve(a, b)

    @staticmethod
    def solve_t(coeff_kolmogorov, p_stable, p_init):
        n = coeff_kolmogorov.shape[0]
        t_stable = [0] * n
        p_cur = p_init
        p_trace = np.array([p_cur])

        def update_stability(p_c, dp, p_s, t):
            if abs(dp) < EPS and abs(p_c - p_s) < EPS:
                return t
            return 0

        t = 0
        while not all(t_stable):
            t += DT
            dp = (coeff_kolmogorov @ p_cur) * DT
            p_cur += dp
            p_trace = np.append(p_trace, [p_cur], axis=0)

            for i in range(n):
                if t_stable[i] == 0:
                    t_stable[i] = update_stability(p_cur[i], dp[i], p_stable[i], t)

        return t_stable, p_trace
