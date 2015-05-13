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
from burtsev_centroid import deviation_from_centroid, centroidnp
from burtsev_utilities import count_agents,agents_in_cell

def main():
    
    run_simulation(starting_pop=10)
        
          
                 

class Agent:
    def __init__(self,parent_genes,initial_location,initial_energy,phenotype,parent_direction):
        self.location = initial_location
        self.genes=parent_genes  
        self.energy = initial_energy
        self.phenotype=phenotype
        self.direction=parent_direction 
    
    def turn(self,right=True):
        x,y,z=self.direction
        if right:self.direction=rotate(self.direction,1) # two wrongs don't make a right,
        else:self.direction=rotate(self.direction,5) # but five rights make a left!
        self.pay_energy(0.012)#param
    def rest(self):
        self.pay_energy(0.01)#param
    def move_forward(self):
        x,y,z=tuple(self.location)
        x1,y1,z1=self.direction
        self.location=MIRROR_COORDS[(x+x1,y+y1,z+z1)]
        draw_agent(self)#drawing
        draw_food((x,y,z))#drawing
        self.pay_energy(0.04)#param
    def pay_energy(self,amount):
        self.energy-=amount
        if self.energy<=0:
            #print "ouch"
            coord=self.location
            del(AGENTS[AGENTS.index(self)])
            draw_food(coord)#drawing
    def feed(self):
        amount=min(RESOURCES[self.location],0.06) #param
        RESOURCES[self.location]=RESOURCES[self.location]-amount
        self.energy= min(self.energy+amount,ENERGY_MAX)
        if amount==0: self.rest()
    def attack(self,victim):
        #print victim
        #print victim.energy
        victims_energy=victim.energy
        tasty_flesh=min(victims_energy,0.2)
        self.energy= min(self.energy+tasty_flesh,ENERGY_MAX)
        victim.pay_energy(tasty_flesh)
        self.pay_energy(0.1)#param
    def divide(self): 
        #TODO clean up lol
        offspring_phenotype=[0,0,0,0,0,0,0,0,0]
        red1,green1,blue1,red2,green2,blue2,red3,green3,blue3=self.phenotype
        rm1,gm1,bm1= r.choice(((0,0,0), (0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0)))
        rm2,gm2,bm2= r.choice(((0,0,0), (0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0)))
        rm3,gm3,bm3= r.choice(((0,0,0), (0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0)))
        intensity=r.randint(1,15)
        rm1*=intensity
        gm1*=intensity
        bm1*=intensity
        rm2*=intensity
        gm2*=intensity
        bm2*=intensity
        rm3*=intensity
        gm3*=intensity
        bm3*=intensity
        offspring_phenotype= (min(255,max(0,red1+rm1)),min(255,max(0,green1+gm1)),min(255,max(0,blue1+bm1)),
                               min(255,max(0,red2+rm2)),min(255,max(0,green2+gm2)),min(255,max(0,blue2+bm2)),
                                min(255,max(0,red3+rm3)),min(255,max(0,green3+gm3)),min(255,max(0,blue3+bm3)),
                                )
            
        #print offspring_phenotype
        AGENTS.append(Agent(parent_genes=self.genes+ np.random.uniform(-0.15,0.15,(7,11)),
                        initial_location=self.location,
                         initial_energy=self.energy/2.0-0.2,
                         phenotype=offspring_phenotype,
                         parent_direction=self.direction))
        self.pay_energy(self.energy/2.0 +0.2)
        



