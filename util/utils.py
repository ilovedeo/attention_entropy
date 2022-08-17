# Useful functions.

import numpy as np


# Needs to be revised...
def SampEnA(U, m, r, axis):

    # N is a length of the series.
    N = U.shape[axis]

    # Metric function.
    def _maxdist(xi, xj):
        return abs(xi - xj).max(axis=axis)

    # Split data and create window list.
    def _split(m):
        return np.stack(
            [np.take(U, range(i, N - m + 1 + i), axis=axis) for i in range(m)],
            axis=axis + 1,
        )

    def _phi(m):
        x1 = _split(m)
        L = x1.shape[axis]
        sum_ = 0
        for i in range(L):
            for j in range(L):
                sum_ = sum_ + 1 * (
                        _maxdist(np.take(x1, i, axis=axis), np.take(x1, j, axis=axis)) <= r
                )
        return (sum_ - L) / (N - m) * (N - m + 1.0) ** (-1)

    out = -np.log(_phi(m + 1) / _phi(m))
    try:
        out[np.where(np.isnan(out))] = 0
    except: pass

    return out
