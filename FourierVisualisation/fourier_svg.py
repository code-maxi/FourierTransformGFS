import numpy as np
from svgpathtools import svg2paths, parse_path

def pos_to_tuple(p: complex): return p.real, p.imag

def mirror_y(p: complex): return p.real - p.imag*1j

def get_svg_points(name: str, precision: int, size: float):
    path = svg2paths(name)[0][0]
    points = [mirror_y(path.point(t / precision)) for t in range(precision+1)]
    minx, maxx = np.inf, -np.inf
    miny, maxy = np.inf, -np.inf
    for p in points:
        if p.real < minx: minx = p.real
        if p.imag < miny: miny = p.imag
        if p.real > maxx: maxx = p.real
        if p.imag > maxy: maxy = p.imag
    print('x', minx, maxx)
    print('y', miny, maxy)
    scale = min(size/(maxx - minx), size/(maxy - miny))
    return [(p - (minx + maxx)/2 - (miny + maxy)/2 * 1j) * scale for p in points]
