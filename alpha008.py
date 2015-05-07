import random as r
import json                     # for d3 drawing
import networkx as nx           # for making graphs
from networkx.readwrite import json_graph #more d3
import http_server  #more d3
from sys import exit
#import pylab
import matplotlib.pyplot as plt
import seaborn as sns

"""notes 
    required libraries:
        json, random, http_server
        networkx : for the graphs
        matplotlib : for charts
        seaborn : for pretty charts
        
    required files:
        http_server.py
        graph006template.html
    
    Most parameters are in the main function, though the mutation logic is contained in reproduce()
    -1 is defect, 0 is cooperate throughout the code
    
    If something doesn't make sense please tell me!
    -Andrew van den Hoeven
    """

def main():
    game_matrix=[[3,3],[0,5],[5,0],[1,1]] 
    number_of_agents=64
    maxStates=8
    startStates=2
    allMax=True # whether or not all agents will have the max number of states
    rounds=150
    generations=1000
    w=0.98 #probability of game going on another turn
    noise=0.05 # % of moves which are incorrectly played/transmitted ect
    evolution_settings=(25,23,2) #(breed,die,newcommers)
    
    agents=generate_agents(count= number_of_agents , maxStates=startStates,allMax=True)
    (result,ranks,stats)= run_simulation(agents,game=game_matrix,count=number_of_agents, evol=evolution_settings, rounds=rounds,w=w,generations=generations,startStates=startStates,maxStates=maxStates,allMax=allMax)
    simulationResults=zip(result,ranks,stats[1])
    prettyPrint(simulationResults,entriesPerLine=2)

    topAgent=result[0]
    print topAgent, ranks[0]
    drawToBrowser(result,stats)
    

def prettyPrint(list,entriesPerLine=4):
    #prints out agents to console in a non-barbaric fashion, does not return outuput
    liNums = range(len(list))
    x = 0
    line = ""
    for i in liNums:
        x+=1
        line += str(list[i]) +"    "
        if not x%entriesPerLine:
            line += "\n"
    #send line to output, here I will just print it
    print line
    
    
def generate_agents(count= 64 , maxStates=8,allMax=False):
    # this function generates a list of agents in the following format:
    #    {current state}{initial move} [{move for this state}{new state if coop}{new state if defect}] for each state
    result=[]
    for i in range(count):
        if allMax: states=maxStates
        else: states=r.randint(1,maxStates)
        agent=[1,r.randint(0,1)] +sum([[r.randint(0,1),r.randint(1,states),r.randint(1,states)] for j in range(states)], []) # the sum flattens the list
        
        #agent=[1,r.randint(0,1)] +sum([[1,1,1] for j in range(states)], []) #hawks
        result.append("".join(map(str, agent)))
    return result

def play_game(agent1,agent2,game,turns=100,allMax=False):
    # takes as input two agent strategies as strings returns their respective scores
    player1=[int(i) for i in agent1]
    player2=[int(i) for i in agent2]
    moves=[(player1[2],player2[2])]
    #print player1
    #print player2
    for i in range(turns):
        #the states are updated based off of the other agent's last move
        #print moves[i]
        try:player1[0]=player1[player1[0]*3+moves[-1][1]]
        except: 
            #used for debugging faulty mutation mechanism
            # the first number can vary here as it is used to track the player's current state
            print"check your mutation logic"
            print "p1", player1
            print "p2",player2
            print moves[-1][1]
            print moves
            exit("error occurred in play_game")
        try:player2[0]=player2[player2[0]*3+moves[-1][0]]
        except: 
            print"check your mutation logic"
            print "p1", player1
            print "p2",player2
            print moves[-1][0]
            print moves
            exit("error occurred in play_game")
        try:moves.append((player1[player1[0]*3-1],player2[player2[0]*3-1]))
        except: 
            print"check your mutation logic"
            print player1,player2
            exit("error occurred in play_game")
    return(tally_score(moves,game))    
       
def tally_score(moves,game):
    #returns the agents' respective scores
    R1,S1,T1,P1=game[0][0],game[1][0],game[2][0],game[3][0]
    R2,T2,S2,P2=game[0][1],game[1][1],game[2][1],game[3][1]
    score1= moves.count((0,0))*R1+moves.count((0,1))*S1+moves.count((1,0))*T1+moves.count((1,1))*P1
    score2= moves.count((0,0))*R2+moves.count((1,0))*S2+moves.count((0,1))*T2+moves.count((1,1))*P2 
    return (score1,score2)

