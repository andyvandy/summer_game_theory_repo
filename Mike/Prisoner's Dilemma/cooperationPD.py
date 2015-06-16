import random
from operator import itemgetter

N = 5 # Population size
R = 5 # number of games per match
G = 10 # number of generations
S = 3 # number of new players introduced/killed off in each generation

counter = 1
Population = []

#Define the player class
class Player():
        def __init__(self):
                self.firstplay = random.randint(0,1)
                self.bank = 0
                self.history = []
                self.game_number = 0


def make_player(i):
        p = Player()
        player = [p.firstplay, p.bank, p.history, p.game_number, i+1]
        return player


for i in range(N):
        counter = counter + 1
        Population.append(make_player(i))


print Population

def play_game(player1, player2):
    if player1[3] ==0:
        player1[3] +=1
        player2[3] +=1
        if player1[0] == 1 and player2[0] ==1:
            player1[2].append(1)
            player2[2].append(1)
            player1[1] = player1[1] + 3
            player2[1] = player2[1] + 3
        if player1[0] == 1 and player2[0] == 0:
            player1[2].append(0)
            player2[2].append(1)
            player1[1] = player1[1] + 0
            player2[1] = player2[1] + 5
        if player1[0] ==0 and player2[0] == 1:
            player1[2].append(1)
            player2[2].append(0)
            player1[1] = player1[1] + 5
            player2[1] = player2[1] + 0
        if player1[0] == 0 and player2[0] == 0:
            player1[2].append(0)
            player2[2].append(0)
            player1[1] = player1[1] + 1
            player2[1] = player2[1] + 1
    return player1, player2

print play_game(Population[0], Population[1])
