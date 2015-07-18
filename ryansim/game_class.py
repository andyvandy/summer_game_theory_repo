import numpy as np
import pandas as pd
from team_class import Team

class Game(object):
    """This specifies the game.
    """

    def __init__(self, **params):
        """
        """

        team_spec = params["TEAM_SPEC"]
        dimension = params["DIMENSION"]
        number_of_teams = params['NUMBER_OF_TEAMS']

        self.teams = []

        for i in range(number_of_teams):
            self.teams.append(Team(team_spec[i][0], team_spec[i][1], 
                                   team_spec[i][2], **params))

        self.names = [team.name for team in self.teams]


    def calc_scores(self, **params):
        """Uses the strategy distribution and relative population to calculate
        fitness.
        """

        dimension = params['DIMENSION']
        granularity = params['GRANULARITY']
        number_of_teams = params['NUMBER_OF_TEAMS']

        interim = np.mgrid[100: -granularity: -granularity, 
                           100: -granularity: -granularity][1]
        
        dist_mod = [team.distribution * interim for team in self.teams]

        pop_table = np.zeros((number_of_teams, number_of_teams))

        for i in range(number_of_teams):
            for j in range(number_of_teams):
                pop_table[i][j] = (self.teams[i].population / 
                                     (self.teams[i].population + 
                                      self.teams[j].population))

        j_mats = []
        i_mats = []

        for team_number in range(number_of_teams):
            j_mats.append(np.matrix([[dist_mod[team_number][j: dimension, :].sum()] * 
                                      dimension for j in range(dimension)]))

            i_mats.append(np.matrix([[(100 - i * granularity) * 
                                     self.teams[team_number].distribution[:, (dimension - i): dimension].sum() for i in range(dimension)]] * dimension))

        for team_number in range(number_of_teams):
            magic_matrix = np.zeros((dimension, dimension))

            for i in range(number_of_teams):
                for j in range(number_of_teams):
                    if team_number != i and team_number != j and i != j:
                        magic_matrix += pop_table[i][j] * (j_mats[i] + i_mats[i])

            self.teams[team_number].scores = np.array(0.5 * magic_matrix)


    def update_data(self, round_number, **params):
        """
        """

        dimension = params['DIMENSION']
        unit_value = params['UNIT_VALUE']
        number_of_teams = params['NUMBER_OF_TEAMS']

        # Update team stats
        for team in self.teams:
            average_deal = team.scores.sum() / (dimension ** 2) / (number_of_teams - 1)

            new_stats = {'population': team.population,
                         'average_deal': average_deal,
                         'center_of_mass': team.center_of_mass(**params)}

            team.update_stats(round_number, new_stats)

        # Update distributions
        scores_sums = [team.scores.sum() for team in self.teams]
        scores_sum = sum(scores_sums)

        pop_multipliers = [scores_sums[i] / (scores_sum + 
                                             (number_of_teams - 1) / 
                                             number_of_teams) for i in range(number_of_teams)]

        pop_breakdown_temp = [(self.teams[i].population * pop_multipliers[i]) 
                              for i in range(number_of_teams)]

        pop_breakdown_sum = sum(pop_breakdown_temp)

        for i in range(number_of_teams):
            self.teams[i].population = pop_breakdown_temp[i] / pop_breakdown_sum

        total_matrix = np.zeros((dimension, dimension))

        for team in self.teams:
            total_matrix += team.scores * team.distribution

        total_sum = total_matrix.sum()

        for team in self.teams:
            team.scores = team.scores / total_sum
            team.distribution = team.distribution * team.scores
            team.distribution = team.distribution / team.distribution.sum()