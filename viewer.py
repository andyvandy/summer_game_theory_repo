import json                     # for d3 drawing
import collections              # for data tracking
import networkx as nx           # for making graphs
from networkx.readwrite import json_graph #more d3

import sys; sys.path.insert(0, 'IPD_functions') 
import http_server  #more d3


# this needs to be polished

def main():
    json1_file = open('C:/Users/Andrew/Documents/programs/summer game theory/data/test/final_agents.json',"r+")
    json1_str = json1_file.read()
    agent_dict=json.loads(json1_str)
    json1_file.close()
    print agent_dict
    draw_to_browser(agent_dict)


def write_html(json_list): 
    #print json_list["0"]
    html_template = open("IPD_output/overalltemplate.html", "r")
    html_template_string = html_template.read()
    html_template.close()
    custom = 'var allData='+''+" {'0': {"+'\n'

    total=html_template_string
    output_file = open("IPD_output/overall.html", "w")
    output_file.seek(0)
    output_file.truncate() # empties file
    output_file.write(total)
    output_file.close()

    
def draw_to_browser(agents):

    data1 = {}
    data2= []
    for i in range(0,10):
        for j in range(20):
            #print graphStrings[i]
            
            G = create_graph_of_agent(agents[str(i)][str(j)])
            d = json_graph.node_link_data(G)
            d["directed"] = 1
            d["multigraph"] = 1
            text= "s " +str(i + 1)+" | " + str(j + 1)
            data1[text] = d
           
            data2.append({"text": text, "value": text})

    data = {"0": data1,
            "codes": data2}

    write_html(data)
    json.dump(data, open('IPD_output/data.json', 'w'))
    print('Wrote node-link JSON data to temp.json')
    # open URL in running web browser
    http_server.load_url('IPD_output/overall.html')
    print('Or copy all files to webserver and load graph.html')



def create_graph_of_agent(agent):
    # takes a string as input and outputs a Networkx graph object
    (nodes, edges) = parse(agent)
    G = nx.MultiDiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    active_nodes = [1]
    next_nodes = []

    for i in range(nx.number_of_nodes(G)):
        
        active_nodes = list(set(active_nodes + next_nodes))
        next_nodes = []

        for node in active_nodes:          
            next_nodes += G.successors(node) #0 is predecessors, 1 is successors

    extra_nodes = sorted(list(set(range(1, nx.number_of_nodes(G) +1)) 
                       - set(active_nodes)), reverse=True)
  
    for i in extra_nodes:
        G.remove_node(i)
    return G
    

def parse(behaviour):
    #returns two lists of edges and a list of nodes

    number_nodes = len(behaviour)
    edge_list = []
    node_list = []
    for i in range(number_nodes):
        # (start, end, {'attribute': 'value'})
        edge_list.append((i +1, behaviour[i][1], {'type': 'C'})) 
        edge_list.append((i +1, behaviour[i][2], {'type': 'D'}))

        if behaviour[i][0]: node_list.append((i + 1, {'type': 'D'}))
        else: node_list.append((i + 1, {'type': 'C'}))
    
    return (node_list, edge_list)






if __name__ =="__main__":
    main()
