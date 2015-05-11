import json
import random as r

class Agent(object):
    
    def __init__(self, ID, behaviour, joss_ann=(0,0), parent_ID=None):
        self.ID = ID
        self.parent_ID = parent_ID
        self.current_state = 1
        self.joss_ann = joss_ann
        self.behaviour = behaviour
            

        

    
        
