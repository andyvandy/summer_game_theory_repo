# This is where the settings can be changed for the IPD simulation

# the payoff matrix
GAME_MATRIX = [[3, 3], [0, 5], [5, 0], [1, 1]]
"""list of games:
    prisoner's dilema:[[3, 3], [0, 5], [5, 0], [1, 1]] 
    snowdrift/chicken game: [[3, 3], [1, 5], [5, 1], [0, 0]] 
"""

NUMBER_OF_AGENTS = 64
MAX_STATES = 6
START_STATES = 1
ALL_MAX = False # whether or not all agents will have the max number of states
ROUNDS = 10
GENERATIONS = 250
SIMULATIONS = 1
W = 0.98 # probability of game going on another turn
NOISE = False # use Joss_ann noise or not
EVOLUTION_SETTINGS = (24, 34, 1) # (breed, survive, newcommers)