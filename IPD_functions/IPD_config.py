# This is where the settings can be changed for the IPD simulation

# the payoff matrix
GAME_MATRIX = [[3, 3], [0, 5], [5, 0], [1, 1]]  
"""list of games:
    prisoner's dilemma:          [[3, 3], [0, 5], [5, 0], [1, 1]] 
    snowdrift/chicken game:     [[3, 3], [1, 5], [5, 1], [0, 0]] 
    Stag-hunt game :             [[2, 2], [0, 1], [1, 0], [1, 1]] 
    Battle of the Sexes game :  [[0, 0], [1, 2], [2, 1], [0, 0]] 
"""

NUMBER_OF_AGENTS = 64
MAX_STATES = 10
START_STATES = 1
ALL_MAX = False # whether or not all agents will have the max number of states
ROUNDS = 150
GENERATIONS = 250
SIMULATIONS = 10
W = 0.98 # probability of game going on another turn
NOISE = False # use Joss_ann noise or not
EVOLUTION_SETTINGS = (12, 11, 1) # (breed, survive, newcommers)