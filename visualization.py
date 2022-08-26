# Data visualization function.

import os
import pandas as pd

# here = os.path.dirname(os.path.abspath(__file__))
here = os.getcwd()

# Import data.
data_dir = os.path.join(here, r"train/datasets/data/MMSE")
dir_list = sorted([i for i in os.listdir(data_dir) if i[0] == "S"])
for dir in dir_list:
    data_path = os.path.join(data_dir, dir, dir + ".csv")
    exec(f"{dir}_data = pd.read_csv(data_path)")

