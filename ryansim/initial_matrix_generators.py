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


def multivariate_normal_array(dimension, mean, cov, samples):
    """Builds a 2D array by sampling a multivariate normal distribution and 
    binning the samples into a 2D histogram.

    Args:
        dimension: a tuple containing the desired (rows, columns)
        mean: a tuple containing the ()

    Returns:
    """
    

def random_array(dimension):
    """Builds a random 2D array.

    Args:
        dimension: a tuple containing the desired (rows, columns)
    """

    array = np.random.random(dimension)
    array = array / array.sum()

    return array


def uniform_array(dimension):
    """Builds a uniform 2D array.

    Args:
        dimension: a tuple containing the desired (rows, columns)
    """

    array = np.ones(dimension)
    array = array / array.sum()

    return array


def initialize_starting_distribution(**params):
    """Initialize the starting strategy distributions.

    Args:
        params:
            dimension:
            starting_distribution:
            starting_pct

    Returns:
        teams: a list containing the strategy distributions
    """

    dimension = params['DIMENSION']
    starting_distribution = params['STARTING_DISTRIBUTION']
    starting_pct = params['STARTING_PCT']

    teams = []

    if starting_distribution == 'rand':
        teams.append(random_array((dimension, dimension)))
        teams.append(random_array((dimension, dimension)))
        teams.append(random_array((dimension, dimension)))
  
    elif starting_distribution == 'cluster':
        teams.append(binomial_product_array((dimension, dimension), (0.3, 0.7)))
        teams.append(binomial_product_array((dimension, dimension), (0.7, 0.3)))
        teams.append(binomial_product_array((dimension, dimension), (0.5, 0.5)))
        
    elif starting_distribution == 'uniform':
        teams.append([starting_pct] * dimension ** 2)
        teams[0] = np.reshape(original_teams[0], (dimension, dimension))
        teams.append([starting_pct] * dimension ** 2)
        teams[1] = np.reshape(teams[1], (dimension, dimension))
        teams.append([starting_pct] * dimension ** 2)
        teams[2] = np.reshape(teams[2], (dimension, dimension))

    return teams


