import random as r
import numpy as np
from agent_class import *


def init_agents(**params):
    """Creates a list of agents.

    Args:
        number_of_agents: the number of agents to create
        max_turns: the maximum number of rounds

    Returns:
        agent_list: a list of agents
    """

    # Why do I have to do it like this? why can't the nested function see the 
    # kwargs? - Andrew
    # Good question... you implemented this. :P -Stu 
    # lol but srsly if you figure it out lemme know aha -A
    ENDOWMENT = params['ENDOWMENT']
    MEMORY = params['MEMORY']
    B = params['B'] 
    
    agent_list = []
    
    genome_a_rows = ENDOWMENT[0] + 1
    genome_a_columns = MEMORY * (ENDOWMENT[0] * B + 1 + ENDOWMENT[1])
    genome_a_shape = (genome_a_rows, genome_a_columns)
    intial_genome_a = np.zeros(genome_a_shape)

    genome_b_rows = ENDOWMENT[0] * B + 1 + ENDOWMENT[1]
    genome_b_columns = MEMORY * (ENDOWMENT[0] + 1)
    genome_b_shape = (genome_b_rows, genome_b_columns)
    intial_genome_b = np.zeros(genome_b_shape)
    
    for i in range(params['NUMBER_OF_AGENTS']):
        agent_list.append(Agent(intial_genome_a, intial_genome_b, ID = (0, i), 
                                **params))

    return agent_list

def create_offspring(agent, generation, pos, **params):
    ENDOWMENT = params['ENDOWMENT']
    MEMORY = params['MEMORY']
    B = params['B'] 
    new_ID = (generation, pos)
    
    genome_a_rows = ENDOWMENT[0] + 1
    genome_a_columns = MEMORY * (ENDOWMENT[0] * B + 1 + ENDOWMENT[1])
    genome_a_shape = (genome_a_rows, genome_a_columns)
    intial_genome_a = agent.genome_a + np.random.randint(-15, 16, 
                                                         genome_a_shape)

    genome_b_rows = ENDOWMENT[0] * B + 1 + ENDOWMENT[1]
    genome_b_columns = MEMORY * (ENDOWMENT[0] + 1)
    genome_b_shape = (genome_b_rows, genome_b_columns)
    intial_genome_b = agent.genome_b + np.random.randint(-15, 16, 
                                                         genome_b_shape)

    return Agent(intial_genome_a, intial_genome_b, ID = new_ID, 
                 parent_ID = agent.ID, **params)
    

def create_initial_agents(**params):
    """Creates the initial generation of agents.

    Args:
        number_of_agents: the number of agents to create
        max_turns: the maximum number of rounds

    Returns:
        agent_list: a list of agents
    """

    agent_list = init_agents(**params)
    #print ENDOWMENT # probably need to build a decorator to unpack the dicts -a

    return agent_list


def mutate_agents(agent_list, generation, **params):
    """Creates new generation from the agents in agent_list.

    Args:
        agent_list: a list of agents

    Returns:
        new_agent_list: the list of agents for the new generation
    """
    
    MUTATION_PARAMS= params["MUTATION_PARAMS"]
    new_agent_list = []
    
    for i in range(MUTATION_PARAMS[0]):
        new_agent_list.append(agent_list[i])
        new_agent_list.append(create_offspring(agent_list[i], generation, i, 
                              **params))
    #print len(new_agent_list)
    for i in range(MUTATION_PARAMS[1]):
        new_agent_list.append(agent_list[i])
    #print len(new_agent_list)
    params['NUMBER_OF_AGENTS'] = 1
    for i in range(MUTATION_PARAMS[2]):
        new_agent_list.append(init_agents(**params))
    #print len(new_agent_list)
    return new_agent_list
    
    
def generation_test_cases():
    #initializing params
    params={"theta":0.05,
            "NUMBER_OF_AGENTS" : 36,
            "ROUNDS": 100,
            "max_turns":40,
            "B":3,
            "C":1,
            "SWAP" : False, 
            "RESET" : False, 
            "MEMORY" : 2,
            "LOG" : False,
            "ENDOWMENT" : (3,0),
            "MUTATION_PARAMS" : (12,12,0) ,
            }
    ENDOWMENT =params["ENDOWMENT" ]
    MEMORY =params["MEMORY" ]
    B =params["B" ]
            
    #init_agents tests
    assert isinstance(init_agents(**params),tuple)
    assert len(init_agents(**params))==params["NUMBER_OF_AGENTS" ]
    assert shape(init_agents(**params)[4].genome_a) == (ENDOWMENT+1,MEMORY*(B*ENDOWMENT+1))
    assert shape(init_agents(**params)[6].genome_b) == ((B*ENDOWMENT+1),MEMORY*(ENDOWMENT+1))
    
    
    #create_offspring tests
        #initializing test agent
    intial_genome_a_test = np.zeros((ENDOWMENT[0]+1, 
                                MEMORY * ((ENDOWMENT[0]) * B +1 + ENDOWMENT[1])))
    intial_genome_b_test = np.zeros(((ENDOWMENT[0]) * B +1 + ENDOWMENT[1], 
                                MEMORY * (ENDOWMENT[0]+1)))
    test_agent=Agent(intial_genome_a, intial_genome_b, ID = (0, 1), **params)
    
    result_agent =create_offspring( test_agent,1,0,**params)
    
        # running the tests
        #ought to set a seed to test the matrix addition stuff probably
    assert (result_agent.ID , result_agent.parent_ID)== ((0,1),(1,0))
    assert shape(test_agent.genome_a) == (ENDOWMENT+1,MEMORY*(B*ENDOWMENT+1))
    assert shape(test_agent.genome_b) == ((B*ENDOWMENT+1),MEMORY*(ENDOWMENT+1))
    

    #create_initial_agents tests
        #not necessary
    
    #mutate_agents tests
    
    
    print "test pass!"
    
#generation_test_cases():