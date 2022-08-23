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
print("Base parsing done.")
input("Press enter to continue...")

# Data visualization.
# Save entropy of each episode.
store_MMSE(here)
