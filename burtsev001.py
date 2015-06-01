import time
import sys
import pygame
import random
import numpy as np
import itertools
import operator
import random as r
import math

import sys; sys.path.insert(0, 'burtsev_functions') 
from coordinate_logic import generate_coordinates,generate_mirror_dict,rotate,cube_to_offset
from burtsev_centroid import deviation_from_centroid, centroidnp, determine_kinship_to_partner
from burtsev_utilities import count_agents,agents_in_cell,tally_energy
from mutation_logic import mutate_phenotype

'''
    strategies are encoded in an n by m matrix as such:
        
                            inputs(m)
                    |  2 ,  3 , 90 , ...     , ## , ## |
        actions(n)  | 34 ,  2 ,  5 , ...     , ## , ## |
                    | ## , ## , ## , ...     , ## , ## |
                    ...                               ...
                    | ## , ## , ## , ...     , ## , ## |
             
    
    actions (in order):
                        -rest
                        -turn right
                        -turn left
                        -feed
                        -move forward
                        -attack
                        -divide
    
    inputs (in order):
                        -constant k
                        -current energy level
                        -potential space for more energy
                        -kinship to current cell 
                        -kinship to current partner 
                      4*-boolean for whether there are resources in the current, infront,right,left cells
                      4*-number of agents  there are in the current, infront, right, left cells
        '''
                
def main():
    
    run_simulation(starting_pop=25)
              
class Agent:
    def __init__(self,parent_genes,initial_location,initial_energy,phenotype,parent_direction):
        self.location = initial_location
        self.genes=parent_genes  
        self.energy = initial_energy
        self.phenotype=phenotype
        self.direction=parent_direction 
        self.forwards=MIRROR_COORDS[tuple(map(operator.add, self.location , self.direction))]
        self.right=MIRROR_COORDS[tuple(map(operator.add, self.location , rotate(self.direction,1)))]
        self.left=MIRROR_COORDS[tuple(map(operator.add, self.location , rotate(self.direction,5)))]
        
    def turn(self,right=True):
        x,y,z=self.direction
        if right: # two wrongs don't make a right,
            self.direction=rotate(self.direction,1) 
            
        else:   # but five rights make a left!
            self.direction=rotate(self.direction,5) 
        self.forwards=MIRROR_COORDS[tuple(map(operator.add, self.location , self.direction))]
        self.right=MIRROR_COORDS[tuple(map(operator.add, self.location , rotate(self.direction,1)))]
        self.left=MIRROR_COORDS[tuple(map(operator.add, self.location , rotate(self.direction,5)))]    
        
        self.pay_energy(TURN_COST)#p0009
    def rest(self):
        self.pay_energy(REST_COST)#p0008
    def move_forward(self):
        x,y,z=tuple(self.location)
        x1,y1,z1=self.direction
        self.location=MIRROR_COORDS[(x+x1,y+y1,z+z1)]
        self.forwards=MIRROR_COORDS[tuple(map(operator.add, self.forwards , self.direction))]
        self.right=MIRROR_COORDS[tuple(map(operator.add, self.right , self.direction))]
        self.left=MIRROR_COORDS[tuple(map(operator.add, self.left , self.direction))]    
        if GRAPHICS_ON:draw_agent(self)#drawing
        if GRAPHICS_ON:draw_food((x,y,z))#drawing
        self.pay_energy(MOVE_COST)#p0010
    def pay_energy(self,amount):
        self.energy-=amount
        if self.energy<=0:
            #print "ouch"
            coord=self.location
            del(AGENTS[AGENTS.index(self)])
            if GRAPHICS_ON: draw_food(coord)#drawing
    def feed(self):
        amount=min(RESOURCES[self.location],BITE_SIZE) #p0011
        RESOURCES[self.location]=RESOURCES[self.location]-amount
        self.energy= min(self.energy+amount,ENERGY_MAX)
        if amount==0: self.rest()
    def attack(self,victim):
        victims_energy=victim.energy
        tasty_flesh=min(victims_energy,ATTACK_DAMAGE)#p0013
        self.energy= min(self.energy+tasty_flesh,ENERGY_MAX)
        victim.pay_energy(tasty_flesh)
        self.pay_energy(ATTACK_COST)#p0012
    def divide(self): 
        #TODO: write an efficient function so that the new genes are bounded
        if self.energy<=DIVIDE_COST: #stops agents from dividing without enough energy
            self.pay_energy(DIVIDE_COST)
            return
        self.pay_energy(DIVIDE_COST)#p0014
        
        offspring_phenotype=mutate_phenotype(self,PHENO_MUTATION_AMPLITUDE,WMAX) #p0016
        offspring_genotype=self.genes+ np.random.randint(-MUTATION_AMPLITUDE,MUTATION_AMPLITUDE+1,(7,13))

        if np.amax(offspring_genotype) > WMAX: 
            print "fix this stuff on line 90"
        if np.amin(offspring_genotype) <  -WMAX: 
            print "fix this stuff on line 91"
       
        
        
        AGENTS.append(Agent(parent_genes=offspring_genotype, #remember to update matsize if changes are made  #p0015
                        initial_location=self.location,
                         initial_energy=int(self.energy/2.0),
                         phenotype=offspring_phenotype,
                         parent_direction=self.direction))
        self.pay_energy(int(self.energy/2.0))


