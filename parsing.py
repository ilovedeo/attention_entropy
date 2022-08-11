# Data parsing code.

import os
import phyaat # Download phyaat library by command: "pip install phyaat".
import pandas as pd

# here: current directory.
here = os.getcwd()

# data_path: parent directory.
def rename_file(download_path):
    if not os.path.isdir(download_path):
        dirPath = phyaat.download_data(baseDir=download_path, subject=-1, verbose=0, overwrite=False)

    data_path =  os.path.join(download_path + "/phyaat_dataset" + "/Signals")
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

# Rename file.
# Download phyaat library by command: "pip install phyaat".
download_path = os.path.join(here + "/train" + "/datasets" + "/data")
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


# Example : we will do this in iterative way using for loop.
i = 1
# Signal directory.
data_dir = os.path.join(
    data_path + "/S{0:02d}".format(i) + "/S{}_Signals.csv".format(i)
)
# Score directory.
score_dir = os.path.join(
    data_path + "/S{0:02d}".format(i) + "/S{}_Textscore.csv".format(i)
)

# Read signal file by panda.
data = pd.read_csv(data_dir)
score = pd.read_csv(score_dir)

print(data.shape)
print(score.shape)
