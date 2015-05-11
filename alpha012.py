"""
Author: Andrew van den Hoeven
Date: May 2015

Simulates multiple agents in an iterative prisoners dilemma, with evolving
strategies.

Some notes from Andrew:
    Required libraries:
        json, random, http_server
        networkx : for the graphs
        matplotlib : for charts
        seaborn : for pretty charts
        
    required files:
        http_server.py
        graph009template.html
    
    Most parameters are in the main function, though the mutation logic is 
    contained in reproduce()

    -1 is defect, 0 is cooperate throughout the code
    
    If something doesn't make sense please tell me!
    
    maxstates =1 and noise= False with the snowdrift game produces a mixed population
    of hawks and doves that oscillates around an equilibrium ratio as seen
    in the literature

Note from Stuart:
    If for some reason the web page doesn't launch automatically for you when
    the server starts, you can access it at http://localhost:8000/graph009.html

TODO:
    -make the sim end with a full gen played but skip the last reproduction so that all the strategies can be ranked and ordered
    -interactive charts?
    -log a history?
    -add family trees across time?
    -add random element to state actions and transitions
    -add noise X (semi complete)
    -time functions to determine what's inefficient
    -turn stats tuple into a named tuple
    -add cost for complexity?
"""

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

DEBUG = False
    
def main():
    # represents the value of choices
    game_matrix = [[3, 3], [1, 5], [5, 1], [0, 0]]
        #prisoner's dilema:[[3, 3], [0, 5], [5, 0], [1, 1]] 
        #snowdrift/chicken game: [[3, 3], [1, 5], [5, 1], [0, 0]] 
    number_of_agents = 36
    max_states = 1
    start_states = 1 #set to 1 for single simulation output 
    # whether or not all agents will have the max number of states
    all_max = True 
    rounds = 150
    generations = 250
    simulations=200
    w = 0.98 #probability of game going on another turn
    noise = False # use Joss_ann noise or not
    evolution_settings = (12, 11, 1) # (breed, survive, newcommers)
    
    
    run_all_simulations( game = game_matrix,
                             evol = evolution_settings,
                             number_of_simulations=simulations,
                             count = number_of_agents, 
                             rounds = rounds, w = w,
                             generations = generations, 
                             start_states = start_states, 
                             max_states = max_states, all_max = all_max, 
                             noise = noise)
    return "complete"
    
    

def run_all_simulations(game, evol, number_of_simulations, count=64, rounds=100, w=0.9, 
                   generations=100, start_states=2, max_states=8, all_max=False,
                   noise=True):  
    if number_of_simulations==1:
        (result, ranks, stats) = run_simulation( game = game,
                             evol = evol,
                             number_of_simulations=number_of_simulations,
                             count = count, 
                             rounds = rounds, w = w,
                             generations = generations, 
                             start_states = start_states, 
                             max_states = max_states, all_max = all_max, 
                             noise = noise,
                             verbose=True)
        simulation_results = zip(result, ranks, stats[1])
        pretty_print(simulation_results, entries_per_line = 1)

        topAgent = result[0]
        print topAgent, ranks[0]
        draw_to_browser(result,stats)
        return "complete"
    
    
    avg_score_logs=[],
    avg_coop_logs=[],
    avg_defect_logs=[]
    stats=[[],
            [],
            [],
            
            
            
        ]
    
    for i in range(number_of_simulations):
        (result, ranks, simulation_stats) = run_simulation( game = game,
                             evol = evol,
                             count = count, 
                             rounds = rounds, w = w,
                             generations = generations, 
                             start_states = start_states, 
                             max_states = max_states, all_max = all_max, 
                             noise = noise)
        if (i+1)%10 ==0: print "simulation ", i+1
        stats[0].append(simulation_stats[0]) #avg turn score
        stats[1].append(simulation_stats[5]) #avg_pop_coop
        stats[2].append(simulation_stats[6]) #avg_pop_defect
    
    draw_overall_charts(stats)
    write_overall_data(stats)
    
