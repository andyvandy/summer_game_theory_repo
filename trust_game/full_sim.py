# Library imports
import numpy as np
import matplotlib.pyplot as pyplot
import seaborn as sns

# Imports from local files
from game import *
from agent_class import *
from trust_config import *
from generation import *

def main():
    print "Beginning simulation..."
    # Calculate max number of turns.
    theta = (1 - W)
    max_turns = int(round(-np.log(0.95) / theta)) # why? -andrew
    
    

    avg_gift = np.zeros(GENERATIONS)
    params={"theta":theta,
            "NUMBER_OF_AGENTS" : NUMBER_OF_AGENTS,
            "ROUNDS": ROUNDS,
            "GENERATIONS":GENERATIONS,
            "max_turns":max_turns,
            "B":B,
            "C":C,
            "SWAP" : SWAP, 
            "RESET" : RESET, 
            "MEMORY" : MEMORY, 
            "ENDOWMENT" : ENDOWMENT,
            "MUTATION_PARAMS" : MUTATION_PARAMS,
        }
    agent_list = create_initial_agents(**params)
    for i in range(GENERATIONS):
        # Mutates the agents if necessary 
        if i :  #changed this from  i != 0 to just i since bool(i) is the same in theis case as bool( i != 0) - andrew
            agent_list.sort(key = lambda x: x.score, reverse = True)
            agent_list = mutate_agents(agent_list,**params) #changed this so that it just passes the full list as well as some mutation params -a

        for _ in range(ROUNDS):
            # Sets the number of turns with an exponential distribution, with a 
            # maximum at the 95th percentile
            turns = min(int(round(r.expovariate(theta))) + 1, 
                     int(-np.log(0.05) / theta))
            
            for j in xrange(0,NUMBER_OF_AGENTS,2): #(NUMBER_OF_AGENTS / 2) does half of them. (0,NUMBER_OF_AGENTS,2) counts by twos and does them all -a
                game_stats = play_game(agent_list[j], agent_list[j + 1],
                                       turns = turns, **params)
                '''agent_list[j].score += game_score[0]
                agent_list[j + 1].score += game_score[1]
                agent_list[j].avg_gift += game_score[2]
                agent_list[j].avg_gift += game_score[3]'''

        if GENERATIONS % 1 == 0:
                print i+1, "generations complete."

    print "The simulation has completed."
    print "Generating plot..."

if __name__=="__main__":
    main()