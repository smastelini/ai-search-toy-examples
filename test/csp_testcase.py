import sys
import matplotlib.pyplot as plt
sys.path.append('../src/')
# from ais_toy.csp import BacktrackingCSP
# from ais_toy.csp import BacktrackingCSPMAC
from ais_toy.csp import MinConflictsCSP
from ais_toy.problem_generator import random_map_coloring


problem = random_map_coloring(20, 3)
# csp = BacktrackingCSP(**problem)
csp = MinConflictsCSP(**problem)
retr = csp.solve(max_steps=10000)

if retr is None:
    print('No solution was achieved')
    exit()

colors = {
 0: 'red',
 1: 'blue',
 2: 'green',
 3: 'yellow'
}

plt.figure(figsize=(10, 5))
for p, q in problem['C']:
    plt.plot([p[0], q[0]], [p[1], q[1]], 'k-')

for p, c in retr.items():
    plt.scatter(p[0], p[1], c=colors[c])
# plt.legend(fontsize=8)
plt.show()
