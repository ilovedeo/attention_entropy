# Data parsing code.

import os
import pandas as pd
import phyaat
import numpy as np
from tqdm import tqdm
import natsort
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util import *

# File download and rename.
# download_path: ./attention_entropy/train/datasets/data
def rename_file(download_path):
    if not os.path.isdir(download_path):
        os.mkdir(download_path)
        dirPath = phyaat.download_data(
            baseDir=download_path, subject=-1, verbose=0, overwrite=False
        )

    data_path = os.path.join(download_path + r"/phyaat_dataset" + r"/Signals")
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
# Normalize data and save chunks of data by given intervals.
def mapper(data, score, intervals, new_index):
    # EEG data normalization.
    header = list(data.columns) + new_index
    # Get EEG header and normalize.
    EEG_list = header[0:14]
    for channel in EEG_list:
        data[channel] = (data[channel] - data[channel].mean()) / data[channel].std()

    # Data chunking.
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
    download_path = os.path.join(here + r"/train" + r"/datasets" + r"/data")

    # First make directory to store data
    parsed_dir = os.path.join(download_path + r"/episode_parsed")
    if os.path.isdir(parsed_dir):
        return None

    # First make directory to store data
    os.mkdir(parsed_dir)

    # Rename file.
    rename_file(download_path)

    # create data path list
    data_path = os.path.join(download_path + r"/phyaat_dataset" + r"/Signals")
    file_list = sorted([i for i in os.listdir(data_path) if i[0] == "S"])

    for i, dir in enumerate(tqdm(file_list)):
        subject = i + 1
        # Signal directory.
        data_dir = os.path.join(
            download_path
            + r"/phyaat_dataset"
            + r"/Signals"
            + r"/S{0:02d}".format(subject)
            + r"/S{}_Signals.csv".format(subject)
        )
        # Score directory.
        score_dir = os.path.join(
            download_path
            + r"/phyaat_dataset"
            + r"/Signals"
            + r"/S{0:02d}".format(subject)
            + r"/S{}_Textscore.csv".format(subject)
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

        # Data normalize and create episode list.
        episode_list, header = mapper(data, score, intervals, new_index)

        # And then store header.
        episode_list.insert(0, header)

        # Make destination directory.
        subject_dir = os.path.join(parsed_dir + r"/S{0:02d}".format(subject))
        if not os.path.isdir(subject_dir):
            os.mkdir(subject_dir)

        # And, save
        np.savez(subject_dir + r"/S{0:02d}.npz".format(subject), *episode_list)


def store_MMSE(here):
    # Data download path.
    data_path = os.path.join(here + r"/train" + r"/datasets" + r"/data")

    # First make directory to store data
    MMSE_dir = os.path.join(data_path + r"/MMSE")
    if os.path.isdir(MMSE_dir):
        return None

    # First make directory to store data
    os.mkdir(MMSE_dir)

    # create data path list
    episode_path = os.path.join(data_path + r"episode_parsed")
    file_list = sorted([i for i in os.listdir(episode_path) if i[0] == "S"])

    for i, dir in enumerate(file_list):
        # Load data.
        subject_num = "S{0:02d}".format(i + 1)
        npz_filename = subject_num + ".npz"
        temp = np.load(os.path.join(episode_path, subject_num, npz_filename))
        list = natsort.natsorted(temp.files)

        # Make a long list that ...
        for i, item in tqdm(
            enumerate(list),
            total=len(list),
            desc="Subject_{0:02d}".format(i + 1),
            ncols=80,
            leave=False,
        ):
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
                    -1,
                    -1,
                ]
                app = pd.DataFrame([append], columns=header)
                data = pd.concat([data, app], ignore_index=True)

            # Store the EEG data.
            else:
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
                app = pd.DataFrame([append], columns=header)
                data = pd.concat([data, app], ignore_index=True)

        # Store data.
        # Save directory
        save_dir = os.path.join(MMSE_dir, subject_num)
        os.mkdir(save_dir)
        # Filename for csv file.
        csv_filename = os.path.join(subject_num + ".csv")
        data.to_csv(os.path.join(save_dir, csv_filename))
