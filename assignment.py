import collections

from ortools.graph import pywrapgraph


def min_cost_assignment(lefts, rights, cost_function):
    if not isinstance(lefts, collections.Sequence):
        lefts = list(lefts)
    if not isinstance(rights, collections.Sequence):
        rights = list(rights)
    assignment = pywrapgraph.LinearSumAssignment()
    for i, left in enumerate(lefts):
        for j, right in enumerate(rights):
            assignment.AddArcWithCost(i, j, cost_function(left, right))
    solve_status = assignment.Solve()
    assert solve_status == assignment.OPTIMAL
    return (
        assignment.OptimalCost(),
        [(left, rights[assignment.RightMate(i)]) for (i, left) in enumerate(lefts)],
    )
