import numpy as np
from scipy import special
import matplotlib.pyplot as plt


def binomial_probability(n, N, p):
    """Gives the probability of N successes in n trials with probability of
    success p from the binomial distribution.

    Args:
        n: number of trials
        N: number of successes
        p: probability of success for each trial

    Returns:
        P: probability of N successes
    """

    P = special.binom(n, N) * (p ** N) * (1.0 - p) ** (n - N)

    return P


def binomial_sum_array(dimension, p):
    """Builds a 2D array by adding two binomial probabilities at each entry.

    Args:
        dimension: a tuple containing the desired (rows, columns)
        p: a tuple containing the binomial distribution parameter p along the
            (rows, columns)

    Returns:
        array: a 2D numpy array with size given by dimension
    """

    rows, columns = dimension
    p_rows, p_columns = p

    row_points, column_points = np.arange(rows), np.arange(columns)

    row_mesh, column_mesh = np.meshgrid(row_points, column_points)

    bin_sum = lambda x, y: (binomial_probability(rows, x, p_rows) +
                            binomial_probability(columns, y, p_columns))

    array = bin_sum(row_mesh, column_mesh)

    array = array / np.sum(array)

    return array


def binomial_product_array(dimension, p):
    """Builds a 2D array by multiplying two binomial probabilities at each
    entry.

    Args:
        dimension: a tuple containing the desired (rows, columns)
        p: a tuple containing the binomial distribution parameter p along the
            (rows, columns)

    Returns:
        array: a 2D numpy array with size given by dimension
    """

    rows, columns = dimension
    p_rows, p_columns = p

    row_points, column_points = np.arange(rows), np.arange(columns)

    row_mesh, column_mesh = np.meshgrid(row_points, column_points)

    bin_product = lambda x, y: (binomial_probability(rows, x, p_rows) *
                                binomial_probability(columns, y, p_columns))

    array = bin_product(row_mesh, column_mesh)

    array = array / np.sum(array)

    return array