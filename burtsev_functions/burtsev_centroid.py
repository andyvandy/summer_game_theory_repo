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
    agents_in_tile=agents_in_cell(coord,agents)
    if len (agents_in_tile)==1:return 0
    list_of_phenotypes=[agent.phenotype for agent in agents_in_tile]
    centroid=centroidnp(list_of_phenotypes)
    phenotype=agent.phenotype
    result=0
    for i in range(9):
        result+=(centroid[i]-phenotype[i])**2
    return  round(math.sqrt(result   ),2) 
    
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
 