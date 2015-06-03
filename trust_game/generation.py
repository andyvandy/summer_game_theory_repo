import random as r
import numpy as np
from agent_class import *


def init_agents(number_of_agents, max_rounds):
    """Creates a list of agents.

    Args:
        number_of_agents: the number of agents to create
        max_rounds: the maximum number of rounds

    Returns:
        agent_list: a list of agents
    """

    agent_list = []

    for i in range(number_of_agents):
        agent_list.append(Agent(max_rounds = max_rounds))

    return agent_list


def randomize_multipliers(agent_list, max_rounds, sigma=1):
    """Adds normally distributed random noise to the multipliers for the agents 
    in agent_list.

    Args:
        agent_list: a list of agents
        sigma: standard deviation of the noise

    Returns:
        agent_list: a list of agents
    """

    for agent in agent_list:
        noise = np.random.normal(0, sigma, max_rounds)
        agent.multipliers += noise

    return agent_list


def randomize_shifts(agent_list, max_rounds, sigma=0.1):
    """Adds normally distributed random noise to the shifts for the agents in
    agent_list.

    Args:
        agent_list: a list of agents
        sigma: standard deviation of the noise

    Returns:
        agent_list: a list of agents
    """

    for agent in agent_list:
        noise = np.random.normal(0, sigma, max_rounds)
        agent.multipliers += noise

    return agent_list


def create_initial_agents(number_of_agents, max_rounds):
    """Creates the initial generation of agents.

    Args:
        number_of_agents: the number of agents to create
        max_rounds: the maximum number of rounds

    Returns:
        agent_list: a list of agents
    """

    agent_list = init_agents(number_of_agents, max_rounds)

    agent_list = randomize_multipliers(agent_list, max_rounds, 1)
    agent_list = randomize_shifts(agent_list, max_rounds, 0.1)

    return agent_list


def mutate_agents(agent_list, max_rounds):
    """Creates new generation from the agents in agent_list.

    Args:
        agent_list: a list of agents

    Returns:
        new_agent_list: a list of agents twice the size of agent_list
    """

    new_agent_list = []

    for agent in agent_list:
        new_agent_list.append(agent)
        new_agent_list.append(agent)

    new_agent_list = randomize_multipliers(new_agent_list, max_rounds, 
                                           sigma = 0.1):
    new_agent_list = randomize_shifts(new_agent_list, max_rounds, 
                                      sigma = 0.01)

    return new_agent_list