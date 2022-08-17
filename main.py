# Main training code.
import os
from data_preprocess import *

# Data parse.
here = os.path.dirname(os.path.abspath(__file__))
if not (
    os.path.isdir(
        os.path.join(here + "\\train" + "\\datasets" + "\\data" + "\\episode_parsed")
    )
):
    parsing(here)

