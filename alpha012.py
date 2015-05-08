import sys; sys.path.insert(0, 'IPD_functions') 
from game_logic import play_game,tally_score
from generation_logic import play_round,run_generation
from generate_agents import generate_agents
from IPD_utilities import pretty_print

import random as r
import json                     # for d3 drawing
import collections              # for data tracking
import networkx as nx           # for making graphs
from networkx.readwrite import json_graph #more d3
import http_server  #more d3
import numpy as np
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
        graph009template.html
    
    Most parameters are in the main function, though the mutation logic is contained in reproduce()
    -1 is defect, 0 is cooperate throughout the code
    
    If something doesn't make sense please tell me!
    -Andrew van den Hoeven
    """
DEBUG=False
    
''' TODO

        -make the sim end with a full gen played but skip the last reproduction so that all the strategies can be ranked and ordered
        -interactive charts?
        -log a history?
        -add family trees across time?
        -add random element to state actions and transitions
        -add noise X semi complete
        -time functions to determine what's inefficient
    
    
    '''
def main():
    game_matrix=[[3,3],[0,5],[5,0],[1,1]] 
    number_of_agents=64
    maxStates=16
    startStates=1
    allMax=True # whether or not all agents will have the max number of states
    rounds=10
    generations=500
    w=0.98 #probability of game going on another turn
    noise=False # use Joss_ann noise or not
    evolution_settings=(25,13,1) #(breed,survive,newcommers)
    
    agents=generate_agents(count= number_of_agents , maxStates=startStates,allMax=True)
    (result,ranks,stats)= run_simulation(agents,game=game_matrix,count=number_of_agents, evol=evolution_settings, rounds=rounds,w=w,generations=generations,startStates=startStates,maxStates=maxStates,allMax=allMax,noise=noise)
    simulationResults=zip(result,ranks,stats[1])
    pretty_print(simulationResults,entriesPerLine=1)

    topAgent=result[0]
    print topAgent, ranks[0]
    drawToBrowser(result,stats)
    

   
        

def run_simulation(agents,game,evol,count=64,rounds=100,w=0.9,generations=100 ,startStates=2,maxStates=8,allMax=False,noise=True):
    #returns a tuple,feeds into main
    simulationStats=[[],[0],[],[],[]]
    lastGen=False
    for i in range(generations):
        if i%25==24: print "Generation " +str(i+1)
        if i== generations-1: lastGen=True
        
        (agents,topScores,stats)=run_generation(agents,game,count=count,rounds=rounds,w=w,evol=evol,startStates=startStates,maxStates=maxStates,allMax=allMax,noise=noise,lastGen=lastGen)
        simulationStats[0].append(stats[0])
        simulationStats[2].append(stats[2])
        simulationStats[3].append(stats[3])
        simulationStats[4].append(stats[4])
        #average size of strategy grows since extra genetic material doesn't seem to have an adverse effect, interesting in relation to DNA
        #totalStates=0
        #for agent in agents:
        #    totalStates+=len(agent)/3
        #print "average number of states:",  float(totalStates)/len(agents)
    simulationStats[1]=stats[1]
    return (agents,topScores,simulationStats)

def writeHtml(jsonList): 
    #print jsonList["0"]
    htmlTemplate=open("graph009template.html","r")
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
    
    outputFile=open("graph009.html","w")
    outputFile.seek(0)
    outputFile.truncate() # empties file
    outputFile.write(total)
    outputFile.close()

def drawToBrowser(graphList,stats):
    #print "# of strings"
    #print len(graphStrings)
    drawCharts(stats)
    data1 = {}
    data2= []
    for i in range(len(graphList)):
        #print graphStrings[i]
        
        G=createGraphFromList(graphList[i])
        d=json_graph.node_link_data(G)
        d["directed"]=1
        d["multigraph"]=1
        data1[str(i+1)]=d
        j1,j2=round(graphList[i][1][0],4),round(graphList[i][1][1],4)
        if j1+j2 >1: j1,j2=(1-j1,1-j2)
        text=str(i+1)+" - ("+str(j1)+","+str(j2)+")"
        data2.append({"text": text,"value": str(i+1)})
            
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
    http_server.load_url('graph009.html')
    print('Or copy all files to webserver and load graph.html')

def drawCharts(stats):
    sns.set(style="darkgrid", palette="muted")
    fig= plt.subplots(1,1, figsize=(3.5, 2.8))
    b, g, r, p = sns.color_palette("muted", 4)
    ax = sns.tsplot(stats[0],  color=g)
    ax.set( ylabel="Average score per turn")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom=0.22)
    
    #pylab.figure(figsize=(4,3), dpi=80)
    #pylab.plot( range(generations),stats[0])
    plt.savefig("historical.png") 
    plt.clf()
    plt.cla()
    sns.set(style="darkgrid", palette="muted")
    fig= plt.subplots(1,1, figsize=(4, 3))
    b, g, r, p = sns.color_palette("muted", 4)
    data=np.dstack([[1-j for j in stats[i]]  for i in range(2,5)]) # 1- to flip the y axis
    ax = sns.tsplot(data,color=[g,b,r])
    ax.set( ylabel="Average sentience")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom=0.22)
    plt.savefig("sentience.png") 
    return 
    
    
def createGraphFromList(graph):
    #takes a string as input and outputs a Networkx graph object
    (nodes,edges)=parse(graph)
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
    
def parse(graphList):
    #returns two lists of edges and a list of nodes
    #print graphList
    numberNodes=(len(graphList)-2)/3
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