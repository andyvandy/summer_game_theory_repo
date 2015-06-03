import random as r
import numpy as np
from agent_class import *

def play_game(agent_1, agent_2, b, turns, reset):
    """Plays an iterated trust game between Agent 1 and Agent 2. Agent 1 plays
    as investor first.

    Args:
        agent_1, agent_2: two agents to play together.
        b: the multiplier for the transfer
        turns: the number of turns to be played
        reset: a boolean determining whether or not the balance is reset for the
            players each round

    Returns:
        game_stats: a tuple containing (agent 1 score, 
                                        agent 2 score, 
                                        agent_1_avg_gift, 
                                        agent_2_avg_gift)
    """

    agent_1_balance = 100.
    agent_2_balance = 0.
    agent_1_scores = np.zeros(turns)
    agent_2_scores = np.zeros(turns)
    agent_1_history = np.zeros(turns)
    agent_2_history = np.zeros(turns)
    agent_1_gifts = np.zeros(turns)
    agent_2_gifts = np.zeros(turns)
    round_stats = np.zeros((turns, 4))

    for turn in range(turns):
        if turn % 2 == 0:
            round_stats[turn] = play_round(agent_1, agent_2, agent_1_balance,
                                            agent_2_balance, agent_1_history, 
                                            agent_2_history, b, turn)
            agent_1_scores[turn] = round_stats[turn][0]
            agent_2_scores[turn] = round_stats[turn][1]

        else:
            round_stats[turn] = play_round(agent_2, agent_1, agent_2_balance,
                                            agent_1_balance, agent_2_history, 
                                            agent_1_history, b, turn)

            agent_1_scores[turn] = round_stats[turn][0]
            agent_2_scores[turn] = round_stats[turn][1]

        agent_1_gifts[turn] = round_stats[turn][2]
        agent_1_gifts[turn] = round_stats[turn][3]

        if reset:
            agent_1_balance, agent_2_balance = agent_2_balance, agent_1_balance
        else:
            agent_1_balance = agent_1_scores[turn]
            agent_2_balance = agent_2_scores[turn]

    agent_1_avg_gift = np.mean(agent_1_gifts)
    agent_2_avg_gift = np.mean(agent_2_gifts)

    if reset:
        agent_1_score = np.sum(agent_1_scores)
        agent_2_score = np.sum(agent_2_scores)
    else:
        agent_1_score = agent_1_balance
        agent_2_score = agent_2_balance

    game_stats = (agent_1_score, 
                  agent_2_score, 
                  agent_1_avg_gift, 
                  agent_2_avg_gift)

    return game_stats


def play_turn(investor, trustee, investor_balance, trustee_balance,
               investor_history, trustee_history, b, turn):
    """Plays a single round of the trust game between investor and trustee.

    Args:
        investor, trustee: two agents to play together
        b: the multiplier for the first transfer
        investor_balance, trustee_balance: starting balances for the investor 
            and trustee
        turn: the current turn

    Returns:
        turn_stats: a tuple containing (investor score, 
                                         trustee score, 
                                         investor_gift_fraction, 
                                         trustee_gift_fraction)
    """

    investor_gift_fraction = investor.gift(turn, trustee_history) 
    investor_gift = investor_gift_fraction * investor_balance
    investor_history[turn] = investor_gift / investor_balance
    investor_score = investor_balance - investor_gift

    trustee_score = trustee_balance + investor_gift
    trustee_gift_fraction = trustee.gift(turn, investor_history) 
    trustee_gift = trustee_gift_fraction * trustee_score
    trustee_history[turn] = trustee_gift / trustee_score
    trustee_score = trustee_score - trustee_gift

    investor_score = investor_score + (b * trustee_gift)

    turn_stats = (investor_score, 
                   trustee_score, 
                   investor_gift_fraction, 
                   trustee_gift_fraction)

    return turn_stats


def play_game_test():
    """
    """
    try:
    except:
        sys.exit("")