class Stats:
    def __init__(self):
        self.number_of_agents =[len(AGENTS)]
        
def offset_to_tile(offset):
    #takes in an offset coordinate as input and returns a list of 4 nested hexagons' pixel coordinates 
    i,j=offset
    shift=(500,280) #graphics_param
    result=[]
    result.append(((shift[0]+i*20+10*(j%2),shift[1]+6+18*j),
                (shift[0]+10+i*20+10*(j%2),shift[1]+18*j),
                (shift[0]+20+i*20+10*(j%2),shift[1]+6+18*j),
                (shift[0]+20+i*20+10*(j%2),shift[1]+18+18*j),
                (shift[0]+10+i*20+10*(j%2),shift[1]+24+18*j),
                (shift[0]+i*20+10*(j%2),shift[1]+18+18*j)))
    result.append(((shift[0]+i*20+10*(j%2)+2,shift[1]+6+18*j+2),
                (shift[0]+10+i*20+10*(j%2),shift[1]+18*j+3),
                (shift[0]+20+i*20+10*(j%2)-2,shift[1]+6+18*j+2),
                (shift[0]+20+i*20+10*(j%2)-2,shift[1]+18+18*j-2),
                (shift[0]+10+i*20+10*(j%2),shift[1]+24+18*j-3),
                (shift[0]+i*20+10*(j%2)+2,shift[1]+18+18*j-2))) 
                    
    result.append(((shift[0]+i*20+10*(j%2)+4,shift[1]+6+18*j+4),
                (shift[0]+10+i*20+10*(j%2),shift[1]+18*j+6),
                (shift[0]+20+i*20+10*(j%2)-4,shift[1]+6+18*j+4),
                (shift[0]+20+i*20+10*(j%2)-4,shift[1]+18+18*j-4),
                (shift[0]+10+i*20+10*(j%2),shift[1]+24+18*j-6),
                (shift[0]+i*20+10*(j%2)+4,shift[1]+18+18*j-4))) 
                
    result.append(((shift[0]+i*20+10*(j%2)+6,shift[1]+6+18*j+6),
                (shift[0]+10+i*20+10*(j%2),shift[1]+18*j+9),
                (shift[0]+20+i*20+10*(j%2)-6,shift[1]+6+18*j+6),
                (shift[0]+20+i*20+10*(j%2)-6,shift[1]+18+18*j-6),
                (shift[0]+10+i*20+10*(j%2),shift[1]+24+18*j-9),
                (shift[0]+i*20+10*(j%2)+6,shift[1]+18+18*j-6))) 
    return result

def initialize_screen():
    background=pygame.Color(255,255,255) #"#fdd2b9"
    SCREEN.fill(background)
    for coord in COORDINATES:
        draw_food(coord)
    
    for agent in AGENTS:
        draw_agent(agent)
    pygame.display.update()
    return 

def draw_agent(agent):
    coord=agent.location
    (r1,g1,b1,r2,g2,b2,r3,g3,b3)=agent.phenotype
    tile=offset_to_tile(cube_to_offset(coord))
    line_col=pygame.Color("#054246")
    scale=WMAX/250
    ag1=pygame.Color(r1/scale,g1/scale,b1/scale)
    ag2=pygame.Color(r2/scale,g2/scale,b2/scale)
    ag3=pygame.Color(r3/scale,g3/scale,b3/scale)
    #ag1,ag2,ag3,ag4=pygame.Color("#800c1d"),pygame.Color("#ce132f"),pygame.Color("#ec3853"),pygame.Color("#f596a4")
    pygame.draw.polygon(SCREEN, ag1, tile[0], 0)
    pygame.draw.polygon(SCREEN, ag1, tile[1], 0)
    pygame.draw.polygon(SCREEN, ag2, tile[2], 0)
    pygame.draw.polygon(SCREEN, ag3, tile[3], 0)
    
    pygame.draw.polygon(SCREEN, line_col, tile[0], 2)

