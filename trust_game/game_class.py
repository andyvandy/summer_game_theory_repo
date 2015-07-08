import random as r
import numpy as np
import pandas as pd

from turn_class import TrustGameTurn


class Game(object):
    """This class defines a game between two or more players. All games should
    inherit from this class.

    Attributes:
    """

    def __init__(self, **params):
        """Initializes the game object.
        """

        self.set_game_params(**params)


    def set_game_params(self, **params):
        pass


    def play(self, agents, turns):
        pass



class TrustGame(Game):
    """This class defines a trust game between two players consisting of turn(s) 
    which may or may not be (but currently are) identical.

    Attributes:
    """

    def set_game_params(self, **params):
        """Sets the game parameters.

        Args:
            endowment: a tuple specifying the initial (agent_1_cash, agent_2_cash)
            a: the multiplier for the first player's balance after the transfer
            b: the multiplier for the first gift
            b: the multiplier for the return gift
        """

        self.endowment = params["ENDOWMENT"]
        self.a = params["A"]
        self.b = params["B"]
        self.c = params["C"]


    def play(self, agent_1, agent_2, turns, LOG=False, log_file=None, **params):
        """Plays an iterated trust game between agent_1 and agent_2. agent_1 is 
        the investor and agent_2 is the trustee.

        Args:
            agent_1, agent_2: the two agents to play together
            turns: the number of iterations
            LOG: whether or not to write logs
            log_file: the file to write logs to

        Returns:
            game_stats: a panadas DataFrame
        """

        # Initialize history lists
        agent_1_history, agent_2_history = [], []

        # Initialize turn object
        turn = TrustGameTurn(**params)

        # Initialize turn stats list
        turn_stats_list = []

        # Play the game
        for i in range(turns):
            # Set agents' cash to match endowment
            agent_1.cash, agent_2.cash = self.endowment

            # Play a turn
            turn_stats = turn.play(agent_1, agent_2, agent_1_history,
                                   agent_2_history, **params)

            turn_stats.name = "turn_" + str(i)

            # Add turn stats to list of turn stats
            turn_stats_list.append(turn_stats)

            # Log turn data
            if LOG:
                pass

        game_stats = pd.DataFrame(turn_stats_list, index = range(turns))

        # Update agent stat attributes. Hopefully we can do away with this soon.
        agent_1.score += sum(game_stats['agent_1_scores'])
        agent_2.score += sum(game_stats['agent_2_scores'])
        agent_1.total_a_gifts += sum(game_stats['agent_1_actions'])
        agent_2.total_b_gifts += sum(game_stats['agent_2_actions'])
        agent_1.score_a += sum(game_stats['agent_1_scores'])
        agent_2.score_b += sum(game_stats['agent_2_scores'])

        return game_stats