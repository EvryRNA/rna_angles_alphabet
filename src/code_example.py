import numpy as np


def sum_image(matrix: np.ndarray) -> float:
    """
    Function that returns the sum of a matrix
    :param matrix: an array matrix
    :return: the sum of the matrix
    """
    return np.sum(matrix)


def min_image(matrix: np.ndarray) -> float:
    """
    Function that returns the min of a matrix
    :param matrix: an array matrix
    :return: the min of the matrix
    """
    return np.min(matrix)
