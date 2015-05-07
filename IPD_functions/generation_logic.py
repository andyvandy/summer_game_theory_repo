import random as r
from IPD_utilities import *
from generate_agents import *

from game_logic import *

def play_round(agents,game,w=0.9,maxStates=8,allMax=False,noise=0.05):
    # need to check the shuffling closely to make sure everything is going alright, could also likely be sped up
    #takes as input a list of agents and a game length parameter and pairs agents off to go play a game so that each agent plays one game per round
    #all games are of the same length in a given round, the strategies shouldn't be affected.
    #returns a list of scores in the same order as the list of agents was given.
    shuffledNumbers=range(len(agents))
    r.shuffle(shuffledNumbers)
    orderAssignment=zip(agents,shuffledNumbers)
    #print orderAssignment
    scores=[0]*len(agents)
    turns= int(round(r.expovariate(1-w)))+1 #calculates how many turns for the round using an exponential distribution
    for i in [2*j for j in range(len(agents)/2)]:
        index1,index2=[y[1] for y in orderAssignment].index(i),[y[1] for y in orderAssignment].index(i+1)
        (player1,player2)=orderAssignment[index1][0],orderAssignment[index2][0]
        (scores[index1],scores[index2])=play_game(player1,player2,game,turns=turns,noise=noise)
        
    return (scores,turns+1) # since the first turn in games isn't counted
    
def run_generation(agents,game,evol,count=64,rounds=100,w=0.9,maxStates=8,allMax=False,startStates=2,noise=0.05,lastGen=False):
    #returns a tuple, feeds into run_simulation
    scores=[0]*len(agents)
    #for agent in agents:
    #    print agent
    
    turnCount=0
    for i in range(rounds):
        roundScores,numberTurns= play_round(agents,game,w=w,allMax=allMax,maxStates=maxStates,noise=noise)
        scores=[x + y for x, y in zip(scores, roundScores)]
        turnCount+=numberTurns
    #print agents,scores
    results=zip(agents,scores) 
    #for result in results: print result
    results.sort(key=getKey,reverse=True) #highest scores first
    #for result in results: print result
    topScores=[]
    winners=[]
    offspringses=[]
    average=[]
    if lastGen:next_gen,topScores=[x[0] for x in results],[x[1] for x in results]
        
        
   
        
    avgScore=float(sum(scores))/(count*turnCount)
    #print avgScore
    # should return all stats in one tuple, preferably a labelled one
    battingAvg=[float(x)/turnCount for x in topScores]
    if lastGen:return (next_gen,topScores,(avgScore,battingAvg))
    for i in range(evol[0]):
        winner=results[i][0]
        winners.append(winner) 
        topScores.append(results[i][1]) # check
        offspring =reproduce(winner,allMax=allMax,maxStates=maxStates)
        offspringses.append(offspring) 
    for i in range(evol[0],count-evol[0]-evol[2]):
        average.append(results[i][0]) 
        topScores.append(results[i][1])
    next_gen=winners+average+offspringses
    next_gen+=generate_agents(count= evol[2] , maxStates=startStates,allMax=True)
    #print len(next_gen)
    #print next_gen
    #raw_input('Press <ENTER> to continue')
    return (next_gen,topScores,(avgScore,battingAvg))    

def reproduce(agent,allMax=False,maxStates=8):
    # returns a mutated offspring
    listAgent=[i for i in agent]
    states= (len(agent)-2)/3
    mutation=r.randint(0,199)
    mutationState=r.randint(1,states)
    if 25<mutation<35 and states>1:
        #remove a state
        defectDest=listAgent.pop((mutationState)*3+1) # be careful with this stuff it can break super easily :'(
        coopDest=listAgent.pop((mutationState)*3)
        listAgent.pop((mutationState)*3-1)
        for index in range(len(listAgent)):
            if listAgent[index]==mutationState:
                if index%3 ==0 and index>1: 
                    if mutationState != coopDest:listAgent[index]=coopDest
                    else: listAgent[index]= index/3
                elif index%3==1  and index>1: 
                    #this is needed or esle the actions will be overwritten
                    if mutationState != defectDest: listAgent[index]=defectDest
                    else: listAgent[index]= index/3
        for i in range(mutationState+1,  states+2):
            for index in range(2,len(listAgent)): #we don't want to overwrite the starting info so we start at 2
                if listAgent[index]==i :
                    #print "guh"
                    #print listAgent[index],index,i
                    listAgent[index]-=1
    elif 34<mutation<50 and states<maxStates:
        #add a state
        listAgent+= [r.randint(0,1),r.randint(1,states+1),r.randint(1,states+1)] 
    elif 49<mutation <55 and False:
        # change the initial move
        listAgent[2]= 1-listAgent[1]
        #print"test"
    elif 54<mutation<70:
        # change the state move
        listAgent[mutationState*3 -1] = int(not listAgent[mutationState*3 -1])
    elif 69<mutation<90:
        # change the state coop destination
        listAgent[mutationState*3 ]= (listAgent[mutationState*3]+r.randint(0,states-1))%states +1
    elif 89<mutation <100 or 0<mutation <10 :
        # change the state deceive destination
        listAgent[mutationState*3 +1]= (listAgent[mutationState*3+1]+r.randint(0,states-1))%states +1
    #agent = "".join(map(str, listAgent))
    
    return listAgent

    
def test_generation_logic():
    #TODO: write tests for these functions
    r.seed(13)
    assert len(generate_agents(count= 12,maxStates=4,allMax=True)[5]) == 4*3+2
    return 'test passes'

#print test_generation_logic()
    
