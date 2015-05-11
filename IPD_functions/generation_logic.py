import random as r
from IPD_utilities import *
from generate_agents import *
from game_logic import *


def play_round(agents, game, w=0.9, max_states=8, all_max=False, noise=True):
    """Pairs agents off to go play a game so that each agent plays one game per
    round. All games are of the same length in a given round, the strategies
    shouldn't be affected.
    
    Args:
        agents: the list of agents
        game: the game matrix
        w: the probability of the game going on another turn
        max_states: the maximum number of states
        all_max: whether or not the agents will all have the maximum number of
            states
        noise: whether or not to use Joss-Ann noise

    Returns:
        round_info: a list of scores in the same order as the list of agents was
            given

    Notes:
        - Need to check the shuffling closely to make sure everything is going
          alright.
        - Could likely be sped up
    """

    shuffled_numbers = range(len(agents))
    r.shuffle(shuffled_numbers)
    order_assignment = zip(agents, shuffled_numbers)
    # print order_assignment
    scores = [0] * len(agents)

    stats=[0, #cooperations
           0, #defections
           0 #turns
           ]
           
    #calculates how many turns for the round using an exponential distribution
    turns = int(round(r.expovariate(1 - w))) + 1 
    
    # I have a feeling that this is the slow bit -Stu
    for i in [2 * j for j in range(len(agents) / 2)]:
        index1, index2 = [y[1] for y in order_assignment].index(i), [y[1] for y in order_assignment].index(i + 1)
        (player1, player2) = order_assignment[index1][0], order_assignment[index2][0]
        (scores[index1], scores[index2]),gamestats = play_game(player1, player2, game, 
                                                     turns = turns, 
                                                     noise = noise)
        stats[0]+=gamestats[0]
        stats[1]+=gamestats[1]
    stats[2]= turns + 1 
    return (scores, stats ) # since the first turn in games isn't counted

    
def run_generation(agents, game, evol, count=64, rounds=100, w=0.9, 
                   max_states=8, all_max=False, start_states=2, last_gen=False, 
                   noise=True):
    """Runs a single generation.

    Args:
        agents: the list of agents
        game: the game matrix
        evol: a list of evolution settings (breed, survive, newcomers)
        count: the number of agents
        rounds: ???
        w: the probability of the game going on another turn
        max_states: the maximum number of states
        all_max: whether or not the agents will all have the maximum number of 
            states
        start_states: ???
        last_gen: whether or not this is the final generation
        noise: whether or not to use Joss-Ann noise

    Returns
        gen_info: a tuple containing ??? 
    """

    scores = [0] * len(agents)
    #for agent in agents:
    #    print agent
    
    cooperations=0
    defections=0
    turn_count = 0
    for i in range(rounds):
        round_scores, round_stats = play_round(agents, game, w = w, 
                                                all_max = all_max, 
                                                max_states = max_states, 
                                                noise = noise)
        scores = [x + y for x, y in zip(scores, round_scores)]
        cooperations+= round_stats[0]
        defections+= round_stats[1]
        turn_count += round_stats[2]
        

    results = zip(agents, scores) 
    results.sort(key = get_key, reverse = True) #highest scores first

    top_scores=[]
    winners=[]
    offspringses=[]
    average=[]

    if last_gen: next_gen, top_scores = [x[0] for x in results], [x[1] for x in results]
 
    #data tracking------V
    sentience = 0
    coop_prob_total = 0
    defect_prob_total = 0
    for agent in agents:
        if sum(agent[1]) <= 1:
            sentience += sum(agent[1])
            coop_prob_total += agent[1][0]
            defect_prob_total += agent[1][1]
        else:
            sentience += 2 - sum(agent[1])
            coop_prob_total += 1 - agent[1][1]
            defect_prob_total += 1 - agent[1][0]
    avg_sentience = float(sentience) / count
    avg_hard_coop= float(coop_prob_total) / count
    avg_hard_defect= float(defect_prob_total) / count
    avg_score = float(sum(scores)) / (count * turn_count)
    avg_pop_coop= float(cooperations) / (count * turn_count)
    avg_pop_defect= float(defections) / (count * turn_count)
    # print avg_score
    # should return all stats in one tuple, preferably a labelled one
    batting_avg = [float(x) / turn_count for x in top_scores]
    stats=(avg_score, batting_avg, 
            avg_sentience,
            avg_hard_coop,
            avg_hard_defect,
            avg_pop_coop,
            avg_pop_defect)
    #data tracking------^
   
    if last_gen: return (next_gen, top_scores, stats)

    for i in range(evol[0]):
        winner = results[i][0]
        winners.append(winner) 
        top_scores.append(results[i][1]) # check
        offspring = reproduce(winner, all_max = all_max, 
                              max_states = max_states)
        offspringses.append(offspring)
 
    for i in range(evol[0],count - evol[0] - evol[2]):
        average.append(results[i][0]) 
        top_scores.append(results[i][1])

    next_gen = winners + average + offspringses
    next_gen += generate_agents(count = evol[2], max_states = start_states, 
                                all_max = True)
    #print len(next_gen)
    #print next_gen
    #raw_input('Press <ENTER> to continue')
    return (next_gen, top_scores, stats)    


