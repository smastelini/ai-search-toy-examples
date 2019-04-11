import sys
sys.path.append('../src/')

from ais_toy.problem_generator import random_map_coloring


if __name__ == '__main__':
    X, D, C = random_map_coloring(5, 3)
    print(X)
    print(D)
    print(C)
    print()
    print()

    print(constraints2graph(C))
