import random

import assignment
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


def improve_once(matrix):
    pairs = [(u, v) for u in vertices for v in vertices if u < v]
    random.shuffle(pairs)
    for u, v in pairs:
        if cost_of_swap(matrix, u, v) < 0:
            swap(matrix, u, v)


def random_maximal_independent_set():
    mis = set()
    ranking = vertices[:]
    random.shuffle(ranking)
    for u in ranking:
        if all(v not in mis for v in neighbors(u)):
            mis.add(u)
    return mis


def improve_large_neighborhood_once(matrix):
    moving = random_maximal_independent_set()
    colors = {at(matrix, u) for u in moving}
    cost, matches = assignment.min_cost_assignment(
        moving,
        colors,
        lambda u, k: sum(metrics.distances[k][at(matrix, v)] for v in neighbors(u)),
    )
    for (i, j), k in matches:
        if matrix[i][j] != k:
            matrix[i][j] = k


def improve(matrix, rounds):
    for r in range(rounds):
        improve_once(matrix)
        improve_large_neighborhood_once(matrix)
