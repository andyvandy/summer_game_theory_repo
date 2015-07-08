
import random
from operator import itemgetter

N = 25 # Population size
R = 5 # number of games per match
B1 = 2 # bonus to the initial gift
B2 = 2 # bonus to the returned gift
G = 100 # number of generations
S = 7 # number of new players introduced/killed off in each generation




#Initial values of some global variables
gen = 0
Average = []
counter = 0
Population =[]


#Define the player class
class Player():
        def __init__(self):
                self.gives = random.random()
                self.returns = random.random()
                self.bank = 0


#make a function that generates a random player            
def make_player(i):
        p = Player()
        player = [p.gives, p.returns, p.bank, i+1]
        return player


# Creating the initial population        
for i in range(N):
        counter = counter + 1
        Population.append(make_player(i))


# Playing a game
def play_game(player1, player2):
    gofirst = random.randint(1,2)
    if gofirst == 1:
        gift = player1[0]
        returned = gift*B1*player2[1]
        player1[2] = player1[2] + 1 - gift + B2*returned
        player2[2] = player2[2] + B1*gift - returned
    if gofirst == 2:
        gift = player2[0]
        returned = gift*B1*player1[1]
        player2[2] = player2[2] + 1 - gift + B2*returned
        player1[2] = player1[2] + B1*gift - returned
    return player1[2], player2[2]
    

#Playing a match
def match(player1,player2):
    numrounds = R
    i=1
    while i <= numrounds:
        play_game(player1,player2)
        i=i+1
    return player1[2], player2[2]

#Updating the population after a series of matches
def Update(sortpop):
        global counter
        global gen
        global Average
        #global S
        sumgifts = 0
        sumulti=0
        poppy = list(sortpop)
        for i in range(N):
                sumgifts = sumgifts + sortpop[i][0]
                sumulti = sumulti + sortpop[i][1]
        Average.append((sumgifts/ N, sumulti/N))
        for i in range(S):
                poppy[i] = make_player(counter + 1 + i)
        for i in range(N):
                poppy[i][2]=0
        counter = counter + S
        #S = S - 1
        gen = gen + 1
        return poppy


# One generation: every one plays everyone else
# population is updated depending on the results

def Generation(popu):
        for k in range(len(popu)):
                p1 = popu[k]
                for i in range(len(popu)):
                        p2= popu[i]
                        match(p1, p2)
        sorted_population = tuple(sorted(popu, key = itemgetter(2)))
        popu = Update(sorted_population)
        return popu


#Runs the whole simulation (for the given number of generations)
def Simulation(popu):
        for i in range(G):
                popu = Generation(popu)
                i = i+1
        return popu


     
#Gives us back our results
    
for elem in Simulation(Population):
    print elem

for elem in Average:
        print elem[0]
print "**************"
for elem in Average:        
        print elem[1]


