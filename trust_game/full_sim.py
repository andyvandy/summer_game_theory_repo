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
            "A":A,
            "B":B,
            "C":C,
            "SWAP" : SWAP, 
            "RESET" : RESET, 
            "MEMORY" : MEMORY,
            "LOG" : LOG,
            "LOG_DIR" : os.path.join("output", LOG_DIR, "logs"),
            "ENDOWMENT" : ENDOWMENT,
            "MUTATION_PARAMS" : MUTATION_PARAMS,
            }

    if LOG:
        ensure_directory(params["LOG_DIR"])

    print "Beginning simulation..."

    agent_list = create_initial_agents(**params)

    avgscore,avg_gift_a,avg_gift_b,avg_score_a,avg_score_b=[],[],[],[],[]
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
        total_turns =0
        for k in range(ROUNDS):
            if params["LOG"]:
                write_round_number(log_file, k)

            # Sets the number of turns with an exponential distribution, with a 
            # maximum at the 95th percentile
            turns = min(int(round(r.expovariate(theta))) + 1, 
                        max_turns)
            total_turns += turns
            for j in xrange(0, len(agent_list), 2):
                if params["LOG"]:
                    write_matchup_header(log_file, j / 2, agent_list[j].ID, 
                                         agent_list[j + 1].ID)

                game_stats = play_game(agent_list[j], agent_list[j + 1],
                                       turns = turns, log_file = log_file, 
                                       **params)
            
                if params["LOG"]:
                    log_file.write("\n")
                    
        avgscore.append(sum([x.score for x in agent_list]) / 
                        float(NUMBER_OF_AGENTS * 2 * total_turns))
        avg_gift_a.append(sum([x.total_a_gifts for x in agent_list]) / 
                          float(NUMBER_OF_AGENTS * total_turns))
        avg_gift_b.append(sum([x.total_b_gifts for x in agent_list]) / 
                          float(NUMBER_OF_AGENTS * total_turns))
        avg_score_a.append(sum([x.score_a for x in agent_list]) / 
                          float(NUMBER_OF_AGENTS * total_turns))
        avg_score_b.append(sum([x.score_b for x in agent_list]) / 
                          float(NUMBER_OF_AGENTS * total_turns))
            
        if GENERATIONS % 1 == 0:
                print i+1, "generations complete."

        if params["LOG"]:
            log_file.close()

    print "The simulation has completed."

    # Log params, summary statistics
    summary_statistics = (avgscore, 
                          avg_gift_a, 
                          avg_gift_b, 
                          avg_score_a, 
                          avg_score_b)

    json_file = open(os.path.join(params["LOG_DIR"], "data.json"), 'w')
    write_summary_json(json_file, params, summary_statistics)
    json_file.close()

    print "Generating plot..."

if __name__=="__main__":
    main()