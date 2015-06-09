W = 0.95    # Probability that the game goes on another turn
NUMBER_OF_AGENTS = 36
GENERATIONS = 100
ROUNDS = 100   # Matchups per generation
ENDOWMENT=(5,0)    # How much each player receives at the start of the game
B = 5    # Multiplier for Investor -> Trustee
C = 1    # Multiplier for Trustee -> Investor
SWAP = False    # Whether or not agents switch roles after each turn
RESET = False    # Whether or not the balance is stored or can still be used
LOG = True    # Whether or not to write to log files
LOG_DIR = "testing" # Name of log subdirectory
MEMORY = 4    # How far back the agents remember
# determine the mix of the new pop when mutating 
# (# breed, # live but not breed, # newcommers)
MUTATION_PARAMS= (25,0,0)    