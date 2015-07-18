import numpy as np

PARAMS = {'GRANULARITY': 1,
          'ROUNDS': 1000,
          'STARTING_DISTRIBUTION': 'cluster',
          'SIM_NAME': 'clust_v_unif_test',
          'TEAM_SPEC': [('A', 'cluster', {'p': np.random.rand(1,2)[0]}), 
                        ('B', 'uniform', {})]
         }

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