import sys 
import random as r
from class_definitions import Agent

def tally_score(moves, game):
    # returns the agents' respective scores
    R1, S1, T1, P1 = game[0][0], game[1][0], game[2][0], game[3][0]
    R2, T2, S2, P2 = game[0][1], game[1][1], game[2][1], game[3][1]
    score1 = moves.count((0, 0)) * R1 + moves.count((0, 1)) * S1 + moves.count((1, 0)) * T1+ moves.count((1, 1)) * P1
    score2 = moves.count((0,0)) * R2 + moves.count((1, 0)) * S2 + moves.count((0,1)) * T2 + moves.count((1, 1)) * P2 
    return (score1, score2)

def play_game(agent1, agent2, game, turns=100, all_max=False, noise=True):
    """Plays a game between agent1 and agent2
    
    Args:
        agent1:
        agent2:
        game:
        turns:
        all_max:
        noise:

    Returns:
        
    """
    # resets agent states
    agent1.current_state = 1
    agent2.current_state = 1
    
    if noise == True:
        # makes sure probabilities make sense
        if sum(agent1.joss_ann) <= 1.0: 
            joss_ann1 = (agent1.joss_ann[0], 
                         agent1.joss_ann[1] + agent1.joss_ann[0])
        else: 
            # trippy geometry explains why we swap the values in this one
            joss_ann1 = (1 - agent1.joss_ann[1], 
                         2 - agent1.joss_ann[1][0] - agent1.joss_ann[1][1]) 

        if sum(agent2.joss_ann) <= 1.0: 
            joss_ann2 = (agent2.joss_ann[0], 
                         agent2.joss_ann[0] + agent2.joss_ann[1])
        else: 
            joss_ann2 = (1 - agent2.joss_ann[1], 
                         2 - agent2.joss_ann[1][1] - agent2.joss_ann[1][0])
    else:
        joss_ann1, joss_ann2 = (0, 0), (0, 0) 

    moves = []
    
    for i in range(turns):
        # the states are updated based off of the other agent's last move
        if noise: 
            p1rand, p2rand = r.random(), r.random()
        else:
            p1rand, p2rand = (1, 1)

        move = [0, 0]

        if joss_ann1[0] < p1rand <= joss_ann1[1]:
            move[0] = 1
        elif joss_ann1[1] < p1rand: 
            move[0] = agent1.move()
            if move[0] == None:
                print "P1 empty move, current_state =", agent1.current_state
                print "behaviour =", agent1.behaviour 
                print "turn # = ", i

        if joss_ann2[0] < p2rand <= joss_ann2[1]: 
            move[1] = 1
        elif joss_ann2[1] < p2rand: 
            move[1] = agent2.move()
            if move[1] == None:
                print "P2 empty move, current_state =", agent2.current_state
                print "behaviour =", agent2.behaviour
                print "turn # = ", i

        moves.append(tuple(move))
        
        try: agent1.current_state = agent1.behaviour[agent1.current_state - 1][1 + move[1]]
        except: 
            # used for debugging faulty mutation mechanism
            # the first number can vary here as it is used to track the player's
            # current state
            print "check your mutation logic"
            print "p1", agent1.behaviour
            print "p2", agent2.behaviour
            print moves[-1][1]
            print moves
            sys.exit("error occurred in play_game 1")
        
        try: agent2.current_state = agent2.behaviour[agent2.current_state - 1][1 + move[0]]
        except: 
            print "check your mutation logic"
            print "p1", agent1.behaviour
            print "p2", agent2.behaviour
            print "p2 state", agent2.current_state
            print moves[-1][0]
            print moves
            sys.exit("error occurred in play_game 2 ")
        if moves[i] not in [(0, 0), (0, 1), (1, 0), (1, 1)]: 
            print "p1", agent1.behaviour
            print "p2", agent2.behaviour
            print moves, moves[i], moves[i][0]
            sys.exit("error occurred in play_game 3")
    
    #stat tracking V
    cooperations= moves.count((0, 0)) * 2 + moves.count((0, 1))  + moves.count((1, 0)) 
    defections= moves.count((0, 1)) + moves.count((1, 0)) + moves.count((1, 1)) * 2
    stats=(cooperations,
            defections)
    #stat tracking ^

    result = tally_score(moves, game)
    agent1.score += result[0]
    agent2.score += result[1]

    return stats
    
    
def test_game_logic():
    game = [[3, 3], [0, 5], [5, 0], [1, 1]] 
    
    moves1 = ((0, 1), (0, 0))
    moves2 = ((0, 0), (0, 0), (0, 0), (0, 0))
    moves3 = ((0, 1), (1, 0), (1, 0), (1, 1), (0, 0))
    assert tally_score(moves1, game) == (3, 8)
    assert tally_score(moves2, game) == (12, 12)
    assert tally_score(moves3, game) == (14, 9)
    
    #TODO need to rewrite these test cases using r.seed() for new agent format
    #agent1 = [1,[0.34,0.27], 1, 1, 1]
    #agent2 = [1,[0.34,0.27], 1, 1, 1]
    #agent3 = [1,[0.34,0.27], 0, 1, 1]
    #agent4 = [1,[0.34,0.27], 0, 1, 2, 1, 1, 2]
    #agent5 = [1,[0.34,0.27], 0, 2, 2, 1, 1, 1]
    #agent6 = [1,[0.34,0.27], 0, 2, 2, 1, 3, 3, 1, 1, 1, 1, 1, 3]

    agent1 = Agent((0, 0), ((1, 1, 1),), (0.34, 0.27))
    agent2 = Agent((0, 0), ((1, 1, 1),), (0.34, 0.27))
    agent3 = Agent((0, 0), ((0, 1, 1),), (0.34, 0.27))
    agent4 = Agent((0, 0), ((0, 1, 2), (1, 1, 2)), (0.34, 0.27))
    agent5 = Agent((0, 0), ((0, 2, 2), (1, 1, 1)), (0.34, 0.27))
    agent6 = Agent((0, 0), ((0, 2, 2), (1, 3, 3), (1, 1, 1), (1, 1, 3)), (0.34, 0.27))

    assert isinstance((play_game(agent1, agent2, game, turns = 30,noise=False)[0]), tuple)
    print play_game(agent1, agent2, game, turns =100,noise=False)[0]
    assert play_game(agent1, agent2, game, turns = 25,noise=False)[0] == (25, 25)
    assert play_game(agent1, agent3, game, turns = 40,noise=False)[0]  == (200,0)
    assert test == play_game(agent4, agent5, game, turns = 12,noise=False)[0]
    assert play_game(agent4, agent6, game, turns = 12,noise=False)[0]  == (22,27)
    return 'test passes'



# print test_game_logic()    