def erase_tile(coord):
    #replaces the current pixels in coord with the default background tile
    tile=offset_to_tile(cube_to_offset(coord))
    line_col=pygame.Color("#054246")
    col1,col2,col3,col4=pygame.Color("#b6f5f9"),pygame.Color("#87eff6"),pygame.Color("#48e7f1"),pygame.Color("#10c8d4")
    pygame.draw.polygon(SCREEN, col1, tile[0], 0)
    pygame.draw.polygon(SCREEN, col2, tile[1], 0)
    pygame.draw.polygon(SCREEN, col3, tile[2], 0)
    pygame.draw.polygon(SCREEN, col4, tile[3], 0)
    pygame.draw.polygon(SCREEN, line_col, tile[0], 2)

def draw_food(coord):
    line_col=pygame.Color("#054246")
    col1,col2,col3,col4=pygame.Color("#bdc70b"),pygame.Color("#e6f213"),pygame.Color("#eff663"),pygame.Color("#f5faa4")
    if len([agent for agent in AGENTS if agent.location==coord])==0:
        if RESOURCES[coord]:
            tile=offset_to_tile(cube_to_offset(coord))
            pygame.draw.polygon(SCREEN, col1, tile[0], 0)
            pygame.draw.polygon(SCREEN, col2, tile[1], 0)
            pygame.draw.polygon(SCREEN, col3, tile[2], 0)
            pygame.draw.polygon(SCREEN, col4, tile[3], 0)
            pygame.draw.polygon(SCREEN, line_col, tile[0], 2)
            
        else: erase_tile(coord)    

def draw_world_stats(stats):
    bg_col=pygame.Color(255,255,255)
    black=pygame.Color("#000000")
    myfont = pygame.font.SysFont("monospace", 15)
    line1 = myfont.render("Number of agents: "+str(stats[0]), 1, (0,0,0))
    line2 = myfont.render("Sum of agent energy: "+str(stats[1]), 1, (0,0,0))
    line3 = myfont.render("Energy available: "+str(stats[2]), 1, (0,0,0))
    line4 = myfont.render("time : "+str(stats[3]), 1, (0,0,0))
    box_dimensions=(5,5,290,100)
    pygame.draw.rect(SCREEN, bg_col, box_dimensions, 0)
    pygame.draw.rect(SCREEN, black, box_dimensions, 2)
    SCREEN.blit(line1, (10, 10))
    SCREEN.blit(line2, (10, 30))
    SCREEN.blit(line3, (10, 50))
    SCREEN.blit(line4, (10, 70))
    print "sadsa"
    
