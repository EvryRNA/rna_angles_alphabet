import numpy as np
import pandas as pd
import pickle
from typing import Any


def text_to_csv(path : str):

    with open(path, 'r') as filin, open(f"{path[:-4]}.csv", 'w') as filout:
        filout.write("ETA,THETA\n")
        for line in filin:
            values = line.split()

            if values[0] != "THETA" and values[0] != "NA" and values[1] != "NA":
                filout.write(f"{float(values[1])},{float(values[0])}\n")
    
    return


def get_angle(path):
	angle = []

	data = pd.read_csv(path)
	x = np.array(data.ETA.values)
	y = np.array(data.THETA.values)

	for j in range(0, len(x)):
		angle.append([x[j], y[j]])
	
	return np.array(angle)


def save_model(path : str, model : Any):

    with open(path, 'wb') as model_file:
        pickle.dump(model, model_file)

    return


def load_model(path):

    with open(path, 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    return loaded_model


if __name__ == "__main__":
    a = 0