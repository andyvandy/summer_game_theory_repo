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
    ENDOWMENT= params['ENDOWMENT']
    MEMORY= params['MEMORY']
    B=params['B'] 
    
    agent_list = []
    
    intial_genome_a = np.zeros((ENDOWMENT[0], 
                                MEMORY * (ENDOWMENT[0] * B + ENDOWMENT[1])))

    intial_genome_b = np.zeros((ENDOWMENT[0] * B + ENDOWMENT[1], 
                                MEMORY * (ENDOWMENT[0])))
    
    for i in range(params['NUMBER_OF_AGENTS']):
        agent_list.append(Agent(intial_genome_a, intial_genome_b, ID = (0, i), 
                                **params))

    return agent_list

def create_offspring(agent,**params):
    ENDOWMENT= params['ENDOWMENT']
    MEMORY= params['MEMORY']
    B=params['B'] 
    
    
    intial_genome_a = agent.genome_a + np.random.randint(-15,16,(ENDOWMENT[0],MEMORY*(ENDOWMENT[0]*B+ENDOWMENT[1])))
    intial_genome_b = agent.genome_b +np.random.randint(-15,16,(ENDOWMENT[0]*B+ENDOWMENT[1],MEMORY*(ENDOWMENT[0])))
    retunr Agent(intial_genome_a, intial_genome_b, **params)
    
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


def mutate_agents(agent_list, **params):
    """Creates new generation from the agents in agent_list.

    Args:
        agent_list: a list of agents

    Returns:
        new_agent_list: a list of agents twice the size of agent_list
    """
    
    MUTATION_PARAMS= params[MUTATION_PARAMS]
    return agent_list #temporary while we get the other stuff working
    new_agent_list = []
    
    for i in range(MUTATION_PARAMS[0]):
        new_agent_list.append(agent_list[i])
        new_agent_list.append(create_offspring(agent,**params))
    
    for agent in agent_list:
        new_agent_list.append(agent)
        new_agent_list.append(agent)

    new_agent_list = randomize_multipliers(new_agent_list, params[max_turns], 
                                           sigma = 0.1)
    new_agent_list = randomize_shifts(new_agent_list, params[max_turns], 
                                      sigma = 0.01)

    return new_agent_list