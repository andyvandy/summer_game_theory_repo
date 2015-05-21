import random as r
from IPD_utilities import *
from generate_agents import *
from game_logic import *

import time


def timing_round(f):
    def wrap(agents, game, w=0.9, max_states=8, all_max=False, noise=True):
        time1 = time.time()
        ret = f(agents, game, w=w, max_states=max_states, all_max=all_max, noise=noise)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap    

def timing_generation(f):
    def wrap(agents, game, evol, count=64, rounds=100, w=0.9, 
                   max_states=8, all_max=False, start_states=2, last_gen=False, 
                   noise=True):
        time1 = time.time()
        ret = f(agents, game, evol, count = count, 
                rounds = rounds, w = w, 
                start_states = start_states,
                max_states = max_states, 
                all_max = all_max, 
                noise = noise,
                last_gen = last_gen)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap      

#@timing_round
def play_round(agents, game, w=0.9, max_states=8, all_max=False, noise=False):
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
    
   
    
    stats=[0, #cooperations
           0, #defections
           0 #turns
           ]
           
    # calculates how many turns for the round using an exponential distribution
    # to save on time since some games were taking forever and slowing stuff 
    # down This makes it run 30% faster
    turns = min(int(round(r.expovariate(1 - w)))+ 1, int(float(1/(1-w)))) 

    for i in range(0, len(agents), 2):
        gamestats = play_game(agents[i], agents[i + 1], game, turns = turns, 
                              noise = noise)

        stats[0] += gamestats[0] #cooperations
        stats[1] += gamestats[1] #defections
    
    stats[2]= turns 
    return stats 

#@timing_generation    
def run_generation(agents, game, evol, count=64, rounds=100, w=0.9, 
                   max_states=8, all_max=False, start_states=2, last_gen=False, 
                   noise=False):
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

    #for agent in agents:
    #    print agent
    
    cooperations=0
    defections=0
    turn_count = 0
    
    # reset scores
    for agent in agents:
        agent.score = 0
    
    # play the game
    for i in range(rounds):
        # Shuffle agents
        r.shuffle(agents)
        round_stats = play_round(agents, game, w = w, 
                                                all_max = all_max, 
                                                max_states = max_states, 
                                                noise = noise)
        cooperations+= round_stats[0]
        defections+= round_stats[1]
        turn_count += round_stats[2]
    
    # sort by scores
    agents.sort(key = lambda x: x.score +r.random(), reverse = True) #highest scores first , random to break ties , could likely be done better
    
    #for agent in agents:
    #    print agent.score
    top_scores=[]
    winners=[]
    offspringses=[]
    average=[]

    if last_gen: next_gen, top_scores = [x for x in agents], [x.score for x in agents]
 
    #data tracking------V
    sentience = 0
    coop_prob_total = 0
    defect_prob_total = 0
    for agent in agents:
        if sum(agent.joss_ann) <= 1:
            sentience += sum(agent.joss_ann)
            coop_prob_total += agent.joss_ann[0]
            defect_prob_total += agent.joss_ann[1]
        else:
            sentience += 2 - sum(agent.joss_ann)
            coop_prob_total += 1 - agent.joss_ann[1]
            defect_prob_total += 1 - agent.joss_ann[0]
    avg_sentience = float(sentience) / count
    avg_hard_coop= float(coop_prob_total) / count
    avg_hard_defect= float(defect_prob_total) / count
    avg_score = float(sum(agent.score for agent in agents)) / (count * turn_count)
    avg_pop_coop= float(cooperations) / (count * turn_count)
    avg_pop_defect= float(defections) / (count * turn_count)
    #print avg_pop_coop
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
        winner = agents[i]
        winners.append(winner) 
        top_scores.append(winner.score) # check
        offspring = reproduce(winner, all_max = all_max, 
                              max_states = max_states)
        offspringses.append(offspring)
 
    for i in range(evol[0],count - evol[0] - evol[2]):
        average.append(agents[i]) 
        top_scores.append(agents[i].score)

    next_gen = winners + average + offspringses
    next_gen += generate_agents(count = evol[2], max_states = start_states, 
                                all_max = True)
    #print len(next_gen)
    '''for agent in agents:
        print agent, agent.score , float(agent.score)/turn_count
    for noob in next_gen:
        print noob, noob.score , float(noob.score)/turn_count
    raw_input('Press <ENTER> to continue')  '''  
    
    return (next_gen, top_scores, stats)    


