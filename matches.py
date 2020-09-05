import collections
import itertools

from ortools.linear_solver import pywraplp

import data
import metrics
import patches


def cluster_distance(c1, c2):
    return sum(metrics.distances[j1][j2] for j1 in c1 for j2 in c2)


def pair_and_merge(clusters):
    k = len(clusters)
    solver = pywraplp.Solver.CreateSolver("pair_and_merge", "SCIP")
    variables = []
    constraints = [solver.RowConstraint(1, 1, "") for i in range(k)]
    objective = solver.Objective()
    objective.SetMinimization()
    for i1, c1 in enumerate(clusters):
        for i2, c2 in enumerate(clusters):
            if i1 >= i2:
                continue
            variable = solver.BoolVar("")
            variables.append((variable, c1, c2))
            constraints[i1].SetCoefficient(variable, 1)
            constraints[i2].SetCoefficient(variable, 1)
            objective.SetCoefficient(variable, cluster_distance(c1, c2))
    solver_status = solver.Solve()
    assert solver_status == pywraplp.Solver.OPTIMAL
    return [c1 | c2 for (variable, c1, c2) in variables if variable.solution_value()]


def cost_in_shape(perm, cluster_distances, h, w):
    return sum(
        cluster_distances[perm[i * w + j]][perm[(i + 1) * w + j]]
        for i in range(h - 1)
        for j in range(w)
    ) + sum(
        cluster_distances[perm[i * w + j]][perm[i * w + (j + 1)]]
        for i in range(h)
        for j in range(w - 1)
    )


def brute_force(members, cluster_distances, h, w):
    return min(
        itertools.permutations(members),
        key=lambda perm: cost_in_shape(perm, cluster_distances, h, w),
    )


def apply_flips(matrix, flips):
    out_matrix = [[None] * data.width for i in range(data.height)]
    for i in range(data.height):
        for j in range(data.width):
            flip = flips[(i // 4) * 5 + (j // 2)]
            ixor = 3 if flip & 2 else 0
            jxor = flip & 1
            out_matrix[i ^ ixor][j ^ jxor] = matrix[i][j]
    return out_matrix


def initial_matrix():
    if False:
        clusters = [set(patch) for patch in patches.optimize()]
    else:
        clusters = [{i} for i in range(len(data.colors))]
        clusters = pair_and_merge(clusters)
        clusters = pair_and_merge(clusters)
    clusters = pair_and_merge(clusters)
    cluster_distances = [
        [cluster_distance(c1, c2) for c2 in clusters] for c1 in clusters
    ]
    cluster_iterator = (
        brute_force(clusters[i], metrics.distances, 4, 2)
        for i in brute_force(
            range(len(clusters)), cluster_distances, data.height // 4, data.width // 2
        )
    )
    matrix = [[None] * data.width for i in range(data.height)]
    for i in range(0, data.height, 4):
        for j in range(0, data.width, 2):
            c = list(next(cluster_iterator))
            for di in range(4):
                for dj in range(2):
                    matrix[i + di][j + dj] = c[di * 2 + dj]
    return min(
        (
            apply_flips(matrix, flips)
            for flips in itertools.product(
                range(4), repeat=(data.height // 4) * (data.width // 2)
            )
        ),
        key=metrics.objective,
    )
