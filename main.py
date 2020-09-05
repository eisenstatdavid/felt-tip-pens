import random

import data
import local_search
import matches
import metrics
import patches


def export(filename, matrix, scale=72):
    with open(filename, "w") as f:
        print(
            '<svg width="{}" height="{}">'.format(
                data.width * scale, data.height * scale
            ),
            file=f,
        )
        for i, row in enumerate(matrix):
            for j, k in enumerate(row):
                print(
                    '<rect x="{}" y="{}" width="{}" height="{}" style="fill:{}" />'.format(
                        j * scale, i * scale, scale, scale, data.colors[k].rgb
                    ),
                    file=f,
                )
        print("</svg>", file=f)


def main():
    if False:
        flattened = list(range(len(data.colors)))
        random.shuffle(flattened)
        matrix = [
            flattened[i * data.width : (i + 1) * data.width] for i in range(data.height)
        ]
    elif False:
        patch_iterator = iter(patches.optimize())
        matrix = [[None] * data.width for i in range(data.height)]
        for i in range(0, data.height, 2):
            for j in range(0, data.width, 2):
                (
                    matrix[i][j],
                    matrix[i][j + 1],
                    matrix[i + 1][j],
                    matrix[i + 1][j + 1],
                ) = next(patch_iterator)
    else:
        matrix = matches.initial_matrix()
    if True:
        print("objective =", metrics.objective(matrix))
        local_search.improve(matrix, 1000)
    print("objective =", metrics.objective(matrix))
    export("arrangement.html", matrix)


if __name__ == "__main__":
    main()
