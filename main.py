import data
import metrics


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
    matrix = [
        list(range(i * data.width, (i + 1) * data.width)) for i in range(data.height)
    ]
    print("objective =", metrics.objective(matrix))
    export("arrangement.html", matrix)


if __name__ == "__main__":
    main()
