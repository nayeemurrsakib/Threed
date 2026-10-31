"""SVG contour and cubic curve helpers; no file writes on import."""
from pathlib import Path
from collections import defaultdict
from xml.sax.saxutils import escape
import json
import shutil
import numpy as np
from PIL import Image

def contours(mask):
    edges = defaultdict(list)
    padded = np.pad(mask, 1)
    (ys, xs) = np.where(mask)
    for (y, x) in zip(ys.tolist(), xs.tolist()):
        if not padded[y, x + 1]:
            edges[x, y].append((x + 1, y))
        if not padded[y + 1, x + 2]:
            edges[x + 1, y].append((x + 1, y + 1))
        if not padded[y + 2, x + 1]:
            edges[x + 1, y + 1].append((x, y + 1))
        if not padded[y + 1, x]:
            edges[x, y + 1].append((x, y))
    paths = []
    direction = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}
    while edges:
        start = next(iter(edges))
        point = start
        loop = [point]
        previous = None
        while True:
            options = edges[point]
            if previous is None or len(options) == 1:
                following = options[0]
            else:
                incoming = direction[point[0] - previous[0], point[1] - previous[1]]
                priority = {1: 0, 0: 1, 3: 2, 2: 3}
                following = min(options, key=lambda q: priority[(direction[q[0] - point[0], q[1] - point[1]] - incoming) % 4])
            options.remove(following)
            if not options:
                del edges[point]
            (previous, point) = (point, following)
            loop.append(point)
            if point == start:
                break
        if len(loop) > 20:
            p = np.array(loop[:-1], dtype=float)
            kernel = (1, 2, 3, 4, 3, 2, 1)
            smooth = sum((np.roll(p, i - 3, axis=0) * weight for (i, weight) in enumerate(kernel))) / 16
            paths.append(smooth.tolist())
    return paths

def unit(v):
    length = np.linalg.norm(v)
    return v / length if length > 1e-10 else np.array([1.0, 0.0])

def fit(points, left, right, tolerance=0.65):
    p = np.asarray(points)
    distance = np.linalg.norm(p[-1] - p[0])
    if len(p) == 2:
        return [(p[0], p[0] + left * distance / 3, p[-1] + right * distance / 3, p[-1])]
    u = np.insert(np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1)), 0, 0)
    u /= u[-1]
    b0 = (1 - u) ** 3
    b1 = 3 * u * (1 - u) ** 2
    b2 = 3 * u * u * (1 - u)
    b3 = u ** 3
    a1 = b1[:, None] * left
    a2 = b2[:, None] * right
    residual = p - (b0 + b1)[:, None] * p[0] - (b2 + b3)[:, None] * p[-1]
    c = np.array([[np.sum(a1 * a1), np.sum(a1 * a2)], [np.sum(a1 * a2), np.sum(a2 * a2)]])
    x = np.array([np.sum(a1 * residual), np.sum(a2 * residual)])
    try:
        alpha = np.linalg.solve(c, x)
    except np.linalg.LinAlgError:
        alpha = np.array([distance / 3, distance / 3])
    if np.min(alpha) < distance * 1e-06:
        alpha = np.array([distance / 3, distance / 3])
    curve = (p[0], p[0] + left * alpha[0], p[-1] + right * alpha[1], p[-1])
    estimate = b0[:, None] * curve[0] + b1[:, None] * curve[1] + b2[:, None] * curve[2] + b3[:, None] * curve[3]
    errors = np.sum((estimate - p) ** 2, axis=1)
    split = int(np.argmax(errors))
    if errors[split] < tolerance * tolerance:
        return [curve]
    split = max(1, min(len(p) - 2, split))
    tangent = unit(p[split - 1] - p[split + 1])
    return fit(p[:split + 1], left, tangent, tolerance) + fit(p[split:], -tangent, right, tolerance)

def outline(loops, xoff, yoff):
    result = []
    for points in loops:
        p = np.array(points) - np.array([xoff, yoff])
        split = int(np.argmax(np.sum((p - p[0]) ** 2, axis=1)))
        start = unit(p[1] - p[-1])
        end = unit(p[split + 1] - p[split - 1])
        first = fit(p[:split + 1], start, -end)
        second = fit(np.vstack((p[split:], p[:1])), end, -start)

        def xy(p):
            return f'{p[0]:.2f} {p[1]:.2f}'
        result.append('M' + xy(p[0]))
        for (_, c1, c2, last) in first + second:
            result.append('C' + xy(c1) + ' ' + xy(c2) + ' ' + xy(last))
        result.append('Z')
    return ''.join(result)
