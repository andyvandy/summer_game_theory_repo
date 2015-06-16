import random
from operator import itemgetter

N = 5 # Population size
R = 5 # number of games per match
B1 = 2 # bonus to the initial gift
B2 = 2 # bonus to the returned gift
G = 10 # number of generations
S = 7 # number of new players introduced/killed off in each generation




#Initial values of some global variables
gen = 0
Average = []
counter = 0
Population =[]


#Define the player class
class Player():
        def __init__(self):
                self.gives = random.randint(0,1)
                self.returns = random.randint(1,3)
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


print Population
p1 = [1,1,0,1]
p2 = Population[1]

print p1,p2


gofirst = random.randint(1,2)

print "Player " + str(gofirst) + " plays first."
def play_game(player1, player2):
    global gofirst
    if (gofirst % 2 == 0):
        p2 = player1
        p1 = player2
        gofirst = gofirst + 1
    else:
        p2 = player2
        p1 = player1
        gofirst = gofirst + 1

    gift = p1[0]
    if gift == 0:
        p1[2] = p1[2] + 1
        p2[2] = p2[2]
        if p2[1] == 1:
            p2[0] = p1[0]
    if gift == 1:
        p1[2] = 5
        p2[2] = 4
    return p1, p2


print play_game(p1,p2)




