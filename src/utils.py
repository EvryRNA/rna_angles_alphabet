import os
import pickle
import string
from typing import Any

import numpy as np
import pandas as pd


def list_pdb(path: str, data: str, temp_dir: str):
    """
    Write the list of pdb files in a directory in a txt file
    """
    with open(f"{temp_dir}/{data}_set.txt", "w") as file:
        for filename in os.listdir(path):
            file.write(f"{filename}\n")

    return


def text_to_csv(path: str, angles: list):
    """
    Extract the angle values of a file to write them in a csv
    """
    with open(path, "r") as filin, open(f"{path[:-4]}.csv", "w") as filout:
        filout.write(f"{angles[0]},{angles[1]}\n")
        for line in filin:
            values = line.split()

            if values[0] != f"{angles[1]}" and values[0] != "NA" and values[1] != "NA":
                filout.write(f"{float(values[1])},{float(values[0])}\n")

    return


def get_angle(path: str):
    """
    Extract the angle values of a csv to write them in an array
    """
    angle = []

    data = pd.read_csv(path)
    col = list(data.columns)

    for i in range(0, len(data[col[0]].tolist())):
        angle.append([data[col[0]].tolist()[i], data[col[1]].tolist()[i]])

    return np.array(angle)


def save_model(path: str, model: Any):
    """
    Save a model in pickle format
    """
    with open(path, "wb") as model_file:
        pickle.dump(model, model_file)

    return


def load_model(path: str):
    """
    Load a model in pickle format
    """
    with open(path, "rb") as model_file:
        loaded_model = pickle.load(model_file)

    return loaded_model


def labels_to_seq(tab):
    """
    Transform the labels of an array in a string sequence
    """
    sequence = ""
    list_structure = list(string.ascii_uppercase)

    for i in range(0, len(tab)):
        if tab[i] == -1:
            letter = "-"
        else:
            letter = list_structure[tab[i]]
        sequence += letter

    return sequence
