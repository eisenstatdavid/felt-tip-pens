import collections
import itertools

from ortools.linear_solver import pywraplp

import data
import metrics


def optimize():
    patches = []
    for i, j, k, l in itertools.combinations(range(len(data.colors)), 4):
        patches.append((i, j, k, l))
        patches.append((i, j, l, k))
    costs = [
        (
            metrics.distances[i][j]
            + metrics.distances[i][k]
            + metrics.distances[j][l]
            + metrics.distances[k][l],
            (i, j, k, l),
        )
        for (i, j, k, l) in patches
    ]
    costs.sort()
    del costs[len(costs) // 50 :]

    solver = pywraplp.Solver.CreateSolver("patches", "SCIP")
    variables = []
    constraints = collections.defaultdict(lambda: solver.RowConstraint(1, 1, ""))
    objective = solver.Objective()
    objective.SetMinimization()
    for cost, patch in costs:
        variable = solver.BoolVar(",".join(map(str, patch)))
        variables.append((variable, patch))
        for i in patch:
            constraints[i].SetCoefficient(variable, 1)
        objective.SetCoefficient(variable, cost)
    print("Solving...")
    solver_status = solver.Solve()
    assert solver_status == pywraplp.Solver.OPTIMAL
    print("MIP objective =", objective.Value())
    selected_patches = set()
    for variable, patch in variables:
        if variable.solution_value():
            selected_patches.add(patch)
    return selected_patches
