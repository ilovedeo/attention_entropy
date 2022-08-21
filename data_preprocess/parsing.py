# Data parsing code.

import os
import pandas as pd
import phyaat
import numpy as np
from tqdm import tqdm

# File download and rename.
# download_path: ./attention_entropy/train/datasets/data
def rename_file(download_path):
    if not os.path.isdir(download_path):
        os.mkdir(download_path)
        dirPath = phyaat.download_data(
            baseDir=download_path, subject=-1, verbose=0, overwrite=False
        )

    data_path = os.path.join(download_path + "/phyaat_dataset" + "/Signals")
    file_list = sorted([i for i in os.listdir(data_path) if i[0] == "S"])
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
            print("Original filename: ")
            print(org_filename)
            print("Revised filename: ")
            print(dst_filename)
            os.rename(org_filename, dst_filename)


# Discontinuity finder function:
# returns a chunk of index list // separated by discontinuity.
def find_disCT(data, col_name):
    # Initial conditions
    # A set of intervals
    disCT_list = []
    # Subintervals
    interval = []
    function = data[col_name].to_numpy()
    # Start value with first value of the function.
    value = function[0]
    for i in range(len(function)):
        # Final condition.
        if i == (len(function) - 1):
            interval += [i]
            disCT_list += [interval]

        # If matches : continuous.
        elif function[i] == value:
            interval += [i]

        # In the case of discontinuity.
        else:
            disCT_list += [interval]
            interval = [i]
            value = function[i]

    return disCT_list


# Define a mapper function.
def mapper(data, score, intervals, new_index):
    episode_list = []
    for i, itv in enumerate(intervals):

        # Initial experiment condition : rest state.
        if i == 0:
            save = data.loc[itv]
            episode_list += [save.to_numpy()]

        # 3 episodes are assigned to 1 score.
        else:
            score_idx = (i - 1) // 3
            save = data.loc[itv]
            save[new_index] = score[new_index].loc[score_idx]
            episode_list += [save.to_numpy()]

    return episode_list, list(save.columns)

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
def parsing(here):
    # Data download path.
    download_path = os.path.join(here + "/train" + "/datasets" + "/data")

    # First make directory to store data
    parsed_dir = os.path.join(download_path + "/episode_parsed")
    if os.path.isdir(parsed_dir):
        return None

    # First make directory to store data
    os.mkdir(parsed_dir)

    # Rename file.
    rename_file(download_path)

    # create data path list
    data_path = os.path.join(download_path + "/phyaat_dataset" + "/Signals")
    file_list = sorted([i for i in os.listdir(data_path) if i[0] == "S"])

    for i, dir in enumerate(tqdm(file_list)):
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

        # Define columns to reject TimeStamp.
        data_cols = list(pd.read_csv(data_dir, nrows=1))
        score_cols = list(pd.read_csv(score_dir, nrows=1))

        # Read signal and score file.
        data = pd.read_csv(
            data_dir, sep=",", usecols=[i for i in data_cols if i != "TimeStamp"]
        )

        score = pd.read_csv(
            score_dir, sep=",", usecols=[i for i in score_cols if i != "TimeStamp"]
        )

        # Create discontinuous interval list: if the task index is changed,
        # then we store the data and load a new task.
        intervals = find_disCT(data, "Label_T")

        # Add "TotalW", "CorrectWords"
        new_index = ["TotalW", "CorrectWords"]

        # Create episode list.
        episode_list, header = mapper(data, score, intervals, new_index)

        # And then store header.
        episode_list.insert(0, header)

        # Make destination directory.
        subject_dir = os.path.join(parsed_dir + "/S{0:02d}".format(subject))
        if not os.path.isdir(subject_dir):
            os.mkdir(subject_dir)

        # And, save
        np.savez(subject_dir + "/S{0:02d}.npz".format(subject), *episode_list)

