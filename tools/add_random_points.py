#!/usr/bin/env python3

"""
Add random deviation points to polygon boundaries in a GeoJSON file.

This is a Python translation of tools/add_random_points.php.
"""

from __future__ import annotations

import json
import math
import random
import sys
from typing import Dict, List, Tuple


MAX_DEVIATION = 0.2
MAX_ABS = 0.02
MIN_DISTANCE = 0.05
ITERATIONS = 4


Point = List[float]
Lookup = Dict[str, Point]


def clamp(value: float, low: float, high: float) -> float:
    return max(min(value, high), low)


def point_id(point: Point) -> str:
    return f"{point[0]}-{point[1]}"


def process_points(points: List[Point], lookup: Lookup) -> List[Point]:
    prev: Point | None = None
    new_points: List[Point] = []

    for point in points:
        if prev is not None:
            distance = math.sqrt((prev[0] - point[0]) ** 2 + (prev[1] - point[1]) ** 2)
            if distance != 0 and distance > MIN_DISTANCE:
                id_a = point_id(prev)
                id_b = point_id(point)
                edge_key = f"{id_a}--{id_b}"
                reverse_key = f"{id_b}--{id_a}"

                if edge_key in lookup:
                    new_points.append(lookup[edge_key])
                elif reverse_key in lookup:
                    new_points.append(lookup[reverse_key])
                else:
                    x = (prev[0] + point[0]) / 2.0
                    y = (prev[1] + point[1]) / 2.0

                    r = random.random()  # 0-1
                    r = (r + 1) / 2  # 0.5-1.0

                    # If dx=x2-x1 and dy=y2-y1, normals are (-dy, dx) and (dy, -dx).
                    dx = point[0] - x
                    dy = point[1] - y

                    if random.random() < 0.5:
                        x_off = -dy
                        y_off = dx
                    else:
                        x_off = dy
                        y_off = -dx

                    x_off *= r * MAX_DEVIATION
                    x_off = clamp(x_off, -MAX_ABS, MAX_ABS)

                    y_off *= r * MAX_DEVIATION
                    y_off = clamp(y_off, -MAX_ABS, MAX_ABS)

                    p = [x + x_off, y + y_off]
                    lookup[edge_key] = p
                    new_points.append(p)

        new_points.append(point)
        prev = point

    return new_points


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: add_random_points.py <filename.json>", file=sys.stderr)
        return 1

    filename = sys.argv[1]
    with open(filename, "r", encoding="utf-8") as f:
        cells = json.load(f)

    for _ in range(ITERATIONS):
        lookup: Lookup = {}

        for cell in cells.get("features", []):
            points = cell["geometry"]["coordinates"][0]
            cell["geometry"]["coordinates"][0] = process_points(points, lookup)

    print(json.dumps(cells, indent=4))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
