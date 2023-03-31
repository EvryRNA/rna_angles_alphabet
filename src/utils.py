import os
import pickle
import string
from typing import Any

import numpy as np
import pandas as pd


def list_pdb(path_dir: str, dataset: str, temp_dir: str):
    """
    Write the list of the pdb files of a directory in a txt file

    Parameters
        ----------
        path_dir : the path of the directory containing the data
        data : the name of the dataset used to name the txt file, training or testing
        temp_dir : the path of the temporary directory
    """
    with open(f"{temp_dir}/{dataset}_set.txt", "w") as file:
        for filename in os.listdir(path_dir):
            file.write(f"{filename}\n")


def text_to_csv(path_txt: str, angles_names: list):
    """
    Extract the angle values of a file to write them in a csv

    Parameters
        ----------
        path_txt : the path of the txt file containing tha angle values
        angles_names : names of the angles in the file, PHI-PSI for protein and
        ETA-THETA for RNA
    """
    with open(path_txt, "r") as filin, open(f"{path_txt[:-4]}.csv", "w") as filout:
        filout.write(f"{angles_names[0]},{angles_names[1]}\n")
        for line in filin:
            values = line.split()

            if values[0] != f"{angles_names[1]}" and values[0] != "NA" and values[1] != "NA":
                filout.write(f"{float(values[1])},{float(values[0])}\n")


def get_angle(path_csv: str):
    """
    Extract the angle values of a csv file to write them in an array

    Parameters
        ----------
        path_csv : the path of the csv file
    """
    angle = []

    data = pd.read_csv(path_csv)
    col = list(data.columns)

    for i in range(0, len(data[col[0]].tolist())):
        angle.append([data[col[0]].tolist()[i], data[col[1]].tolist()[i]])

    return np.array(angle)


def save_model(path_save_model: str, model: Any):
    """
    Save a model in pickle format

    Parameters
        ----------
        path_save_model : the path used to save the model
        model : the model to save
    """
    with open(path_save_model, "wb") as model_file:
        pickle.dump(model, model_file)


def load_model(path_load_model: str):
    """
    Load a model in pickle format and return it

    Parameters
        ----------
        path_load_model : the path used to find the save model
    """
    with open(path_load_model, "rb") as model_file:
        loaded_model = pickle.load(model_file)

    return loaded_model


def labels_to_seq(list_labels: list):
    """
    Transform the labels of a list into a string sequence

    Parameters
        ----------
        list_labels : the list containing the labels
    """
    sequence = ""
    list_structure = list(string.ascii_uppercase)

    for i in range(0, len(list_labels)):
        if list_labels[i] == -1:
            letter = "-"
        else:
            letter = list_structure[list_labels[i]]
        sequence += letter

    return sequence
