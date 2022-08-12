# Data parsing code.

import pandas as pd
from datetime import datetime
from train import *

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

### Data import module

# Example : we will do this in iterative way using for loop.
i = 1
# Signal directory.
data_dir = os.path.join(
    download_path
    + "/phyaat_dataset"
    + "/Signals"
    + "/S{0:02d}".format(i)
    + "/S{}_Signals.csv".format(i)
)
# Score directory.
score_dir = os.path.join(
    download_path
    + "/phyaat_dataset"
    + "/Signals"
    + "/S{0:02d}".format(i)
    + "/S{}_Textscore.csv".format(i)
)

# Define datetime format.
dt_parser = lambda x: datetime.strptime(x, "%H:%M:%S:%f")

# Read signal file by panda: set y/m as 1900/01/01.
data = pd.read_csv(
    data_dir, sep=",", parse_dates=["TimeStamp"], date_parser=dt_parser
)

score = pd.read_csv(
    score_dir, sep=",", parse_dates=["TimeStamp"], date_parser=dt_parser
)

###

# Remove -1 and add to list.

###

# Create unique label for each problems // concat TotalW, CorrectW, and dont use score file.

# Find index where problem ends.

# Discontinuity finder function.
def find_disCT(series):

    return True
