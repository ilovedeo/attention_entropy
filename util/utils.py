# Useful functions.

import numpy as np


# A function to calculate sample entropy.
def SampEnA(U, m, r, axis):

    # N is a length of the series.
    N = U.shape[axis]

    # Metric function.
    def _maxdist(xi, xj):
        return abs(xi - xj).max(axis=axis)

    # Split data and create window list.
    # Joint entropy condition : H(X, Y), count N - m vectors.
    def _split_joint(m):
        return np.stack(
            [np.take(U, range(i, N - m + i), axis=axis) for i in range(m + 1)],
            axis=axis + 1,
        )

    # Given entropy condition : H(Y), count N - m vectors.
    def _split_given(m):
        return np.stack(
            [np.take(U, range(i, N - m + i), axis=axis) for i in range(m)],
            axis=axis + 1,
        )

    # Calculate joint entropy.
    def _phi_joint(m):
        x2 = _split_joint(m)
        L = x2.shape[axis]
        sum_ = 0
        for i in range(L):
            for j in range(L):
                sum_ = sum_ + 1 * (
                    _maxdist(np.take(x2, i, axis=axis), np.take(x2, j, axis=axis)) <= r
                )
        # (sum_ - L): Ignore the self counting to reduce bias.
        return (sum_ - L) / ((N - m) * (N - m - 1.0))

    def _phi_given(m):
        x1 = _split_given(m)
        L = x1.shape[axis]
        sum_ = 0
        for i in range(L):
            for j in range(L):
                sum_ = sum_ + 1 * (
                    _maxdist(np.take(x1, i, axis=axis), np.take(x1, j, axis=axis)) <= r
                )
        return (sum_ - L) / ((N - m) * (N - m - 1.0))

    if _phi_joint(m) == 0:
        return np.inf

    else:
        out = -np.log(_phi_joint(m) / _phi_given(m))
        return out
