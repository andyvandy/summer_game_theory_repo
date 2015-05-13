#import burtsev001



def count_agents(coord,agents):
    #returns number of agents at given coord
    return len(agents_in_cell(coord,agents))

def agents_in_cell(coord,agents):
    #returns a list of all agents at a given coord
    result=[]
    for agent in agents:
        if agent.location==coord: result.append(agent)
    return result    
