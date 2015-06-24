from agent_class import Agent

class TrustGameTurn(object):
    """This class defines a turn of the trust game. This is where the rules 
    should be.

    Attributes:
        A: the multiplier for the first player's balance after the transfer
        B: the multiplier for the first gift
        C: the multiplier for the return gift
    """

    def __init__(self, a, b, c):
        "Initializes the turn object."
        self.a = a
        self.b = b
        self.c = c

    def play(self, investor, trustee, investor_history, trustee_history, 
             **params):
        """Plays a turn between investor and trustee.

        Args:
            investor, trustee: the two agents to play together.
            investor_history, trustee_history: the players' moves from earlier
                                               turns

        Returns:
            turn_stats: a tuple containing(investor_score,
                                           trustee_score,
                                           investor_gift_fraction,
                                           trustee_gift_fraction)
        """

        # Get the initial gift
        investor_gift = investor.gift(trustee_history, type = 0, **params)

        # Add the initial gift to the history
        investor_history.append(investor_gift)

        # Modify the agents' cash to reflect the gift
        investor.cash = (investor.cash - investor_gift) * self.a
        trustee.cash = trustee.cash + (self.b * investor_gift)

        # Get the return gift
        trustee_gift = trustee.gift(investor_history, type = 1, **params)

        # Add the return gift to the history
        trustee_history.append(trustee_gift)

        # Modify the agents' cash to reflect the gift
        trustee.cash = trustee.cash - trustee_gift
        investor.cash = investor.cash + (self.c * trustee_gift)

        # Build stats tuple
        turn_stats = (investor.cash,
                      trustee.cash,
                      investor_gift,
                      trustee_gift)

        return turn_stats