import random as r
import numpy as np
from agent_class import *
from log_utils import *

def play_game(agent_1, agent_2,  turns, log_file, **params):
    """Plays an iterated trust game between Agent 1 and Agent 2. Agent 1 plays
    as investor first.

    Args:
        agent_1, agent_2: two agents to play together.
        b: the multiplier for the first transfer
        c: the multiplier for the return transfer
        turns: the number of turns to be played
        log_file: the log file to write to

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
    C = params['C']
    SWAP = params['SWAP']
    LOG = params['LOG']
    
    agent_1.cash, agent_2.cash = ENDOWMENT
    agent_1_scores, agent_2_scores = np.zeros(turns), np.zeros(turns)
    agent_1_history ,agent_2_history =[],[]
    agent_1_gifts, agent_2_gifts = np.zeros(turns), np.zeros(turns)
    turn_stats = np.zeros((turns, 4))
    investor_ID = agent_1.ID
    trustee_ID = agent_2.ID

    for turn in range(turns):
        if SWAP and turn % 2 == 1:
            turn_stats[turn] = play_turn(agent_2, agent_1, agent_2_history, 
                                         agent_1_history, turn, **params)

            agent_1_scores[turn] = turn_stats[turn][1]
            agent_2_scores[turn] = turn_stats[turn][0]
            agent_1_gifts[turn] = turn_stats[turn][3]
            agent_2_gifts[turn] = turn_stats[turn][2]
        else:
            
            turn_stats[turn] = play_turn(agent_1, agent_2,  agent_1_history, 
                                            agent_2_history, turn, **params)
            #print "hists",agent_1_history,agent_2_history
            agent_1_scores[turn] = turn_stats[turn][0]
            agent_2_scores[turn] = turn_stats[turn][1]
            agent_1_gifts[turn] = turn_stats[turn][2]
            agent_2_gifts[turn] = turn_stats[turn][3]

        if SWAP:
            # Swaps the endowments before the next turn if the agents are to
            # switch places.
            agent_1_cash, agent_2_cash = agent_2_cash, agent_1_cash
            investor_ID, trustee_ID = trustee_ID, investor_ID

        if LOG:
            write_turn_info(log_file, turn, investor_ID, trustee_ID, 
                            ENDOWMENT[0], ENDOWMENT[1], turn_stats[turn][2], 
                            turn_stats[turn][3], B, C)

    #print agent_1_scores,agent_2_scores                        
    #print agent_1_gifts,agent_2_gifts

    agent_1_avg_gift = np.mean(agent_1_gifts)
    agent_2_avg_gift = np.mean(agent_2_gifts)
    agent_1_avg_score = np.mean(agent_1_scores)
    agent_2_avg_score = np.mean(agent_2_scores)
    agent_1.score += sum(agent_1_scores)
    agent_2.score += sum(agent_2_scores)
    agent_1.total_a_gifts += sum(agent_1_gifts)
    agent_2.total_b_gifts += sum(agent_2_gifts)
    agent_1.score_a += sum(agent_1_scores)
    agent_2.score_b += sum(agent_2_scores)
    
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
    
    investor_gift = investor.gift(turn, trustee_history, type = 0,**params) #turn isn't used any more in the gift function -a
    #if investor_gift: print investor_gift
    
    investor_history.append( investor_gift)
    investor_score = investor.cash - investor_gift
    
    trustee_score = trustee.cash + (B * investor_gift)
    trustee_gift = trustee.gift(turn, investor_history, type = 1,**params)
    trustee_history.append(trustee_gift)
    #print trustee_history
    trustee_score = trustee_score - trustee_gift

    investor_score = investor_score + (C * trustee_gift)

    turn_stats = (investor_score,
                  trustee_score,
                  investor_gift,
                  trustee_gift)

    return turn_stats


def play_game_test():
    """
    The more test cases we have, the better -A
    
    """
    
    #initialize test params
    params={
            
            "B":3,
            "C":1,
            "SWAP" : False, 
            "RESET" : False, 
            "MEMORY" : 2,
            "LOG" : False,
            "ENDOWMENT" : (2,0),
            }
    
    ENDOWMENT= params["ENDOWMENT"]

    intial_genome_a_1= np.array([[0,5,4,4,4,5,6,4,8,9,10,11,12,13,],
                                 [1,4,3,3,4,5,6,8,8,9,10,11,12,13,],
                                 [2,2,2,3,4,5,6,7,8,9,10,11,12,13,],
                                ])
    intial_genome_b_1=np.array([[0,1,2,3,4,5],
                                [2,1,2,3,4,5],
                                [0,4,2,0,4,5],
                                [0,3,4,5,4,5],
                                [0,0,2,6,4,5],
                                [0,1,2,3,5,5],
                                [0,1,2,3,4,6],                              
                                ])
    test_agent1=Agent(intial_genome_a_1, intial_genome_b_1, ID = (0, 1), initial_gift=1, **params)
    test_agent2=Agent(intial_genome_a_1, intial_genome_b_1, ID = (0, 2), initial_gift=2, **params)                      
    
        # test 1- sequence should be: 1->,<-2  ,   0->,<-0  ,  1->,<-3
    test_agent1.cash, test_agent2.cash = ENDOWMENT
    result=play_turn(test_agent1, test_agent2, [], [], turn=0,  **params)                               
    assert isinstance(result, tuple)
    print result
    assert result== (3,1,1,2)
    
    test_agent1.cash, test_agent2.cash = ENDOWMENT
    result=play_turn(test_agent1, test_agent2, [1], [2], turn=1,**params)    
    print result
    assert result== (2,0,0,0)
    
    test_agent1.cash, test_agent2.cash = ENDOWMENT
    result=play_turn(test_agent1, test_agent2, [1,0], [2,0], turn=2,**params)    
    print result
    assert result== (3,3,2,3)
    

    result=play_game(test_agent1, test_agent2,  3, "", **params)
    assert isinstance(result, tuple)
    print result
    assert result== (8.0/3,4.0/3,3.0/3,5.0/3)
    
        # test 2- sequence should be: 2->,<-3  ,   0->,<-0  ,  3->,<-4
    test_agent2.cash, test_agent1.cash = ENDOWMENT
    result=play_turn(test_agent2, test_agent1, [], [], turn=0,  **params)                               
    print result
    assert result== (3,3,2,3)
    
    test_agent2.cash, test_agent1.cash = ENDOWMENT
    result=play_turn(test_agent2, test_agent1, [2], [3], turn=1,**params)    
    print result
    assert result== (2,0,0,0)
    
    test_agent2.cash, test_agent1.cash = ENDOWMENT
    result=play_turn(test_agent2, test_agent1, [2,0], [3,0], turn=2,**params)    
    print result
    assert result== (3,3,2,3)
    
    result=play_game( test_agent2, test_agent1, 3, "", **params)
    assert isinstance(result, tuple)
    print result
    assert result== (8.0/3,6.0/3,4.0/3,6.0/3)
    
    
    
    print "tests pass"
    try:
        pass
    except:
        sys.exit("")
        
        
play_game_test()      
