import pickle
import numpy as np
import pandas as pd


k_sizes = [3, 4]
problem_sizes = [5, 10, 15, 20, 30, 40, 50]
n_repeats = 10

data_folder = 'results/time_computations'
algorithms = ['backtracking', 'backtracking_forward_checking',
              'backtracking_mac', 'min-conflicts']

flog = {}

cols_n = [['{}_time'.format(alg), '{}_prc_slvd'.format(alg)]
          for alg in algorithms]

cols_n = [c for part in cols_n for c in part]

for size in problem_sizes:
    for k in k_sizes:
        flog['{0:02d}_{1}'.format(size, k)] = {
            c: 0 for c in cols_n
        }
        for alg in algorithms:
            data_n = '{0}/mc_{1}_{2}_{3}.tdat'.format(
                data_folder, size, k, alg
            )
            with open(data_n, 'rb') as f:
                logs = pickle.load(f)
            time_msrs = []
            perc_solved = 0.0
            for r in range(n_repeats):
                time_msrs.append(logs[r]['duration'])
                perc_solved += 1 if logs[r]['solved'] > 0 else 0
            flog['{0:02d}_{1}'.format(size, k)]['{}_time'.format(alg)] = \
                '${0:.4f} \\pm {1:.2f}$'.format(
                    np.mean(time_msrs), np.std(time_msrs)
                )
            flog['{0:02d}_{1}'.format(size, k)]['{}_prc_slvd'.format(alg)] = \
                '{:.2f}'.format((perc_solved / n_repeats) * 100)

dt = pd.DataFrame.from_dict(flog, orient='index')
dt.to_csv('table_of_results.csv')
