
def count_agents(coord,agents):
    #returns number of agents at given coord
    return len(agents_in_cell(coord,agents))

def agents_in_cell(coord,agents):
    #returns a list of all agents at a given coord
    result=[]
    for agent in agents:
        if agent.location==coord: result.append(agent)
    return result    
    
def tally_energy(agents,resources,coordinates):
    #returns the net sum of energy among all agents
    agent_energy=0
    for agent in agents:
        agent_energy+= agent.energy
    available_energy= sum([resources[coord] for coord in coordinates])
    return agent_energy,available_energy
