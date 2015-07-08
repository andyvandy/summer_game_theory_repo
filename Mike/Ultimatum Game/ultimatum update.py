import random
from operator import itemgetter
N = 100
R=10

class Player():
        def __init__(self):
                self.give = random.randint(1,100)
                self.ultim = random.randint(1,100)
                self.bank = 0
            
def make_player(i):
        p = Player()
        player = [p.give, p.ultim, p.bank, i]
        return player

Population =[]        
for i in range(N):
        Population.append(make_player(i))

sorted_population = tuple(sorted(Population, key = itemgetter(1)))
print sorted_population




sum=0
for i in range(N):
    sum = sum + Population[i][1]

averagegift = sum/N

print averagegift
