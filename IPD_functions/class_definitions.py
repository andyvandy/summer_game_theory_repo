import json
import random as r

class Agent(object):
    """This class defines a game playing agent.

    Attributes:
        ID: A unique ID tuple containing (generation, position in generation).
        parent_ID: The unique ID of the agents parent, or None if the agent is
            from the first generation.
        current_state: The current state of the agent, starting at 0
        joss_ann: A tuple containing the Joss-Ann noise parameters of the agent,
            each ranging from 0 to 1, and summing to less than or equal to 1
        behavior: A list of tuples containing (move for this state, new state
            if coop, new state if defect)
    """

    def __init__(self, ID, behaviour, joss_ann=(0,0), parent_ID=None):
        """Inits Agent with ID, behaviour, Joss-Ann noise params, and parent ID
        """
        self.ID = ID
        self.parent_ID = parent_ID
        self.current_state = 1
        self.joss_ann = joss_ann
        self.behaviour = behaviour
        self.score = 0

    def move(self):
        try: return self.behaviour[self.current_state - 1][0]
        except:
            print "Error occurred in Agent.move. agent.current state =",
            print self.current_state, "agent.behaviour =", self.behaviour

    def change_state(self, opponent_move):
        self.current_state = self.behaviour[self.current_state - 1][opponent_move + 1]

