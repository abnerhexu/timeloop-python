import sympy


def lambdify(d, tile_shapes):
    if isinstance(next(iter(d.values())), tuple):
        return {
            k: (v[0], sympy.lambdify(tile_shapes, v[1]))
            for k, v in d.items()
        }
    else:
        return {
            k: sympy.lambdify(tile_shapes, v)
            for k, v in d.items()
        }
