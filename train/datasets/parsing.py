# Store current directory.
import os
import pandas as pd


# data_path: parent directory, file_list: name list of files in parent directory.
def rename_file(data_path, file_list):
    for dir in file_list:
        FilePath = os.path.join(data_path, dir)
        # Decide whether FilePath is a directory.
        if os.path.isdir(FilePath):
            # Original file directory
            org_filename = os.path.join(data_path + "/" + dir)
            # New filoename
            dst_filename = os.path.join(
                data_path + "/" + dir[0] + "{0:02d}".format(int(dir[1:]))
            )
            os.rename(org_filename, dst_filename)


# Rename file.
# here: currnet directory
here = os.getcwd()
# Create file list.
data_path = os.path.join(here + "/data" + "/phyaat_dataset" + "/Signals")
file_list = os.listdir(data_path)
rename_file(data_path, file_list)

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


# Example : we will do this in iterative way using for loop.
i = 1
# Signal directory.
data_dir = os.path.join(
    here
    + "/data"
    + "/phyaat_dataset"
    + "/Signals"
    + "/S{0:02d}".format(i)
    + "/S{}_Signals.csv".format(i)
)
score_dir = os.path.join(
    here
    + "/data"
    + "/phyaat_dataset"
    + "/Signals"
    + "/S{0:02d}".format(i)
    + "/S{}_Textscore.csv".format(i)
)

# Read signal file by panda.
data = pd.read_csv(data_dir)
score = pd.read_csv(score_dir)

print(data.shape)
print(score.shape)
