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

    ENDOWMENT= params['ENDOWMENT']
    MEMORY= params['MEMORY']
    B=params['B'] # why do I have to do it like this? why can't the nested function see the kwargs? -a
    
    agent_list = []
    
    intial_genome_a = np.zeros((ENDOWMENT[0],MEMORY*(ENDOWMENT[0]*B+ENDOWMENT[1])))
    intial_genome_b = np.zeros((ENDOWMENT[0]*B+ENDOWMENT[1],MEMORY*(ENDOWMENT[0])))
    
    for i in range(params['NUMBER_OF_AGENTS']):
        agent_list.append(Agent(intial_genome_a, intial_genome_b, **params))

    return agent_list


def randomize_multipliers(agent_list, max_turns, sigma=1): # do we still need this? -a
    """Adds normally distributed random noise to the multipliers for the agents 
    in agent_list.

    Args:
        agent_list: a list of agents
        sigma: standard deviation of the noise

    Returns:
        agent_list: a list of agents
    """

    for agent in agent_list:
        noise = np.random.normal(0, sigma, max_turns) # not super clear if we still need this
        agent.multipliers += noise

    return agent_list


def randomize_shifts(agent_list, max_turns, sigma=0.1):# do we still need this? -a
    """Adds normally distributed random noise to the shifts for the agents in
    agent_list.

    Args:
        agent_list: a list of agents
        sigma: standard deviation of the noise

    Returns:
        agent_list: a list of agents
    """

    for agent in agent_list:
        noise = np.random.normal(0, sigma, max_turns)
        agent.multipliers += noise

    return agent_list


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

    #agent_list = randomize_multipliers(agent_list,params[ 'max_turns'], 1) # do we still use these ? -a
    #agent_list = randomize_shifts(agent_list, params[ 'max_turns'], 0.1)

    return agent_list


def mutate_agents(agent_list, **params):
    """Creates new generation from the agents in agent_list.

    Args:
        agent_list: a list of agents

    Returns:
        new_agent_list: a list of agents twice the size of agent_list
    """
    return agent_list #temporary while we get the other stuff working
    new_agent_list = []

    for agent in agent_list:
        new_agent_list.append(agent)
        new_agent_list.append(agent)

    new_agent_list = randomize_multipliers(new_agent_list, params[max_turns], 
                                           sigma = 0.1)
    new_agent_list = randomize_shifts(new_agent_list, params[max_turns], 
                                      sigma = 0.01)

    return new_agent_list