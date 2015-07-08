import pandas as pd

class GameTurn(object):
    """This class is intended to be a template for a game. All games should
    inherit from this.
    """

    def __init__(self, number_of_players=2, **params):
        """Initializes the turn object. Ensures initial parameters are set if
        any exist.

        Args:
            number_of_players: the number of players for the game turn.
        """

        self.set_game_params(**params)

        score_labels = []
        action_labels = []

        for player in range(number_of_players):
            score_label = "agent_" + str(player + 1) + "_score"
            score_labels.append(score_label)

            action_label = "agent_" + str(player + 1) + "_action"
            action_labels.append(action_label)

        self.stats_labels = score_labels + action_labels


    def set_game_params(self, **params):
        pass


    def play(self, players, game_state, **params):
        """This function should take in the game state (whatever that is) and
        return a pandas Series of game stats using the build_stats_series 
        function. As this function will differ wildly from game to game, this 
        will probably stay empty here.
        """

        pass


    def build_stats_series(self, data):
        """Builds a pandas Series out of the stats for the turn. If you are
        writing in a new game, make sure the labels and data match up when you
        call this in your play function.

        Args:
            self.stats_labels: a list of stats label strings
            data: the actual stats corresponding to the labels

        Returns:
            turn_stats: a pandas Series containing the stats for the turn
        """

        turn_stats = pd.Series(data, index = self.stats_labels)

        return turn_stats


class TrustGameTurn(GameTurn):
    """This class defines a turn of the trust game. Inherits from the GameTurn
    class.

    Attributes:
        a: the multiplier for the first player's balance after the transfer
        b: the multiplier for the first gift
        c: the multiplier for the return gift
    """

    def set_game_params(self, **params):
        """Initializes the turn object.

        Args:
            **params: parameters including A, B, C. These are the multipliers
                for the transfers and balances.
        """

        self.a = params['A']
        self.b = params['B']
        self.c = params['C']


    def play(self, investor, trustee, investor_history, trustee_history, 
             **params):
        """Plays a turn between investor and trustee.

        Args:
            investor, trustee: the two agents to play together.
            investor_history, trustee_history: the players' moves from earlier
                                               turns

        Returns:
            turn_stats: a Pandas series containing the scores and actions of the
                two players
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

        # Build stats series.
        data = [investor.cash, trustee.cash, investor_gift, trustee_gift]
        turn_stats = self.build_stats_series(data)

        return turn_stats