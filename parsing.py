# Data parsing code.

import pandas as pd
from datetime import datetime
from train import *
import numpy as np

# here: current directory.
here = os.getcwd()
# Data download path.
download_path = os.path.join(here + "/train" + "/datasets" + "/data")

# Rename file.
rename_file(download_path)

#################################################################################
# Parse the data.
# EEG: [AF3, F7, F3, FC5, T7, P7, O1, O2, P8, T8, FC6, F4, F8, AF4],
# PPG,
# BPM: Pulse Rate in Beats per minutes,
# IBI: Inter Beat Interval,
# gsrRAW: Instantaneous GSR Signal,
# gsrLPF: Lowpass GSR Signals (Moving averaged of past 100 samples),
# Label_N: Noise Levels [-6,-3,0,3,6,1000] dB,
# Label_S: Semanticity Label where 0-Semantic, 1-Non-semantic,
# Label_T: Task where 0-Listenting, 1-Writing, 2-Resting,
# CaseID : CaseID An identyfier code for experimental condition,
# encoded value of noise level and semanticity
#################################################################################

### Data import and store module.
# First make directory to store data
parsed_dir = os.path.join(download_path + "/episode_parsed")
if not os.path.isdir(parsed_dir):
    os.mkdir(parsed_dir)

# Example : we will do this in iterative way using for loop.
# for i in dir...
i = 0
subject = i + 1
# Signal directory.
data_dir = os.path.join(
    download_path
    + "/phyaat_dataset"
    + "/Signals"
    + "/S{0:02d}".format(subject)
    + "/S{}_Signals.csv".format(subject)
)
# Score directory.
score_dir = os.path.join(
    download_path
    + "/phyaat_dataset"
    + "/Signals"
    + "/S{0:02d}".format(subject)
    + "/S{}_Textscore.csv".format(subject)
)

# Make destination directory.
subject_dir = os.path.join(parsed_dir + "/S{0:02d}".format(subject))
if not os.path.isdir(subject_dir):
    os.mkdir(subject_dir)

# Define columns to reject TimeStamp.
data_cols = list(pd.read_csv(data_dir, nrows=1))
score_cols = list(pd.read_csv(score_dir, nrows=1))

# Read signal file by panda: set y/m as 1900/01/01.
data = pd.read_csv(
    data_dir, sep=",", usecols=[i for i in data_cols if i != "TimeStamp"]
)

score = pd.read_csv(
    score_dir, sep=",", usecols=[i for i in score_cols if i != "TimeStamp"]
)

###
# Create discontinuous interval list.
intervals = find_disCT(data, "Label_T")

###
# Add score:
# Create dataframe with 3 columns.
task_list = []
# Add "TotalW", "CorrectWords"
new_index = ["TotalW", "CorrectWords"]
add_data = pd.dataframe()


###
# Define a mapper function.
def mapper(data, score, intervals, new_index):
    for i, itv in enumerate(intervals):
        store = data.loc[itv]
        # Initial experiment condition
        if i == 0:


        else:
            for col_name in new_index:
                dataframe[col_name] = val_list[i]

    return data

###
# And then store header for first subject.
if subject == 1:
    cols = list(pd.read_csv(data_dir, nrows=1))
    task_list += [cols]

###
# Remove -1 and add to list.
rest_index = list(data[data["Label_T"] < 0].index)
des_data, sep_data = separator(data, rest_index, axis=0)

###
# Create unique label for each problems // concat TotalW, CorrectW, and dont use score file.

# Find index where problem ends.


