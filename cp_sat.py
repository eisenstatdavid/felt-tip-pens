from ortools.sat.python import cp_model

import data
import metrics


def optimize():
    n = len(data.colors)
    allowed_assignments = {
        (i, j)
        for i in range(n)
        for j in sorted(range(n), key=lambda k: metrics.distances[i][k])[1:12]
    }
    allowed_assignments.update([(j, i) for (i, j) in allowed_assignments])

    model = cp_model.CpModel()
    variables = [model.NewIntVar(0, n - 1, "") for i in range(n)]
    model.AddAllDifferent(variables)
    edges = []
    for i in range(data.height):
        for j in range(data.width - 1):
            edges.append((i * data.width + j, i * data.width + (j + 1)))
    for i in range(data.height - 1):
        for j in range(data.width):
            edges.append((i * data.width + j, (i + 1) * data.width + j))
    for i, j in edges:
        model.AddAllowedAssignments((variables[i], variables[j]), allowed_assignments)

    solver = cp_model.CpSolver()
    solver.Solve(model)
    return [
        [solver.Value(variables[i * data.width + j]) for j in range(data.width)]
        for i in range(data.height)
    ]
