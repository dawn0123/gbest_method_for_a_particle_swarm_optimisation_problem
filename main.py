'''
Implementation of gbest method for solving a particle swarm optimisation problem.
'''
import numpy as np
import matplotlib.pyplot as plt
X1_MIN, X1_MAX, X2_MIN, X2_MAX = 0., 6., 0., 6.


def f(x1, x2):
    return (x1 - 3.14)**2 + (x2 - 2.72)**2 + np.sin(3 * x1 + 1.41) + np.sin(4 * x2 + 1.73)


def print_vectors(V, heading, name='x'):
    print(heading, end='')
    for i, v in enumerate(V):
        print("%s%d = [%.3f, %.3f]" % (name, i+1, v[0], v[1]), end='    ')
    print("")


def plot_contour(X, gbest, title=""):
    x, y = np.array(np.meshgrid(np.linspace(X1_MIN, X1_MAX, 100),
                    np.linspace(X2_MIN, X2_MAX, 100)))
    z = f(x, y)
    plt.figure(figsize=(6, 6))
    plt.title(title)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.xlim(X1_MIN, X1_MAX)
    plt.ylim(X2_MIN, X2_MAX)
    plt.contour(x, y, z, 10)
    plt.scatter(X[..., 0], X[..., 1], cmap='bo')
    plt.plot(gbest[0], gbest[1], 'r*')
    plt.show()


def solve(X, V, w, c1, c2, r1, r2, nIter):
    print_vectors(X, "Initial positions: ", 'x')
    print_vectors(V, "Initial velocities: ", 'v')
    plot_contour(X, np.array([X1_MIN-1, X2_MIN-1]), "Iteration t = 0")
    size = len(X)
    pbest = X
    f_pbest = f(X[..., 0], X[..., 1])
    print("Values of the objective function: ",
          "    ".join(map(lambda i, x: "f%d = %.3f" % (i+1, x), range(size), f_pbest)))
    gbest = X[np.argmin(f_pbest)]
    f_gbest = np.min(f_pbest)
    for it in range(1, nIter+1):
        print("--------------------Iteration %02d--------------------" % (it))
        V = w * V + c1 * r1 * (pbest - X) + c2 * r2 * (gbest - X)
        X = X + V
        print_vectors(X, "Positions: ", 'x')
        print_vectors(V, "Velocities: ", 'v')
        f_pcurrent = f(X[..., 0], X[..., 1])
        print("Values of the objective function: ",
              "    ".join(map(lambda i, x: "f%d = %.3f" % (i+1, x), range(size), f_pcurrent)))
        f_gcurrent = np.min(f_pcurrent)
        for i, flag in enumerate(f_pcurrent < f_pbest):
            if flag:
                print(
                    f"Particle {i + 1} updates its personal best performance.")
        pbest = np.where((f_pbest < f_pcurrent)[..., np.newaxis], pbest, X)
        f_pbest = np.where(f_pbest < f_pcurrent, f_pbest, f_pcurrent)
        if f_gbest > f_gcurrent:
            gbest = X[np.argmin(f_pcurrent)]
            f_gbest = f_gcurrent
            print("The swarm updates its collective best performance.")
        if it % 5 == 0:
            plot_contour(X, gbest, f"Iteration t = {it}")
    return gbest, f_gbest


if __name__ == '__main__':
    w = 0.8
    c1, c2 = 0.1, 0.1
    r1, r2 = 0.4, 0.6
    nIter = 25
    X = np.array([
        [5.951, 4.533],
        [3.486, 0.172],
        [4.859, 1.868],
        [3.347, 4.523]
    ])
    V = np.array([
        [-0.653, -0.986],
        [-0.219, 0.412],
        [-0.876, -0.223],
        [0.087, 0.970]
    ])
    (x1, x2), fx = solve(X, V, w, c1, c2, r1, r2, nIter)
    print("Solution: x1 = %.3f, x2 = %.3f, f(x1, x2) = %.3f" % (x1, x2, fx))
