import time
import sys
import pygame
import random
import numpy as np
import itertools
import operator
import random as r
import math


def generate_coordinates(center,radius,directions):
    #takes in a center coordinates and returns a hexagon of cub coordinates
    coordinates=set([center])
    outerlayer=set([center])
    for i in range(radius):
        new=[]
        for coord in outerlayer:
            for direction in directions:
                new.append(tuple(map(operator.add, coord , direction)))
        outerlayer=set(new)
        coordinates=set(itertools.chain.from_iterable((outerlayer,coordinates)))
    return list(coordinates)

def generate_mirror_dict(radius,coordinates):
    #creates a dictionary to deal with off the map coords, could likely be improved
    result={}
    for i in range(6):
        shift=rotate((2*radius+1, -radius, -radius-1),i)
        for coord in coordinates:
            result[tuple(map(operator.add, coord , shift))]=coord
    for coord in coordinates:
        result[coord]=coord
    return result

def rotate(coord,rotations):
    #takes in a cube coordinate and how many times to rotate it 60 degrees to the right and outputs the rotated coord
    x,y,z=coord
    result=x,y,z
    if rotations==0: return coord
    else: 
        for i in range(rotations):
            x,y,z=result
            result=(-z, -x, -y)#60 degree to the right
    return result

def cube_to_offset(coord):
    #converts cube coordinates to offset coordinates
    x,y,z= coord
    col = x + (z - (z&1)) / 2
    row = z
    return (col,row)


    
    