def reproduce(agent, all_max=False, max_states=8):
    # returns a mutated offspring
    behaviour_list=[]
    for state in agent.behaviour:
        behaviour_list.append(list(state))
    joss_ann_list=list(agent.joss_ann)
    states = len(agent.behaviour) 
    mutation = r.randint(0, 199)
    mutation_state = r.randint(1, states)
    if 0 <= mutation < 10 and states > 1:
        #remove a state
        removed_state=behaviour_list.pop(mutation_state-1)
        defect_dest = removed_state[2] # be careful with this stuff it can break super easily :'(
        coop_dest = removed_state[1]
        for i in range(len(behaviour_list)):
            if behaviour_list[i][1]== mutation_state:
                if coop_dest==mutation_state: behaviour_list[i][1] =behaviour_list[i][1]
                else : behaviour_list[i][1]= coop_dest
            if behaviour_list[i][2] == mutation_state:
                if defect_dest==mutation_state: behaviour_list[i][2] =behaviour_list[i][2]
                else: behaviour_list[i][2] = defect_dest

        for i in range(mutation_state ,  states + 2): # lol be careful with this stuff it's risky business!
            #we don't want to overwrite the starting info so we start at 2
            for state in behaviour_list: 
                if state[1] == i and i!=1:
                    state[1] =i-1
                if state[2] == i and i!=1:
                    state[2]  = i-1

    elif 9 < mutation < 25 and states < max_states:
        # add a state
        behaviour_list.append([r.randint(0,1), r.randint(1, states + 1), r.randint(1, states + 1)])
    elif 24 < mutation < 45  or 99 < mutation < 121:
        # change the defect joss_ann noise parameters +-0.1
        j1, j2 = (joss_ann_list[0], max(min(joss_ann_list[1] - 0.1 + 0.2 * r.random(), 1.0), 0.0))
        joss_ann_list = (j1, j2)
    elif 120 < mutation < 161:
        # change the  coop joss_ann noise parameters +-0.1
        j1, j2 =(max(min(joss_ann_list[0] - 0.1 + 0.2 * r.random(), 1.0), 0.0),joss_ann_list[1])
        joss_ann_list = (j1, j2)
    elif 44 < mutation < 60:
        # change the state move
        behaviour_list[mutation_state - 1][0] = int(not agent.behaviour[mutation_state - 1][0])
    elif 59 < mutation < 80:
        # change the state coop destination
        behaviour_list[mutation_state - 1][1] = (behaviour_list[mutation_state - 1][1] + r.randint(0, states - 1)) % states + 1
    elif 79 < mutation < 100 :
        # change the state deceive destination
        behaviour_list[mutation_state - 1][2] = (behaviour_list[mutation_state - 1][2] + r.randint(0, states - 1)) % states + 1
    
    offspring=Agent( ID=agent.ID, behaviour=tuple(behaviour_list),joss_ann=tuple(joss_ann_list))
    return offspring

    
def test_generation_logic():
    #TODO: write tests for these functions
    r.seed(13)
    assert len(generate_agents(count = 12, max_states = 4, all_max = True)[5]) == 4 * 3 + 2
    agents=generate_agents(count =64, max_states = 4, all_max = True)
    game = [[3, 3], [0, 5], [5, 0], [1, 1]] 
    w=0.98
    play_round(agents, game, w=w, max_states=6, all_max=False, noise=False)
    run_generation(agents, game, 
                     count = 64, 
                     rounds = 150, w = w,
                     evol =  (24, 23, 1), 
                     start_states = 4,
                     max_states = 6, 
                     all_max = False, 
                     noise = True,
                     last_gen = False) # takes about 480ms
    return 'test passes'

#print test_generation_logic()


