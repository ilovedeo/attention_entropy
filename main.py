# Main training code.
import os
from data_preprocess import *
import numpy as np
import natsort

# Data parse.
here = os.path.dirname(os.path.abspath(__file__))
if not (
    os.path.isdir(
        os.path.join(here + "\\train" + "\\datasets" + "\\data" + "\\episode_parsed")
    )
):
    parsing(here)

input("Press enter to continue...")

# Load data.
temp = np.load("train\\datasets\\data\\episode_parsed\\S01\\S01.npz")
# Make list safely by natsort, list: "arr_#".
list = natsort.natsorted(temp.files)

for i, item in enumerate(list):
    # Print subject number and total number of episodes.


    if i == 0:
        print(temp[item])
        print(temp[item].shape)
        print(item)
    elif i == 1:
        print(temp[item].shape)