def play_round(agents,game,w=0.9,maxStates=8,allMax=False):
    # need to check the shuffling closely to make sure everything is going alright, could also likely be sped up
    #takes as input a list of agents and a game length parameter and pairs agents off to go play a game so that each agent plays one game per round
    #all games are of the same length in a given round, the strategies shouldn't be affected.
    #returns a list of scores in the same order as the list of agents was given.
    shuffledNumbers=range(len(agents))
    r.shuffle(shuffledNumbers)
    orderAssignment=zip(agents,shuffledNumbers)
    scores=[0]*len(agents)
    turns= int(round(r.expovariate(1-w)))+1 #calculates how many turns for the round using an exponential distribution
    for i in [2*j for j in range(len(agents)/2)]:
        index1,index2=[y[1] for y in orderAssignment].index(i),[y[1] for y in orderAssignment].index(i+1)
        (player1,player2)=orderAssignment[index1][0],orderAssignment[index2][0]
        (scores[index1],scores[index2])=play_game(player1,player2,game,turns=turns)
    
    return (scores,turns+1) # since the first turn in games isn't counted

def run_generation(agents,game,evol,count=64,rounds=100,w=0.9,maxStates=8,allMax=False,startStates=2):
    #returns a tuple, feeds into run_simulation
    scores=[0]*len(agents)
    turnCount=0
    for i in range(rounds):
        roundScores,numberTurns= play_round(agents,game,w=w,allMax=allMax,maxStates=maxStates)
        scores=[x + y for x, y in zip(scores, roundScores)]
        turnCount+=numberTurns
    results=zip(agents,scores) 
    results.sort(key=getKey,reverse=True) #highest scores first
    
    #print results
    #print scores
    topScores=[]
    winners=[]
    offspringses=[]
    average=[]
    for i in range(evol[0]):
        winner=results[i][0]
        winners.append(winner) 
        topScores.append(results[i][1])
        offspring =reproduce(winner,allMax=allMax)
        offspringses.append(offspring) 
    for i in range(evol[0],count-evol[0]-evol[2]):
        average.append(results[i][0]) 
        topScores.append(results[i][1])
    next_gen=winners+average+offspringses
    next_gen+=generate_agents(count= evol[2] , maxStates=startStates,allMax=True)
    #print len(next_gen)
    avgScore=float(sum(scores))/(count*turnCount)
    # should return all stats in one tuple, preferably a labelled one
    #print avgScore
    battingAvg=[float(x)/turnCount for x in topScores]
    return (next_gen,topScores,(avgScore,battingAvg))

def getKey(item):
    #helper function for run_generation
    return item[1]    
        
def reproduce(agent,allMax=False,maxStates=8):
    # returns a mutated offspring
    listAgent=[int(i) for i in agent]
    states= (len(agent)-2)/3
    mutation=r.randint(0,99)
    mutationState=r.randint(1,states)
    #print "babies"
    #print listAgent
    if 19<mutation<30 and states>1:
        #remove a state
        #print"test"
        
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
        #print listAgent
    elif 29<mutation<50 and states<maxStates:
        #add a state
        listAgent+= [r.randint(0,1),r.randint(1,states+1),r.randint(1,states+1)] 
    elif 49<mutation <55:
        # change the initial move
        listAgent[1]= 1-listAgent[1]
        #print"test"
    elif 54<mutation<70:
        # change the state move
        listAgent[mutationState*3 -1] = int(not listAgent[mutationState*3 -1])
    elif 69<mutation<85:
        # change the state coop destination
        listAgent[mutationState*3 ]= (listAgent[mutationState*3]+r.randint(0,states-1))%states +1
    elif 84<mutation <100:
        # change the state deceive destination
        listAgent[mutationState*3 +1]= (listAgent[mutationState*3+1]+r.randint(0,states-1))%states +1
    agent = "".join(map(str, listAgent))
    #print listAgent
    return agent

