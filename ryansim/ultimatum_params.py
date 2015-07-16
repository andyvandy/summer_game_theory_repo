PARAMS = {'GRANULARITY': 1,
          'ROUNDS': 500,
          'STARTING_DISTRIBUTION': 'cluster',
          'SIM_NAME': 'pre_mod_test',
          'TEAM_SPEC': [('cluster', (0.5, 0.5)), 
                        ('uniform',), 
                        ('random',)]}

"""
GRANULARITY: Represents how fine the strategy distribution is. Higher
    granularity implies fewer strategies.

ROUNDS: The number of rounds to run the simulation for.

STARTING_DISTRIBUTION: Determines the initial distribution of strategies.
    Options:
        'rand': completely random distribution of strategies
        'uniform': uniform distribution of strategies
        'cluster': clustered strategies based on a product of binomial
            distributions
"""