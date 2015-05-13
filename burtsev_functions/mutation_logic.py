import random as r

def mutate_phenotype(agent,mutation_intensity,wmax):
    mutation=[r.randint(-mutation_intensity,mutation_intensity+1) for i in range(9)] #low is inclusive, high is exclusive
    offspring_phenotype= tuple( [min(wmax,max(0,agent.phenotype[i]+mutation[i])) for i in range(9)])    
    return offspring_phenotype
    

    
class TestAgent:
    def __init__(self,parent_genes,initial_location,initial_energy,phenotype,parent_direction):
        self.location = initial_location
        self.genes=parent_genes  
        self.energy = initial_energy
        self.phenotype=phenotype
        self.direction=parent_direction 

def test_mutation_logic():
    agent =TestAgent(parent_genes=6,
                        initial_location=6,
                         initial_energy=100, #p0007
                         phenotype=(255,255,150,150,255,255,255,150,255),
                         parent_direction=6)

    for i in range(100):
        agent.phenotype=mutate_phenotype(agent,30)
        print agent.phenotype
        
#test_mutation_logic()