def run_simulation(agents,game,evol,count=64,rounds=100,w=0.9,generations=100 ,startStates=2,maxStates=8,allMax=False):
    #returns a tuple,feeds into main
    simulationStats=[[],[0]]
    for i in range(generations):
        if i%25==24: print "Generation " +str(i+1)
        (agents,topScores,stats)=run_generation(agents,game,count=count,rounds=rounds,w=w,evol=evol,startStates=startStates,maxStates=maxStates,allMax=allMax)
        simulationStats[0].append(stats[0])
        
        #average size of strategy grows since extra genetic material doesn't seem to have an adverse effect, interesting in relation to DNA
        #totalStates=0
        #for agent in agents:
        #    totalStates+=len(agent)/3
        #print "average number of states:",  float(totalStates)/len(agents)
    simulationStats[1]=stats[1]
    return (agents,topScores,simulationStats)

def writeHtml(jsonList): 
    #print jsonList["0"]
    htmlTemplate=open("graph007template.html","r")
    htmlTemplateString=htmlTemplate.read()
    htmlTemplate.close()
    custom='var allData='+''+" {'0': {"+'\n'
    
    for (index,(key,value)) in enumerate(jsonList['0'].items()):
        custom+="'"+str(key)+"'" +" : "  + str(value) +',\n'
    custom += "},"+'\n'+ "'codes':[ "+'\n'
    for i in range(len(jsonList["codes"])):
        custom+=str(jsonList["codes"][i])+',\n'
    custom += " ]}"+';' +'\n'
    custom+='console.log(typeof allData);'
    total=htmlTemplateString % {"jsonData":custom}
    
    outputFile=open("graph007.html","w")
    outputFile.seek(0)
    outputFile.truncate() # empties file
    outputFile.write(total)
    outputFile.close()

def drawToBrowser(graphStrings,stats):
    #print "# of strings"
    #print len(graphStrings)
    drawCharts(stats)
    graphList=[]
    data1 = {}
    data2= []
    for i in range(len(graphStrings)):
        #print graphStrings[i]
        
        G=createGraphFromString(graphStrings[i])
        d=json_graph.node_link_data(G)
        d["directed"]=1
        d["multigraph"]=1
        data1[str(i+1)]=d
        data2.append({"text": str(i+1),"value": str(i+1)})
            
       # print d
    data={"0":data1,
            "codes": data2,}
    #print jsonList
    #print len(jsonList)
    jsonList= json.dumps(data) # node-link format to serialize
    #print d 
    # write json
    writeHtml(data)
    #json.dump(d, open('temp.json','w'))
    print('Wrote node-link JSON data to temp.json')
    # open URL in running web browser
    http_server.load_url('graph007.html')
    print('Or copy all files to webserver and load graph.html')

def drawCharts(stats):
    sns.set(style="darkgrid", palette="muted")
    fig= plt.subplots(1,1, figsize=(4, 3))
    b, g, r, p = sns.color_palette("muted", 4)
    ax = sns.tsplot(stats[0],  color=g)
    ax.set( ylabel="average score per round")
    ax.set_xlabel("generation")
    plt.gcf().subplots_adjust(bottom=0.22)
    
    #pylab.figure(figsize=(4,3), dpi=80)
    #pylab.plot( range(generations),stats[0])
    plt.savefig("historical.png")    
    
def createGraphFromString(graphString):
    #takes a string as input and outputs a Networkx graph object
    (nodes,edges)=parse(graphString)
    G=nx.MultiDiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    activeNodes=[1]
    nextNodes=[]
    #print nx.number_of_nodes(G)
    for i in range(nx.number_of_nodes(G)):
        
        activeNodes=list(set(activeNodes+nextNodes))
        nextNodes=[]
        for node in activeNodes:
            
            nextNodes+=G.successors(node)  #0 is predecessors, 1 is successors
    #print activeNodes
    #activeNodes=list(set(sorted(activeNodes)))
    
    #print activeNodes
    extraNodes= list(set(range(1,nx.number_of_nodes(G)+1))-set(activeNodes))
    for i in extraNodes:

        G.remove_node(i)
        #print nx.number_of_nodes(G)
    
    return G
    
def parse(graphString):
    #returns two lists of edges and a list of nodes
    graphList=map(int, list(graphString))
    #print graphList
    numberNodes=(len(graphString)-2)/3
    edgeList=[]
    nodeList=[]
    for i in range(numberNodes):
        edgeList.append((i+1,graphList[3*i+3],{'type':'C'})) #(start,end, {'attribute':'value'})
        edgeList.append((i+1,graphList[3*i+4],{'type':'D'}))
        if graphList[3*i+2]: nodeList.append((i+1,{'type':'D'}))
        else: nodeList.append((i+1,{'type':'C'}))
    return (nodeList,edgeList)



    
if __name__=="__main__":
    main()