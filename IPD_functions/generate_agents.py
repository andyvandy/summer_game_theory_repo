import random as r

def generate_agents(count = 64, max_states = 8, all_max = False, noise = True):
    # this function generates a list of agents in the following format:
    # {current state}{initial move} 
    # [{move for this state}{new state if coop}{new state if defect}] 
    # for each state

    result = [[] for i in range(count)]

    for i in range(count):
        if all_max: states = max_states
        else: states = r.randint(1, max_states)
        
        # 1 not included but [0,1) is isomorphic to [0,1] luckily! ..right?
        joss_ann_parameters = (r.random(), r.random()) 

        if noise == False:
            joss_ann_parameters = (0, 0)
        # agent=[1,joss_ann_parameters] + sum([[1,1,1] for j in range(states)],
        #  []) 
        # generates only hawks

        # the sum flattens the list 
        agent = [1, joss_ann_parameters] + sum([[r.randint(0,1), 
                                                 r.randint(1, states), 
                                                 r.randint(1, states)] for j in range(states)],
                                                 []) 

        result[i] = agent

        # print agent
        
    return result
    
def test_generate_agents():
    assert len(generate_agents(count = 38)) == 38
    assert generate_agents()[7][1] in [0,1]
    assert len(generate_agents(count = 12, max_states = 4, all_max = True)[5]) == 4 * 3 + 2
    return 'test passes'

#print test_generate_agents()