def draw_overall_charts(stats):
    #draws charts for data from multiple simulations
    
    #chart 1 : average score per turn
    sns.set(style = "darkgrid", palette = "muted")
    fig = plt.subplots(1, 1, figsize = (4, 2.5))
    b, g, r, p = sns.color_palette("muted", 4)
    ax = sns.tsplot(stats[0], color=g)
    ax.set(ylabel = "Average score per turn")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom = 0.22)
    plt.savefig("images/historical_overall.png") 
    
    
    plt.clf()
    plt.cla()
    
    #chart 3: cooperation and defection
    sns.set(style="darkgrid", palette="muted")
    fig = plt.subplots(1, 1, figsize=(4, 3))
    b, g, r, p = sns.color_palette("muted", 4)
    data = np.dstack([[j for j in stats[i]] for i in [1,2]]) 
    ax = sns.tsplot(data, color = [ b, r])
    ax.set(ylabel = "percent coop/defect")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom = 0.22)
    plt.savefig("images/cooppct_overall.png") 
    
    return

def write_overall_data(stats):
    #TODO
    pass
    
def run_simulation( game, evol, count=64, rounds=100, w=0.9, 
                   generations=100, start_states=2, max_states=8, all_max=False,
                   noise=True, verbose=False):
    
    # returns a tuple,feeds into main
    
    #initialize agents
    agents = generate_agents(count = count, 
                             max_states = start_states, all_max = True,
                             noise = True)
    
    simulation_stats = [[], [0], [], [], [],[],[]]
    last_gen = False
    for i in range(generations):
        if i % 25 == 24 and verbose: print "Generation " + str(i + 1)
        if i == generations - 1: last_gen=True
        
        (agents, top_scores, generation_stats) = run_generation(agents, game, 
                                                     count = count, 
                                                     rounds = rounds, w = w,
                                                     evol = evol, 
                                                     start_states = start_states,
                                                     max_states = max_states, 
                                                     all_max = all_max, 
                                                     noise = noise,
                                                     last_gen = last_gen)

        simulation_stats[0].append(generation_stats[0]) #avgscore
        simulation_stats[2].append(generation_stats[2]) #avg_sentience
        simulation_stats[3].append(generation_stats[3]) #avg_hard_coop , from joss ann noise
        simulation_stats[4].append(generation_stats[4]) #avg_hard_defect , from joss ann noise
        simulation_stats[5].append(generation_stats[5]) #avg_pop_coop
        simulation_stats[6].append(generation_stats[6]) #avg_pop_defect

    simulation_stats[1] = generation_stats[1] #final gen individual batting avgs for final output
    return (agents, top_scores, simulation_stats)


def write_html(json_list): 
    #print json_list["0"]
    html_template = open("graph009template.html", "r")
    html_template_string = html_template.read()
    html_template.close()
    custom = 'var allData='+''+" {'0': {"+'\n'
    
    for (index, (key, value)) in enumerate(json_list['0'].items()):
        custom += "'" + str(key) + "'" + " : "  + str(value) + ',\n'
    custom += "}," + '\n' + "'codes':[ " + '\n'
    for i in range(len(json_list["codes"])):
        custom += str(json_list["codes"][i]) + ',\n'
    custom += " ]}" + ';' + '\n'
    custom += 'console.log(typeof allData);'
    total = html_template_string % {"jsonData": custom}
    
    output_file = open("graph009.html", "w")
    output_file.seek(0)
    output_file.truncate() # empties file
    output_file.write(total)
    output_file.close()


