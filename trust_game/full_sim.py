# Library imports
import numpy as np
import matplotlib.pyplot as pyplot
import seaborn as sns
import os

# Imports from local files
from game import *
from agent_class import *
from trust_config import *
from generation import *
from log_utils import *

def main():
    # Calculate max number of turns.
    theta = (1 - W)
    max_turns = int(round(-np.log(0.05) / theta)) # 95th percentile
    
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
            "LOG" : LOG,
            "LOG_DIR" : os.path.join("output", "logs", LOG_DIR),
            "ENDOWMENT" : ENDOWMENT,
            "MUTATION_PARAMS" : MUTATION_PARAMS,
            }

    if LOG:
        ensure_directory(params["LOG_DIR"])

    print "Beginning simulation..."

    agent_list = create_initial_agents(**params)

    for i in range(GENERATIONS):
        if params["LOG"]:
            log_file = open(os.path.join(params["LOG_DIR"], 
                                      "gen_" + str(i) + ".log"), 
                            "w")

            write_gen_number(log_file, i)

        # Mutates the agents if necessary.  
        if i:
            agent_list.sort(key = lambda x: x.score, reverse = True)
            agent_list = mutate_agents(agent_list, i, **params)

        for k in range(ROUNDS):
            if params["LOG"]:
                write_round_number(log_file, k)

            # Sets the number of turns with an exponential distribution, with a 
            # maximum at the 95th percentile
            turns = min(int(round(r.expovariate(theta))) + 1, 
                        max_turns)
            
            for j in xrange(0, NUMBER_OF_AGENTS, 2):
                if params["LOG"]:
                    write_matchup_header(log_file, j / 2, agent_list[j].ID, 
                                         agent_list[j + 1].ID)

                game_stats = play_game(agent_list[j], agent_list[j + 1],
                                       turns = turns, log_file = log_file, 
                                       **params)

                if params["LOG"]:
                    log_file.write("\n")

                '''agent_list[j].score += game_score[0]
                agent_list[j + 1].score += game_score[1]
                agent_list[j].avg_gift += game_score[2]
                agent_list[j].avg_gift += game_score[3]'''

        if GENERATIONS % 1 == 0:
                print i+1, "generations complete."

        if params["LOG"]:
            log_file.close()

    print "The simulation has completed."
    print "Generating plot..."

if __name__=="__main__":
    main()