def tally_energy():
    #returns the net sum of energy among all agents
    agent_energy=0
    for agent in AGENTS:
        agent_energy+= agent.energy
    available_energy= sum([RESOURCES[coord] for coord in COORDINATES])
    return agent_energy,available_energy

   

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
    ag1=pygame.Color(r1,g1,b1)
    ag2=pygame.Color(r2,g2,b2)
    ag3=pygame.Color(r3,g3,b3)
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
    
    initialize_screen()

    
    #initialize agents
    initial_strategy=np.zeros((7,11))
    initial_strategy[3][1]=10
    initial_strategy[4][4]=7
    initial_strategy[6][2]=2
    initial_phenotype=(255,255,150,150,255,255,255,150,255)                  
    print initial_strategy
    
    for i in range(starting_pop):
        spawn_location=r.choice(COORDINATES)
        initial_direction=r.choice(DIRECTIONS)
        AGENTS.append(Agent(parent_genes=initial_strategy,
                        initial_location=spawn_location,
                         initial_energy=INITIAL_ENERGY, #p0007
                         phenotype=initial_phenotype,
                         parent_direction=initial_direction))
    tick=1
    print "total energy: ", tally_energy()
    print "total agents: ", len(AGENTS)
    while tick :
        pygame.display.update()
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit(); sys.exit();
        
        
        
        tick+=1
        if tick%FOOD_FREQUENCY==0: #p0004
            for i in range(FOOD_COUNT): #p0005
                coord=r.choice(COORDINATES)
                RESOURCES[coord]+=FOOD_SIZE #p0006
                draw_food(coord)        
                
        for agent in AGENTS:
            directional_resources= [ bool(RESOURCES[MIRROR_COORDS[tuple(map(operator.add, agent.location , rotate(agent.direction,i)))]]) for i in [0,1,5]]
            directional_agents=[ count_agents(MIRROR_COORDS[tuple(map(operator.add, agent.location ,rotate(agent.direction,i)))],AGENTS) for i in [0,1,5]]
            dev_from_centroid=deviation_from_centroid(agent,agent.location,AGENTS)
            
            # p0001 , p0003
            input=np.transpose(np.matrix([K,bool(RESOURCES[agent.location]),  agent.energy, ENERGY_MAX] +directional_resources+directional_agents+[dev_from_centroid]))

            output=agent.genes*input
            #print output
            indices = [i for i, x in enumerate(output) if x==max(output)]
            action=r.choice(indices)
            #print indices,action
            #sys.pause()
            if action ==0: agent.rest()
            elif action ==1: agent.turn(right=True)
            elif action ==2: agent.turn(right=False)
            elif action==3: agent.feed()
            elif action==4: agent.move_forward()    
            elif action==5: 
                candidates=agents_in_cell(agent.location,AGENTS)
                targets= []
                if len(candidates)>1:
                    for target in candidates:
                        if target != agent: targets.append(target)
                    agent.attack(r.choice(targets)) 
                else: agent.rest() #need to fix up later to make randomly attacking not good
            elif action==6: agent.divide()     
            else:print "error"
            
            
         
        if tick%50==0:
            
            agent_energy, available_energy=tally_energy()
            draw_world_stats((len(AGENTS),round(agent_energy,2),round(available_energy,2),tick/100.0))   

            print "total agent energy: ", agent_energy
            print "total agents: ", len(AGENTS)
            print "available energy: ", available_energy
            print tick/50
            if agent_energy==0:tick=False
    

#GRAPHICS SETTINGS
WIDTH=1000
HEIGHT=600
pygame.init()
pygame.font.init()
SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))    

#SIM DATA   
AGENTS=[]  
MAX_ENERGY=10 
RADIUS=15
DIRECTIONS= [(1, 0, -1),(1, -1,0 ),(0, -1, 1),(-1, 0, 1),(-1, 1, 0),(0, 1, -1)]
COORDINATES=generate_coordinates((0,0,0),RADIUS,DIRECTIONS)
MIRROR_COORDS=generate_mirror_dict(RADIUS,COORDINATES) #need to write tests for these at some point
RESOURCES ={coord: 1 for coord in COORDINATES} #param

#SIM PARAMETERS 
K=1                     #p0001
WMAX=1000               #p0002
ENERGY_MAX=100.0        #p0003
FOOD_FREQUENCY=1        #p0004
FOOD_COUNT=5            #p0005
FOOD_SIZE= 0.2          #p0006
INITIAL_ENERGY=10       #p0007

    
if __name__ == "__main__":
    main()