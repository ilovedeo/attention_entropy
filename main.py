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

# In case of the loop
# for i in range(25):
#     # needs modulization.
#     # Load data.
#     temp = np.load("train\\datasets\\data\\episode_parsed\\S{0:02d}\\S{0:02d}.npz".format(i+1))
#     list = natsort.natsorted(temp.files)

# pre-loop test
i = 1
# data load
temp = np.load(
    "train\\datasets\\data\\episode_parsed\\S{0:02d}\\S{0:02d}.npz".format(i + 1)
)
### Needs to print the number of the subject.
# Make list safely by natsort, list: "arr_#".
list = natsort.natsorted(temp.files)

### Needs to print the number of the subject.
# Print the total number of the episode.
print("Total number of the episode: {}".format(len(list)))

# Make a long list that ...
for i, item in enumerate(list):
    # Print subject number and total number of episodes.
    # print("Episode: {}".format(int(item[4:])))

    # Data header.
    if i == 0:
        print("header: ")
        print(temp[item])
        eeg_probe = temp[item][0:14]

    # Rest state EEG signal data.
    elif i == 1:
        print(temp[item].shape)

    # Store the EEG data
    # else:
