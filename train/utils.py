# Useful functions.

import os
import numpy as np
import phyaat

# File download and rename.
# download_path: ./attention_entropy/train/datasets/data
def rename_file(download_path):
    if not os.path.isdir(download_path):
        dirPath = phyaat.download_data(
            baseDir=download_path, subject=-1, verbose=0, overwrite=False
        )

    data_path = os.path.join(download_path + "/phyaat_dataset" + "/Signals")
    file_list = os.listdir(data_path)
    for dir in file_list:
        FilePath = os.path.join(data_path, dir)
        # Decide whether FilePath is a directory.
        if os.path.isdir(FilePath):
            # Original file directory
            org_filename = os.path.join(data_path + "/" + dir)
            # New filename
            dst_filename = os.path.join(
                data_path + "/" + dir[0] + "{0:02d}".format(int(dir[1:]))
            )
            print("Original filename")
            print(org_filename)
            print("Revised filename")
            print(dst_filename)
            os.rename(org_filename, dst_filename)


# Needs to be revised...
def SampEnA(U, m, r, axis):
    def _maxdist(xi, xj):
        return abs(xi - xj).max(axis=axis)
    def _split(m):
        return np.stack([np.take(U, range(i, N - m + 1 + i), axis=axis) for i in range(m)], axis=axis + 1)
    def _phi(m):
        x1 = _split(m)
        L = x1.shape[axis]
        sum_ = 0
        for i in range(L):
            for j in range(L):
                sum_ = sum_ + 1 * (_maxdist(np.take(x1, i, axis=axis), np.take(x1, j, axis=axis)) <= r)
        return (sum_ - L) / (N - m) * (N - m + 1.0) ** (-1)
    N = U.shape[axis]
    out = -np.log(_phi(m + 1) / _phi(m))
    out[np.where(np.isnan(out))] = 0
    return out