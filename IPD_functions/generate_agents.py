import random as r
from class_definitions import Agent

def generate_agents(count=64, max_states=8, all_max=False, noise=True):
    """Generates a list of agents.

    Args:
        count: the number of agents to generate
        max_states: the maximum number of states
        all_max: whether or not the agents will all have the maximum number of
            states.
        noise: whether or not to use Joss-Ann noise
    
    Returns:
        result: A list of agent objects
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
        
        # the following block must be rewritten before use with agent objects:
        # agent=[1,joss_ann_parameters] + sum([[1,1,1] for j in range(states)],
        #  []) 
        # generates only hawks
        
        behaviour = []
        for j in range(states):
            behaviour.append([r.randint(0, 1), 
                              r.randint(1, states), 
                              r.randint(1, states)])
        
        agent = Agent((1, i), behaviour, joss_ann_parameters)

        result[i] = agent
        
    return result
    
def test_generate_agents(): 
    """Runs some test cases for the agent generator.
    
    Returns:
        'test passes': string is returned unless a test fails
    """
    
    # Assures that the expected number of agents is generated.
    assert len(generate_agents(count = 38)) == 38
    
    # Asserts that the Joss-Ann noise is correctly disabled.
    assert generate_agents(noise=False)[7].joss_ann[0] in [0,1]

    # Asserts that the behavior list for an agent is the correct length.
    test_list = generate_agents(count = 12, max_states = 4, all_max = True)
    test_agent = test_list[5]
    assert len(test_agent.behaviour) == 4
    return 'test passes'

#print test_generate_agents()