def reproduce(agent, all_max=False, max_states=8):
    # returns a mutated offspring
    list_agent = [i for i in agent]
    states = (len(agent) - 2) / 3
    mutation = r.randint(0, 199)
    mutation_state = r.randint(1, states)
    if 0 <= mutation < 10 and states > 1:
        #remove a state
        defect_dest = list_agent.pop((mutation_state) * 3 + 1) # be careful with this stuff it can break super easily :'(
        coop_dest=list_agent.pop((mutation_state) * 3)
        list_agent.pop((mutation_state) * 3 - 1)
        for index in range(len(list_agent)):
            if list_agent[index] == mutation_state:
                if index % 3 == 0 and index > 1: 
                    if mutation_state != coop_dest: list_agent[index] = coop_dest
                    else: list_agent[index]= index / 3
                elif index % 3 == 1  and index > 1: 
                    # this is needed or esle the actions will be overwritten
                    if mutation_state != defect_dest: list_agent[index] = defect_dest
                    else: list_agent[index] = index / 3
        for i in range(mutation_state + 1,  states + 2):
            #we don't want to overwrite the starting info so we start at 2
            for index in range(2, len(list_agent)): 
                if list_agent[index] == i:
                    # print "guh"
                    # print list_agent[index],index,i
                    list_agent[index] -= 1
    elif 9 < mutation < 25 and states < max_states:
        # add a state
        list_agent += [r.randint(0,1), r.randint(1, states + 1), r.randint(1, states + 1)] 
    elif 24 < mutation < 45  or 99 < mutation < 121:
        # change the defect joss_ann noise parameters +-0.1
        j1, j2 = (list_agent[1][0], max(min(list_agent[1][1] - 0.1 + 0.2 * r.random(), 1.0), 0.0))
        list_agent[1]=[j1, j2]
    elif 120 < mutation < 161:
        # change the  coop joss_ann noise parameters +-0.1
        j1, j2 =(max(min(list_agent[1][0] - 0.1 + 0.2 * r.random(), 1.0), 0.0), list_agent[1][1])
        list_agent[1] = [j1, j2]
    elif 44 < mutation < 60:
        # change the state move
        list_agent[mutation_state * 3 - 1] = int(not list_agent[mutation_state * 3 -1])
    elif 59 < mutation < 80:
        # change the state coop destination
        list_agent[mutation_state * 3] = (list_agent[mutation_state * 3] + r.randint(0, states - 1)) % states +1
    elif 79 < mutation < 100 :
        # change the state deceive destination
        list_agent[mutation_state * 3 +1] = (list_agent[mutation_state * 3 + 1] + r.randint(0, states - 1)) % states + 1
    
    return list_agent

    
def test_generation_logic():
    #TODO: write tests for these functions
    r.seed(13)
    assert len(generate_agents(count = 12, max_states = 4, all_max = True)[5]) == 4 * 3 + 2
    return 'test passes'

#print test_generation_logic()
    
