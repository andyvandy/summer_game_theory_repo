import random as r

def generate_agents(count= 64 , maxStates=8,allMax=False):
    # this function generates a list of agents in the following format:
    #    {current state}{initial move} [{move for this state}{new state if coop}{new state if defect}] for each state
    result=[[] for i in range(count)]
    for i in range(count):
        if allMax: states=maxStates
        else: states=r.randint(1,maxStates)
        #agent=[1,r.randint(0,1)] +sum([[r.randint(0,1),r.randint(1,states),r.randint(1,states)] for j in range(states)], []) # the sum flattens the list        
        agent=[1,r.randint(0,1)] +sum([[1,1,1] for j in range(states)], []) #hawks
        result[i]=agent
        
    return result
    
def test_generate_agents():
    assert len(generate_agents(count= 38)) == 38
    assert generate_agents()[7][1] in [0,1]
    assert len(generate_agents(count= 12,maxStates=4,allMax=True)[5]) == 4*3+2
    return 'test passes'

#print test_generate_agents()