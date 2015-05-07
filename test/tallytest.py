import random as r
import json                     # for d3 drawing
import networkx as nx           # for making graphs
from networkx.readwrite import json_graph #more d3
from sys import exit

def tally_score(moves,game):
    #returns the agents' respective scores
    R1,S1,T1,P1=game[0][0],game[1][0],game[2][0],game[3][0]
    R2,T2,S2,P2=game[0][1],game[1][1],game[2][1],game[3][1]
    score1= moves.count((0,0))*R1+moves.count((0,1))*S1+moves.count((1,0))*T1+moves.count((1,1))*P1
    score2= moves.count((0,0))*R2+moves.count((1,0))*S2+moves.count((0,1))*T2+moves.count((1,1))*P2 
    return (score1,score2)




    
def test():
    game=[[3,3],[0,5],[5,0],[1,1]] 
    moves1=((0,1),(0,0))
    moves2=((0,0),(0,0),(0,0),(0,0))
    moves3=((0,1),(1,0),(1,0),(1,1),(0,0))
    assert tally_score(moves1, game) == (3,8)
    assert tally_score(moves2, game) == (12,12)
    assert tally_score(moves3, game) == (14,9)
    return 'test passes'

print test()