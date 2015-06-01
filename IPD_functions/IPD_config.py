# This is where the settings can be changed for the IPD simulation

# the payoff matrix
GAME_MATRIX =   [[3,3], [-10, 0], [-10, 0], [0,0]] 
"""list of games:
    prisoner's dilemma:          [[3, 3], [0, 5], [5, 0], [1, 1]] 
    snowdrift/chicken game:     [[3, 3], [1, 5], [5, 1], [0, 0]] 
    Stag-hunt game :             [[2, 2], [0, 1], [1, 0], [1, 1]] 
    Battle of the Sexes game :  [[0, 0], [1, 2], [2, 1], [0, 0]] 
    
    ---Andrew's games---
    prisoner's dilemma mod 1:     [[3, 3], [0, 7], [7, 0], [1, 1]] 
    jerk :     [[3,3], [-10, 0], [-10, 0], [0,0]] 
    
    
    
    custom 1:                   [[5, 5], [3,1], [1, 3], [0, 0]] 
    custom 2:                   [[5, 5], [3,0], [0, 3], [1, 1]]
    custom 3:                   [[5, 5], [1,3], [3, 1], [0, 0]] 
    custom 4:                   [[5, 5], [1,0], [0, 1], [3, 3]] #coordination
    custom 5:                   [[5, 5], [0,3], [3, 0], [1, 1]]
    custom 6:                   [[5, 5], [0,1], [1, 0], [3, 3]] #coordination flipped
    custom 7:                   [[1, 1], [5,3], [3, 5], [0, 0]] # similar to battle of the sexes but one option has slight more weight to it
    custom 8:                   [[1, 1], [5,0], [0, 5], [3, 3]] 
    custom 9:                   [[0, 0], [5,3], [3, 5], [1, 1]] # similar to battle of the sexes but one option has slight more weight to it flipped
    custom 10:                  [[0, 0], [5,1], [1, 5], [3, 3]]
"""

NUMBER_OF_AGENTS = 64
MAX_STATES = 32
START_STATES = 1
ALL_MAX = False # whether or not all agents will have the max number of states
ROUNDS = 128
GENERATIONS = 1000
SIMULATIONS = 250
W = 0.98 # probability of game going on another turn
NOISE = False # use Joss_ann noise or not
EVOLUTION_SETTINGS = (24, 23, 1) # (breed, survive, newcommers)