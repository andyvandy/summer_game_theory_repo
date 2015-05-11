import random as r

def generate_agents(count=64, max_states=8, all_max=False, noise=True):
    """Generates a list of agents.

    Args:
        count: the number of agents to generate
        max_states: the maximum number of states
        all_max: whether or not the agents will all have the maximum number of
            states.
        noise: whether or not to use Joss-Ann noise
    
    Returns:
        result: A list of agents in the following format:
            {current state}{initial move}
            [{move for this state}{new state if coop}{new state if defect}]
            for each state.
    """

    # Create a list of empty lists, length count
    result = [[] for i in range(count)]
    
    # Iterate over the list of agents
    for i in range(count):
        # Set number of states. Could change the distribution of the random 
        # samples to prefer lower number of states.
        if all_max: states = max_states
        else: states = r.randint(1, max_states)
        
        # 1 not included but [0,1) is isomorphic to [0,1] luckily! ..right?
        if noise == False:
            joss_ann_parameters = (0, 0)
        else:
            joss_ann_parameters = (r.random(), r.random())

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
