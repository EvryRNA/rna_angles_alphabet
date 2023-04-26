import os
import pickle
import random
import string
from typing import Any

import matplotlib.colors as mcolors
import numpy as np
import pandas as pd


def setup_dir(temp_dir: str):
    """
    Create directories used by the pipeline

    Args:
        :param temp_dir: the path of the temporary directory
    """
    # Check if the directories and create them if not
    os.makedirs("models", exist_ok=True)
    os.makedirs("figures_clust", exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)


def get_angle(path_csv: str, mol: str) -> np.ndarray:
    """
    Extract the angle values of a csv file to write them in an array

    Args:
        :param path_csv: the path of the csv file
        :param mol: the type of biomolecule, protein or rna
    Returns:
        return an array with the couples of angle values
    """
    raw_data = pd.read_csv(path_csv)

    data = raw_data.dropna()

    # The column names depends on the molecule type
    if mol == "rna":
        angle_values = data[["ETA", "THETA"]].to_numpy()
    elif mol == "protein":
        angle_values = data[["PHI", "PSI"]].to_numpy()

    return angle_values


def save_model(path_save_model: str, model: Any):
    """
    Save a model in pickle format

    Args:
        :param path_save_model: the path used to save the model
        :param model: the model to save
    """
    with open(path_save_model, "wb") as model_file:
        pickle.dump(model, model_file)


def load_model(path_load_model: str):
    """
    Load a model in pickle format

    Args:
        :param path_load_model: the path used to find the save model
    Returns:
        return the loaded model
    """
    with open(path_load_model, "rb") as model_file:
        loaded_model = pickle.load(model_file)

    return loaded_model


def labels_to_seq(list_labels: list) -> str:
    """
    Transform the labels of a list into a string sequence

    Args:
        :param list_labels: the list containing the labels of the a file
    Returns:
        return a sequence in capital letters
    """
    sequence = ""
    list_structure = list(string.ascii_uppercase)

    # For outlier method, changes labels -1 and 1 into -1 and 0
    if list(set(list_labels)) == [1, -1]:
        list_labels = [0 if x == 1 else x for x in list_labels]

    # Attribute a letter to each label, "-" if -1
    for i in range(0, len(list_labels)):
        if list_labels[i] == -1:
            letter = "-"
        else:
            letter = list_structure[list_labels[i]]
        sequence += letter

    return sequence


def get_colors(nb_colors: int):
    """
    Return a list of random colors

    Args:
        :param nb_colors: the number of colors to return
    Returns:
        return a list of different colors
    """
    # The 7 base colors
    colors = ["k", "r", "g", "b", "y", "m", "c"]

    # If there are more clusters, add random ones to complete
    if nb_colors > 7:
        list_colors = mcolors.CSS4_COLORS

        for i in range(0, nb_colors - 7):
            colors.append(random.choice(list(list_colors.keys())))

    return colors
