import numpy as np
import pandas as pd
from scipy import ndimage

from initial_matrix_generators import random_array, uniform_array
from initial_matrix_generators import binomial_product_array


class Team(object):
    """This represents a team (or agent) in the game.

    Attributes:
        distribution: a numpy matrix representing the distribution of strategies
        population: a number representing the team's share of the global 
            population
        name: the name of the team
    """


    def __init__(self, name, starting_distribution, dist_params=None, **params):
        """Initializes the team and gives it a starting strategy distribution.

        Args:
            params:
                dimension: the side length of the strategy distribution matrix
                number_of_teams: the total number of teams in the game
            starting_distribution: the type of distribution to start with
        """

        # Unpack parameters
        dimension = params['DIMENSION']
        number_of_teams = params['NUMBER_OF_TEAMS']

        self.name = name

        # Assume square strategy space
        shape = (dimension, dimension)

        # Initialize strategy distribution
        if starting_distribution == 'rand':
            self.distribution = random_array(shape)
        elif starting_distribution == 'cluster':
            self.distribution = binomial_product_array(shape, dist_params['p'])
        elif starting_distribution == 'uniform':
            self.distribution = uniform_array(shape)
        else:
            print "Critical error."
            sys.exit()

        # Initialize fitness
        self.scores = np.zeros((dimension, dimension))

        self.population = 1.0 / number_of_teams

        self.stats = pd.DataFrame(columns = ('population', 
                                             'average_deal',
                                             'center_of_mass'))


    def center_of_mass(self, **params):
        """Calculates the center of mass (mean) of the strategy distribution.

        Args:
            params:
                number_of_teams: the total number of teams in the game

        Returns:
            cm: a tuple (I think) showing the coordinates 
        """

        number_of_teams = params['NUMBER_OF_TEAMS']

        cm = ndimage.measurements.center_of_mass(self.distribution / 
                                                  number_of_teams)

        return cm


    def update_stats(self, round_number, new_stats):
        """
        """

        self.stats.loc[round_number] = new_stats