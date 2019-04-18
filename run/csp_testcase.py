import os
import sys
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('../src/')
from ais_toy.csp import BacktrackingCSP
from ais_toy.csp import BacktrackingCSPMAC
from ais_toy.csp import MinConflictsCSP
from ais_toy.problem_generator import random_map_coloring


def plot_solution_and_save(problem, solution, method_n, n_points, k, path):
    colors = {
     0: 'red',
     1: 'blue',
     2: 'green',
     3: 'purple',
    }

    plt.figure(figsize=(8, 8))
    for p, q in problem['C']:
        plt.plot([p[0], q[0]], [p[1], q[1]], 'k-', linewidth=0.5, zorder=1)

    for p, c in solution.items():
        plt.scatter(p[0], p[1], c=colors[c], zorder=2)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Map coloring ({0}): {1} x {2}'.format(method_n, n_points, k))
    plt.savefig('{0}/map_coloring_{1}_{2}_{3}.eps'.format(
        path, n_points, k, method_n.lower().replace(' ', '_')
    ))


def solve_and_compute(method_n, method, problem, max_steps):
    np.random.seed(None)
    seed = np.random.get_state()
    csp = method(**problem)

    if method_n == 'Min Conflicts':
        start = time.time()
        solution = csp.solve(max_steps=max_steps)
        end = time.time()
    else:
        start = time.time()
        solution = csp.solve()
        end = time.time()

    t_time = end - start

    return t_time, solution, seed


def check_and_solve(k_sizes, problem_sizes, n_repeats=30, max_steps=10000,
                    output_path='./results'):

    rep_seeds = np.random.randint(low=0, high=9999, size=n_repeats).tolist()
    time_logs = '{0}/time_computations'.format(output_path)
    plot_logs = '{0}/plots'.format(output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        os.makedirs(time_logs)
        os.makedirs(plot_logs)

    solvers = {
        'Backtracking AC-3': BacktrackingCSP,
        'Backtracking MAC': BacktrackingCSPMAC,
        'Min Conflicts': MinConflictsCSP
    }

    for k in k_sizes:
        for size in problem_sizes:
            for solver_n, solver in solvers.items():
                log_name = '{0}/mc_{1}_{2}_{3}.tdat'.format(
                    time_logs, size, k, solver_n.lower().replace(' ', '_')
                )

                log_exists = os.path.isfile(log_name)
                if not log_exists:
                    tlog = {}
                else:
                    with open(log_name, 'rb') as f:
                        tlog = pickle.load(f)

                plot_saved = False
                for r in range(n_repeats):
                    if r in tlog:
                        continue
                    np.random.seed(rep_seeds[r])
                    problem = random_map_coloring(size, k)

                    t_time, solution, seed = solve_and_compute(
                        solver_n, solver, problem, max_steps
                    )

                    if solution is not None and not plot_saved:
                        plot_solution_and_save(
                            problem, solution, solver_n, size, k, plot_logs
                        )
                        plot_saved = True

                    d = {}
                    d['duration'] = t_time
                    d['solved'] = 1 if solution is not None else -1
                    d['seed'] = seed

                    tlog[r] = d
                    with open(log_name, 'wb') as f:
                        pickle.dump(obj=tlog, file=f, protocol=-1)

                f.close()


np.random.seed(2019)
k_sizes = [3, 4]
problem_sizes = [10, 20, 30, 40, 50, 70, 100, 150, 200, 500, 1000]


if __name__ == '__main__':
    check_and_solve(k_sizes, problem_sizes)