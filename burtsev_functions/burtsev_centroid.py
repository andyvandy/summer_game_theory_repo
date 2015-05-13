import time
import sys
import pygame
import random
import numpy as np
import itertools
import operator
import random as r
import math

from burtsev_utilities import agents_in_cell

def deviation_from_centroid(agent,coord,agents):
    # doesn't count the agent themselves in the centroid
    agents_in_tile=agents_in_cell(coord,agents)
    if len (agents_in_tile)==1:return 0
    list_of_phenotypes=[other_agent.phenotype for other_agent in agents_in_tile if other_agent!=agent]
    centroid=centroidnp(list_of_phenotypes)
    return  euclidean_distance(centroid,agent.phenotype)
    
def centroidnp(list_of_phenotypes):
    length = len(list_of_phenotypes)
    centroid=[0]*9
    for i in range(length):
        for j in range(9):
            try: centroid[j]+=list_of_phenotypes[i][j]/float(length)
            except:
                print i,j
                print centroid
                print list_of_phenotypes
                sys.exit()
    return tuple(centroid)
 

def determine_kinship_to_partner(agent1,agent2,wmax,k):
    return k*euclidean_distance(agent1.phenotype,agent1.phenotype)/(2.0*wmax)
 
def euclidean_distance(vector1,vector2):
    result=0
    for i in range(9):
        result+=(vector1[i]-vector2[i])**2
    return  round(math.sqrt(result   ),2) 
 