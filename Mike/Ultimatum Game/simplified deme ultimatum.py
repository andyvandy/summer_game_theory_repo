
import random
from operator import itemgetter



# PARAMETERS FOR THE GAME

DEME_SIZE = 50 # size of demes
POPULATION_SIZE = 100 # Population size
NUMBER_OF_GENERATIONS = 5000 # Number of generations
RATE_OF_EVOLUTION = 1 # Number of new members introduced/killed in the population after each generation
BONUS = 1 # Bonus multiplier
MIGRATION_RATE = 0.1
BASELINE_FITNESS = 1
ENDOWMENT = 100
MUTATION_RATE = 0.02
counter = 0
gen = 0

class Player():
        def __init__(self):
                self.give = random.randint(0,ENDOWMENT)
                self.ultim = random.randint(0,ENDOWMENT)*BONUS
                self.bank = 0

def make_player(i):
        p = Player()
        deme = i % (POPULATION_SIZE/DEME_SIZE)
        birth_prob = 0.00
        player = [p.give, p.ultim, p.bank, deme, birth_prob, i]
        return player

Population =[]        
for i in range(POPULATION_SIZE):
        counter = counter + 1
        Population.append(make_player(i))

def game(p1,p2):
    gift = p1[0]
    ultimatum = p2[1]
    if BONUS*gift < ultimatum:
        p1[2] = p1[2] + 0
        p2[2] = p2[2] + 0
    if BONUS*gift >= ultimatum:
        p1[2] = p1[2] + ENDOWMENT - gift
        p2[2] = p2[2] + BONUS*gift
    gift2 = p2[0]
    ultimatum2 = p1[1]
    if BONUS*gift2 < ultimatum2:
        p1[2] = p1[2] + 0
        p2[2] = p2[2] + 0
    if BONUS*gift2 >= ultimatum2:
        p2[2] = p2[2] + ENDOWMENT - gift2
        p1[2] = p1[2] + BONUS*gift2       
    return p1[2], p2[2]


def Generation(popu):
    for k in range(len(popu)):
            player1 = popu[k]
            for i in range(len(popu)):
                player2 = popu[i]
                if player1[3] == player2[3] and player1[5] != player2[5]:
                    game(player1, player2)
            player1[2] = player1[2]/DEME_SIZE + BASELINE_FITNESS
    return popu


TOTAL_FITNESS = 0

def birth_selection(popu):
    global TOTAL_FITNESS
    for i in range(len(popu)):
        TOTAL_FITNESS =  TOTAL_FITNESS + popu[i][2]
    for j in range(len(popu)):
        popu[j][4] = popu[j][2]*1.0 / TOTAL_FITNESS
    selection = random.random()
    upto = 0.0
    mother = []
    TOTAL_FITNESS = 0
    for k in popu:
        if selection <= k[4]:
            return k
        selection -= k[4]


def replacement(popu):
    global counter
    mother = birth_selection(popu)
    deme_selection = random.random()
    maternal_deme = []
    external_deme = []
    for member in popu:
        member[2] = 0
        member[4] = 0.0
        if member[3] == mother[3]:
            maternal_deme.append(member)
        else:
            external_deme.append(member)
    if deme_selection <= MIGRATION_RATE:
        #This means that there is a migratory birth. we need to have a random choice from all the members of the population that are in a different deme than the mother
        death = random.choice(external_deme)
    else:
        death = random.choice(maternal_deme)
    mutation = random.random()
    if mutation >= MUTATION_RATE:
        death[0] = mother[0]
        death[1] = mother[1]
    else:
        death[0] = random.randint(0,ENDOWMENT)
        death[1] = random.randint(0,ENDOWMENT)*BONUS    
    death[5] = counter
    counter = counter + 1
    mother = []
    return popu


##print replacement(Generation(Population))

def Update(popu):
    replacement(Generation(popu))
    return popu

def Simulation(popu):
    for i in range(NUMBER_OF_GENERATIONS):
        Update(popu)
    return popu


sorted_population = tuple(sorted(Simulation(Population), key = itemgetter(3)))

for elem in sorted_population:
    print elem



##for elem in Population:
##    print elem
##for elem in Generation(Population):
##    print elem
##for elem in Update(Population):
##    print elem
##
##print Simulation(Population)
