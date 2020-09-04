import colormath.color_objects
import colormath.color_conversions
import colormath.color_diff

import data


_labs = [
    colormath.color_conversions.convert_color(
        colormath.color_objects.sRGBColor.new_from_rgb_hex(color.rgb),
        colormath.color_objects.LabColor,
    )
    for color in data.colors
]
distances = [
    [round(100 * colormath.color_diff.delta_e_cie2000(c1, c2)) for c2 in _labs]
    for c1 in _labs
]


def objective(matrix):
    return sum(
        distances[matrix[i][j]][matrix[i + 1][j]]
        for i in range(data.height - 1)
        for j in range(data.width)
    ) + sum(
        distances[matrix[i][j]][matrix[i][j + 1]]
        for i in range(data.height)
        for j in range(data.width - 1)
    )
