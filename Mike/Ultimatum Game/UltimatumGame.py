
import random
from operator import itemgetter

# PARAMETERS FOR THE GAME

N = 30 # Population size

G = 5000 # Number of generations
S = 1 # Number of new members introduced/killed in the population after each generation
delta = 0.8 # probability of playing again
A = 3
#Type 1: Stay the course
#Always stick to their guns

#Type 2: TFT
#If they play first, they'll give the normal amount
# if they play second, then in the next instance of the game
# they will offer what their partner offered in the previous round

#Type 3: Adapter
# If they play first and their offer is rejected, they will increase it in the following round
# If they play first and their offer is accepted, they will decrease it in the following round
# If they play second and reject an offer, then they will decrease ultimatum value next round


#Type 4: Punisher
# If the first offer is too low, they will try to keep everything (i.e. their own offer becomes 0,0)


counter = 0
gen = 0

##Average = []

class Player():
        def __init__(self):
                self.give = random.randint(0,100)
                self.ultim = random.randint(0,100)
                self.bank = 0
                self.giftmemory = []
                self.ultimmemory = []
                self.type = random.randint(1,4)

def create_player(i):
    p = Player()
    player = [p.give, p.ultim, p.bank, p.giftmemory, p.ultimmemory, p.type,i+1]
    player[3].append(player[0])
    player[4].append(player[1])
    if p.type == 1:
        player.append("Stay the course")
    if p.type == 2:
        player.append("TFT")
    if p.type ==3:
        player.append("Adapter")
    if p.type ==4:
        player.append("Punisher")
    return player

def make_type(i, types):
    p = Player()
    player = [p.give, p.ultim, p.bank, p.giftmemory, p.ultimmemory, types, i+1]
    player[3].append(player[0])
    player[4].append(player[1])
    if types == 1:
        player.append("Stay the course")
    if types == 2:
        player.append("TFT")
    if types ==3:
        player.append("Adapter")
    if types ==4:
        player.append("Punisher")
    return player


Population =[]        
for i in range(N):
        counter = counter + 1
        Population.append(make_type(i,1))

def play_game(p1,p2):
    gofirst = random.randint(1,2)
    while random.random()<=delta:
        if (gofirst % 2 == 0):
            gofirst = gofirst + 1
            gift = p1[3][-1]
            ultimatum = p2[4][-1]
            if gift >= ultimatum:
                p1[2] += 100 - gift
                p2[2] += gift
                if p1[5] == 3:
                    p1[3].append(max(gift - A,0))
                if p2[5] ==2:
                    p2[3].append(gift)          
            else:
                p1[2] = p1[2]
                p2[2] = p2[2]
                if p1[5] ==3:
                    p1[3].append(min(gift + A,100))
                if p2[5] ==3:
                    p2[4].append(max(ultimatum - A,0))
                if p2[5] ==4:
                    p2[3].append(0)
                if p2[5] == 2:
                    p2[3].append(gift)
        else:
            gofirst = gofirst + 1
            gift = p2[3][-1]
            ultimatum = p1[4][-1]
            if gift >= ultimatum:
                p2[2] += 100 - gift
                p1[2] += gift
                if p2[5] == 3:
                    p2[3].append(max(gift - A,0))
                if p1[5] ==2:
                    p1[3].append(gift)          
            else:
                p2[2] = p2[2]
                p1[2] = p1[2]
                if p2[5] ==3:
                    p2[3].append(min(gift + A,100))
                if p1[5] ==3:
                    p1[4].append(max(ultimatum - A,0))
                if p1[5] ==4:
                    p1[3].append(0)
                if p1[5] == 2:
                    p1[3].append(gift)

    p1[3]= [p1[0]]
    p2[3]= [p2[0]]
    p1[4] = [p1[1]]
    p2[4] = [p2[1]]
    return p1,p2

def Generation(popu):
        for k in range(len(popu)):
                p1 = popu[k]
                for i in range(len(popu)):
                        p2= popu[i]
                        play_game(p1, p2)
        sorted_population = tuple(sorted(popu, key = itemgetter(2)))
        popu = Update(sorted_population)
        return popu

def Update(sortpop):
        global counter
        global gen
##        global Average
        #global S
        sumgifts = 0
        sumulti=0
        poppy = list(sortpop)
##        for i in range(N):
##                sumgifts = sumgifts + sortpop[i][0]
##                sumulti = sumulti + sortpop[i][1]
##        Average.append((sumgifts/ N, sumulti/N))
        for i in range(S):
                poppy[i] = create_player(counter + 1 + i)
        for i in range(N):
                poppy[i][2]= 0
                poppy[i][3] = [poppy[i][0]]
                poppy[i][4] = [poppy[i][1]]
        counter = counter + S
        #S = S - 1
        gen = gen + 1
        return poppy

def Simulation(popu):
        for i in range(G):
            popu = Generation(popu)
        return popu

for elem in Simulation(Population):
    print elem

