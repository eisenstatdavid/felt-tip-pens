import data
import metrics

n = len(metrics.distances)
edges = sorted(
    (metrics.distances[i][j], i, j) for i in range(n) for j in range(n) if i < j
)
parents = {}
print("graph {")
print('node [style="filled"]')
for i, color in enumerate(data.colors):
    print('{} [fillcolor="{}"]'.format(i, color.rgb))
for cost, i, j in edges:
    ri = i
    while ri in parents:
        ri = parents[ri]
    rj = j
    while rj in parents:
        rj = parents[rj]
    if ri != rj:
        parents[max(ri, rj)] = min(ri, rj)
        print("{} -- {}".format(i, j))
print("}")
