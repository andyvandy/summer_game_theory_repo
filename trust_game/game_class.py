import random as r
import numpy as np

from turn_class import TrustGameTurn

class TrustGame(object):
    """This class defines a trust game between two players consisting of turn(s) 
    which may or may not be (but currently are) identical.

    Attributes:
    """

    def __init__(self, **params):
        """Initializes the game object.

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


    def play(self, agent_1, agent_2, turns, log=False, log_file=None, **params):
        """Plays an iterated trust game between agent_1 and agent_2. agent_1 is 
        the investor and agent_2 is the trustee.

        Args:
            agent_1, agent_2: the to agents to play together
            turns: the number of iterations
            log: whether or not to write logs
            log_file: the file to write logs to

        Returns:
            game_stats: a tuple containing (agent_1_avg_score, 
                                            agent_2_avg_score, 
                                            agent_1_avg_gift, 
                                            agent_2_avg_gift)
        """

        # Initialize score arrays
        agent_1_scores, agent_2_scores = np.zeros(turns), np.zeros(turns)

        # Initialize history lists
        agent_1_history, agent_2_history

        # Initialize gift arrays
        agent_1_gifts, agent_2_gifts = np.zeros(turns), np.zeros(turns)

        # Initialize stats array
        turn_stats = np.zeros((turns, 4))

        # Initialize turn object
        turn = TrustGameTurn(self.a, self.b, self.c)

        # Play the game
        for i in range(turns):
            # Set agents' cash to match endowment
            agent_1.cash, agent_2.cash = self.endowment

            # Play a turn
            turn_stats[i] = turn.play(agent_1, agent_2, agent_1_history,
                                      agent_2_history, **params)

            # Unpack stats tuple into lists
            agent_1_scores[turn] = turn_stats[turn][0]
            agent_2_scores[turn] = turn_stats[turn][1]
            agent_1_gifts[turn] = turn_stats[turn][2]
            agent_2_gifts[turn] = turn_stats[turn][3]

            # Log turn data
            if LOG:
                pass

        # Calculate game stats
        agent_1_avg_gift = np.mean(agent_1_gifts)
        agent_2_avg_gift = np.mean(agent_2_gifts)
        agent_1_avg_score = np.mean(agent_1_scores)
        agent_2_avg_score = np.mean(agent_2_scores)

        # Update agent stat attributes
        agent_1.score += sum(agent_1_scores)
        agent_2.score += sum(agent_2_scores)
        agent_1.total_a_gifts += sum(agent_1_gifts)
        agent_2.total_b_gifts += sum(agent_2_gifts)
        agent_1.score_a += sum(agent_1_scores)
        agent_2.score_b += sum(agent_2_scores)

        # Pack game stats
        game_stats = (agent_1_avg_score, 
                      agent_2_avg_score, 
                      agent_1_avg_gift, 
                      agent_2_avg_gift)

        return game_stats