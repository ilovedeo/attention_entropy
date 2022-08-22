# Main training code.
import os
from data_preprocess import *
import numpy as np
import natsort
from util import *

# Data parse.
here = os.path.dirname(os.path.abspath(__file__))
if not (
    os.path.isdir(
        os.path.join(here + "\\train" + "\\datasets" + "\\data" + "\\episode_parsed")
    )
):
    parsing(here)

input("Press enter to continue...")

# Data visualization.



# In case of the loop
# for i in range(25):
#     # needs modulization.
#     # Load data.
#     temp = np.load("train\\datasets\\data\\episode_parsed\\S{0:02d}\\S{0:02d}.npz".format(i+1))
#     list = natsort.natsorted(temp.files)

# pre-loop test
i = 1
# Data load: temp is a list of the episode of a given subject.
temp = np.load(
    "train\\datasets\\data\\episode_parsed\\S{0:02d}\\S{0:02d}.npz".format(i + 1)
)
### Needs to print the number of the subject.
# Make list safely by natsort, list: "arr_#".
list = natsort.natsorted(temp.files)

### Needs to print the number of the subject.
# Print the total number of the episode.
print("Total number of the episode: {}".format(len(list)))

# Create empty list to store the value.
entropy_list = []

# Make a long list that ...
for i, item in enumerate(list):
    # Print subject number and total number of episodes.
    # print("Episode: {}".format(int(item[4:])))

    # Store header.
    if i == 0:
        # 20: Label Noise level, 21: Label Semantic, 22: Label Task, 24: TotalW, 25: CorrectWords.
        header = [
            "MMSE",
            "length_second",
            temp[item][20],
            temp[item][21],
            temp[item][22],
            temp[item][24],
            temp[item][25],
        ]
        data = pd.DataFrame(columns=header)

    # Store the rest state EEG signal data.
    elif i == 1:
        print(temp[item].shape)
        EEG = temp[item][:, 0:14]
        ent = MMSE(EEG, 2, 0.25, 0)
        # sampling rate: 128Hz
        time = temp[item].shape[0] / 128
        append = [ent, time, temp[item][0, 20], temp[item][0, 21], temp[item][0, 22], -1, -1]
        temp = pd.DataFrame([append], columns=header)
        data = pd.concat([data, temp], ignore_index=True)

    # Store the EEG data.
    else:
        print(temp[item].shape)
        EEG = temp[item][:, 0:14]
        ent = MMSE(EEG, 2, 0.25, 0)
        # sampling rate: 128Hz
        time = temp[item].shape[0] / 128
        append = [
            ent,
            time,
            temp[item][0, 20],
            temp[item][0, 21],
            temp[item][0, 22],
            temp[item][0, 24],
            temp[item][0, 25],
        ]
        temp = pd.DataFrame([append], columns=header)
        data = pd.concat([data, temp], ignore_index=True)