def draw_to_browser(graph_list, stats):
    # print "# of strings"
    # print len(graphStrings)
    draw_sim_charts(stats)
    data1 = {}
    data2= []
    for i in range(len(graph_list)):
        #print graphStrings[i]
        
        G = create_graph_from_list(graph_list[i])
        d = json_graph.node_link_data(G)
        d["directed"] = 1
        d["multigraph"] = 1
        data1[str(i + 1)] = d
        j1, j2 = round(graph_list[i][1][0], 4), round(graph_list[i][1][1], 4)
        jay1, jay2 = j1, j2
        if j1 + j2 > 1: jay1, jay2 = (1 - j2, 1 - j1)
        text = str(i + 1) + " - (" + str(jay1) + "," + str(jay2) + ")"
        data2.append({"text": text, "value": str(i + 1)})
            
        # print d

    data = {"0": data1,
            "codes": data2}

    # print json_list
    # print len(json_list)
    json_list = json.dumps(data) # node-link format to serialize
    # print d 
    # write json
    write_html(data)
    # json.dump(d, open('temp.json', 'w'))
    print('Wrote node-link JSON data to temp.json')
    # open URL in running web browser
    http_server.load_url('graph009.html')
    print('Or copy all files to webserver and load graph.html')

def draw_sim_charts(stats):
    #draws charts from a single simulation and saves files to be shown in html output_file
    
    #chart 1 : average score per turn
    sns.set(style = "darkgrid", palette = "muted")
    fig = plt.subplots(1, 1, figsize = (4, 2.5))
    b, g, r, p = sns.color_palette("muted", 4)
    ax = sns.tsplot(stats[0], color=g)
    ax.set(ylabel = "Average score per turn")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom = 0.22)
    plt.savefig("images/historical.png") 
    
    plt.clf()
    plt.cla()
    
    #chart 2 : joss-Ann "sentience" where sentience is defined as how little
    # noise the strategy has. A more "sentient" strategy follows it's states more closely
    sns.set(style="darkgrid", palette="muted")
    fig = plt.subplots(1, 1, figsize=(4, 3))
    b, g, r, p = sns.color_palette("muted", 4)
    # 1- to flip the y axis
    data = np.dstack([[1 - j for j in stats[i]] for i in range(2, 5)]) 
    ax = sns.tsplot(data, color = [g, b, r])
    ax.set(ylabel = "Average sentience")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom = 0.22)
    plt.savefig("images/sentience.png") 
    
    plt.clf()
    plt.cla()
    
    #chart 3: cooperation and defection
    sns.set(style="darkgrid", palette="muted")
    fig = plt.subplots(1, 1, figsize=(4, 3))
    b, g, r, p = sns.color_palette("muted", 4)
    data = np.dstack([[j for j in stats[i]] for i in [5,6]]) 
    ax = sns.tsplot(data, color = [ b, r])
    ax.set(ylabel = "percent coop/defect")
    ax.set_xlabel("Generation")
    plt.gcf().subplots_adjust(bottom = 0.22)
    plt.savefig("images/cooppct.png") 
    
    return 
    
    
def create_graph_from_list(graph):
    # takes a string as input and outputs a Networkx graph object
    (nodes, edges) = parse(graph)
    G = nx.MultiDiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    active_nodes = [1]
    next_nodes = []
    # print nx.number_of_nodes(G)

    for i in range(nx.number_of_nodes(G)):
        active_nodes = list(set(active_nodes + next_nodes))
        next_nodes = []

        for node in active_nodes:          
            next_nodes += G.successors(node) #0 is predecessors, 1 is successors
    
    #print active_nodes
    #active_nodes=list(set(sorted(active_nodes)))
    
    #print active_nodes

    extra_nodes = list(set(range(1, nx.number_of_nodes(G) + 1)) 
                       - set(active_nodes))

    for i in extra_nodes:
        G.remove_node(i)
        #print nx.number_of_nodes(G)
    
    return G
    

def parse(graph_list):
    #returns two lists of edges and a list of nodes
    #print graph_list
    number_nodes = (len(graph_list) - 2) / 3
    edge_list = []
    node_list = []
    for i in range(number_nodes):
        # (start, end, {'attribute': 'value'})
        edge_list.append((i + 1, graph_list[3 * i + 3], {'type': 'C'})) 
        edge_list.append((i + 1, graph_list[3 * i + 4], {'type': 'D'}))

        if graph_list[3 * i + 2]: node_list.append((i + 1, {'type': 'D'}))
        else: node_list.append((i + 1, {'type': 'C'}))
    
    return (node_list, edge_list)

    
if __name__ =="__main__":
    main()