def run_simulation(starting_pop=25):
    
    if GRAPHICS_ON: initialize_screen()

    initial_strategy=np.zeros((7,13))
    initial_strategy[3][5]=100
    initial_strategy[4][6]=70
    initial_strategy[6][0]=20
    initial_phenotype=(WMAX/4*3,WMAX/4*3,WMAX/4*3,WMAX/4*3,WMAX/4*3,WMAX/4*3,WMAX/4*3,WMAX/4*3,WMAX/4*3)                  
    print initial_strategy
    
    #generate agents
    for i in range(starting_pop):
        spawn_location=r.choice(COORDINATES)
        initial_direction=r.choice(DIRECTIONS)
        AGENTS.append(Agent(parent_genes=initial_strategy,
                        initial_location=spawn_location,
                         initial_energy=INITIAL_ENERGY, #p0007
                         phenotype=initial_phenotype,
                         parent_direction=initial_direction))
    #spawn initial food supply
    for coord in COORDINATES:
        #TODO: determine how to distribute the initial supply
        RESOURCES[coord]=FOOD_SIZE
    
    tick=1
    print "total energy: ", tally_energy(AGENTS,RESOURCES,COORDINATES)
    print "total agents: ", len(AGENTS)
    while tick :
        #graphics
        if GRAPHICS_ON:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     pygame.quit(); sys.exit();
        
        tick+=1
        if tick%FOOD_FREQUENCY==0: #p0004
            for i in range(FOOD_COUNT): #p0005
                coord=r.choice(COORDINATES)
                RESOURCES[coord]+=FOOD_SIZE #p0006
                if GRAPHICS_ON: draw_food(coord)        
                
        for agent in AGENTS:
            if count_agents(agent.location,AGENTS)>2:
                candidates=agents_in_cell(agent.location,AGENTS)
                targets= [target for target in candidates if target != agent]
                
                partner=r.choice(targets)
                kinship_to_partner=determine_kinship_to_partner(agent,partner,WMAX,K)
            elif count_agents(agent.location,AGENTS)>1:
                candidates=agents_in_cell(agent.location,AGENTS)
                targets= [target for target in candidates if target != agent]
                partner=targets[0]
            else:
                partner=agent
                kinship_to_partner=0 #0 is high
            directional_resources= [bool(RESOURCES[agent.location])]+[ bool(RESOURCES[agent.forwards]),bool(RESOURCES[agent.right]),bool(RESOURCES[agent.left])]
            directional_agents= [count_agents(agent.location,AGENTS)]+[ count_agents(agent.forwards,AGENTS),count_agents(agent.right,AGENTS),count_agents(agent.left,AGENTS) ]
            kinship_with_locals=deviation_from_centroid(agent,agent.location,AGENTS)
            
            # p0001 , p0003
            input=np.transpose(np.matrix([K,  float(agent.energy)/ENERGY_MAX,float(ENERGY_MAX-agent.energy)/ENERGY_MAX , kinship_with_locals ,kinship_to_partner] +directional_resources+directional_agents))
            #print input 
            output=agent.genes*input
            #print output
            top_choice=max(output)
            indices = [i for i, x in enumerate(output) if x==top_choice]
            action=r.choice(indices)
            #print indices,action
            if action ==0: agent.rest()
            elif action ==1: agent.turn(right=True)
            elif action ==2: agent.turn(right=False)
            elif action==3: agent.feed()
            elif action==4: agent.move_forward()    
            elif action==5: agent.attack(partner) 
            elif action==6: agent.divide()     
            else:print "error"
            
        if tick%50==0:
            if GRAPHICS_ON or LOG_TO_CONSOLE>1:
                agent_energy, available_energy=tally_energy(AGENTS,RESOURCES,COORDINATES)
                if GRAPHICS_ON: draw_world_stats((len(AGENTS),round(agent_energy,2),round(available_energy,2),tick/100.0))  #drawing

                print "total agent energy: ", agent_energy
                print "total agents: ", len(AGENTS)
                print "available energy: ", available_energy
            if  GRAPHICS_ON or LOG_TO_CONSOLE>0:  
                print tick
            if len(AGENTS)==0:tick=False
    

#GRAPHICS SETTINGS
GRAPHICS_ON=True
if GRAPHICS_ON:
    WIDTH=1000
    HEIGHT=600
    pygame.init()
    pygame.font.init()
    SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))    

#GENERAL SETTINGS
LOG_TO_CONSOLE=1 #2 for verbose, 1 for ticks,0 for nothing    

    
#SIM DATA   
AGENTS=[]  
MAX_ENERGY=10 
RADIUS=15
DIRECTIONS= [(1, 0, -1),(1, -1,0 ),(0, -1, 1),(-1, 0, 1),(-1, 1, 0),(0, 1, -1)]
COORDINATES=generate_coordinates((0,0,0),RADIUS,DIRECTIONS)
MIRROR_COORDS=generate_mirror_dict(RADIUS,COORDINATES) #need to write tests for these at some point
RESOURCES ={coord: 0 for coord in COORDINATES} 

#SIM PARAMETERS 
K=1                                      #p0001
WMAX=1000                                #p0002
ENERGY_MAX=5000                          #p0003

FOOD_FREQUENCY=1                         #p0004
FOOD_COUNT=5                             #p0005
FOOD_SIZE= int(ENERGY_MAX*0.02 )         #p0006

INITIAL_ENERGY=int(ENERGY_MAX*0.5)       #p0007
    
REST_COST=int(ENERGY_MAX*0.001 )         #p0008
TURN_COST=int(ENERGY_MAX*0.002  )        #p0009
MOVE_COST=int(ENERGY_MAX*0.001 )         #p0010
BITE_SIZE=FOOD_SIZE                      #p0011
ATTACK_COST=int(ENERGY_MAX*0.1 )         #p0012
ATTACK_DAMAGE=int(ENERGY_MAX*0.2 )       #p0013
DIVIDE_COST=int(ENERGY_MAX*0.004)        #p0014

MUTATION_AMPLITUDE=int(WMAX*0.03)        #p0015
PHENO_MUTATION_AMPLITUDE=int(WMAX*0.015)  #p0016

  
if __name__ == "__main__":
    main()