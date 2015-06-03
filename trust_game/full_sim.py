# Library imports
import numpy as np
import matplotlib.pyplot as pyplot
import seaborn as sns

# Imports from local files
from game import *
from agent_class import *
from trust_config import *

def main():
    print "Beginning simulation..."
    # Calculate max number of turns.
    theta = (1 - w)
    max_turns = int(round(-np.log(0.95) / theta))
    
    agent_list = create_initial_agents(NUMBER_OF_AGENTS, max_turns)

    avg_gift = np.zeros(GENERATIONS)

    for i in range(GENERATIONS):
        # Mutates the agents if necessary
            if i != 0:
                agent_list.sort(key = lambda x: x.score, reverse = True)
                agent_list = mutate_agents(agent_list[:NUMBER_OF_AGENTS / 2], 
                                           max_turns)

        for j in range(ROUNDS):
            # Sets the number of turns with an exponential distribution, with a 
            # maximum at the 95th percentile
            turns = min(int(round(r.expovariate(theta))) + 1, 
                     int(-np.log(0.05) / theta)))
            
            for j in range(NUMBER_OF_AGENTS / 2):
                game_stats = play_game(agent_list[j], agent_list[j + 1], b = B, 
                                       turns = turns, reset = RESET)
                agent_list[j].score = game_score[0]
                agent_list[j + 1].score = game_score[1]
                agent_list[j].avg_gift = game_score[2]
                agent_list[j].avg_gift = game_score[3]

        if GENERATIONS % 25 == 0:
                print GENERATIONS, "generations complete."

    print "The simulation has completed."
    print "Generating plot..."


main()