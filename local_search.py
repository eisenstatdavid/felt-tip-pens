import random

import data
import metrics

vertices = [(i, j) for i in range(data.height) for j in range(data.width)]


def neighbors(u):
    i, j = u
    if i >= 1:
        yield i - 1, j
    if i < data.height - 1:
        yield i + 1, j
    if j >= 1:
        yield i, j - 1
    if j < data.width - 1:
        yield i, j + 1


def at(matrix, u):
    i, j = u
    return matrix[i][j]


def swap(matrix, u, v):
    ui, uj = u
    vi, vj = v
    matrix[ui][uj], matrix[vi][vj] = (matrix[vi][vj], matrix[ui][uj])


def cost_of_swap(matrix, u, v):
    u_costs = metrics.distances[at(matrix, u)]
    u_neigh = [at(matrix, w) for w in neighbors(u) if w != v]
    v_costs = metrics.distances[at(matrix, v)]
    v_neigh = [at(matrix, w) for w in neighbors(v) if w != u]
    old_cost = sum(u_costs[k] for k in u_neigh) + sum(v_costs[k] for k in v_neigh)
    new_cost = sum(u_costs[k] for k in v_neigh) + sum(v_costs[k] for k in u_neigh)
    return new_cost - old_cost


def improve(matrix, rounds):
    for r in range(rounds):
        pairs = [(u, v) for u in vertices for v in vertices if u < v]
        random.shuffle(pairs)
        changed = False
        for u, v in pairs:
            if cost_of_swap(matrix, u, v) < 0:
                swap(matrix, u, v)
                changed = True
        if not changed:
            return