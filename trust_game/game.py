import random as r
import numpy as np
from agent_class import *

def play_game(agent_1, agent_2,  turns,**params):
    """Plays an iterated trust game between Agent 1 and Agent 2. Agent 1 plays
    as investor first.

    Args:
        agent_1, agent_2: two agents to play together.
        b: the multiplier for the first transfer
        c: the multiplier for the return transfer
        turns: the number of turns to be played
        swap: a boolean determining whether or not the players swap roles
            between turns

    Returns:
        game_stats: a tuple containing (agent_1_avg_score, 
                                        agent_2_avg_score, 
                                        agent_1_avg_gift, 
                                        agent_2_avg_gift)
    """
    #print params
    ENDOWMENT = params['ENDOWMENT']
    MEMORY = params['MEMORY']
    B = params['B']
    SWAP = params['SWAP']
    
    
    agent_1.cash,agent_2.cash = ENDOWMENT
    agent_1_scores, agent_2_scores = np.zeros(turns), np.zeros(turns)
    agent_1_history ,agent_2_history = np.zeros(turns), np.zeros(turns)
    agent_1_gifts, agent_2_gifts = np.zeros(turns), np.zeros(turns)
    turn_stats = np.zeros((turns, 4))

    for turn in range(turns):
        if SWAP and turn % 2 == 1:
            turn_stats[turn] = play_turn(agent_2, agent_1, agent_2_history, 
                                         agent_1_history, turn, **params)

            agent_1_scores[turn] = turn_stats[turn][1]
            agent_2_scores[turn] = turn_stats[turn][0]
            agent_1_gifts = turn_stats[turn][3]
            agent_2_gifts = turn_stats[turn][2]
        else:
            turn_stats[turn] = play_turn(agent_1, agent_2,  agent_1_history, 
                                            agent_2_history, turn, **params)

            agent_1_scores[turn] = turn_stats[turn][0]
            agent_2_scores[turn] = turn_stats[turn][1]
            agent_1_gifts = turn_stats[turn][2]
            agent_2_gifts = turn_stats[turn][3]

        if SWAP:
            # Swaps the endowments before the next turn if the agents are to
            # switch places.
            agent_1_balance, agent_2_balance = agent_2_balance, agent_1_balance

    agent_1_avg_gift = np.mean(agent_1_gifts)
    agent_2_avg_gift = np.mean(agent_2_gifts)
    agent_1_avg_score = np.mean(agent_1_scores)
    agent_2_avg_score = np.mean(agent_2_scores)
    agent_1.score+=sum(agent_1_scores)
    agent_2.score+=sum(agent_1_scores)
    
    game_stats = (agent_1_avg_score, 
                  agent_2_avg_score, 
                  agent_1_avg_gift, 
                  agent_2_avg_gift)

    return game_stats


def play_turn(investor, trustee, investor_history, trustee_history, turn, 
              **params):
    """Plays a single turn of the trust game between investor and trustee.

    Args:
        investor, trustee: two agents to play together
        b: the multiplier for the first transfer
        c: the multiplier for the return transfer
        investor_balance, trustee_balance: starting balances for the investor 
            and trustee
        turn: the current turn

    Returns:
        turn_stats: a tuple containing (investor score, 
                                         trustee score, 
                                         investor_gift_fraction, 
                                         trustee_gift_fraction)
    """
    B = params['B']
    C = params['C']
    
    investor_gift = investor.gift(turn, trustee_history, type = 0,**params)
    investor_history[turn] = investor_gift
    investor_score = investor.cash - investor_gift

    trustee_score = trustee.cash + (B * investor_gift)
    trustee_gift = trustee.gift(turn, investor_history, type = 1,**params)
    trustee_history[turn] = trustee_gift
    trustee_score = trustee_score - trustee_gift

    investor_score = investor_score + (C * trustee_gift)

    turn_stats = (investor_score,
                  trustee_score,
                  investor_gift,
                  trustee_gift)

    return turn_stats


def play_game_test():
    """
    """
    try:
        pass
    except:
        sys.exit("")