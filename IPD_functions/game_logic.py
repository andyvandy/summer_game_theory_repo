import sys 
import random as r
from class_definitions import Agent

def tally_score(moves, game):
    # returns the agents' respective scores
    R1, S1, T1, P1 = game[0][0], game[1][0], game[2][0], game[3][0]
    R2, T2, S2, P2 = game[0][1], game[1][1], game[2][1], game[3][1]
    plays=(moves.count((0, 0)),moves.count((0, 1)),moves.count((1, 0)),moves.count((1, 1))) #so that we don't call count too many times
    score1 = plays[0] * R1 + plays[1]  * S1 + plays[2] * T1+ plays[3]  * P1
    score2 = plays[0] * R2 + plays[1] * S2 + plays[2] * T2 + plays[3] * P2 
    return (score1, score2)

def play_game(agent1, agent2, game, turns=100, all_max=False, noise=False):
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
    if noise: print "Sadasdasd"
    # resets agent states
    agent1.current_state = agent1.behaviour[0]
    agent2.current_state = agent2.behaviour[0]
    
    if noise:
        # makes sure probabilities make sense
        if sum(agent1.joss_ann) <= 1.0: 
            joss_ann1 = (agent1.joss_ann[0], 
                         agent1.joss_ann[1] + agent1.joss_ann[0])
        else: 
            # trippy geometry explains why we swap the values in this one
            joss_ann1 = (1 - agent1.joss_ann[1], 
                         2 - agent1.joss_ann[0] - agent1.joss_ann[1]) 

        if sum(agent2.joss_ann) <= 1.0: 
            joss_ann2 = (agent2.joss_ann[0], 
                         agent2.joss_ann[0] + agent2.joss_ann[1])
        else: 
            joss_ann2 = (1 - agent2.joss_ann[1], 
                         2 - agent2.joss_ann[1] - agent2.joss_ann[0])


    moves = []
    
    defections=0
       
    if not noise: #seperate versions for each condition to avoid constantly checking
        for i in range(turns):
            # the states are updated based off of the other agent's last move
            
            
            move = (agent1.current_state[0],agent2.current_state[0])

            defections+=move[0] +move[1]

            

           

            moves.append(move)
            
            try: agent1.current_state = agent1.behaviour[agent1.current_state[1 + move[1]]-1]
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
            
            try: agent2.current_state = agent2.behaviour[agent2.current_state [1 + move[0]]- 1]
            except: 
                print "check your mutation logic"
                print "p1", agent1.behaviour
                print "p2", agent2.behaviour
                print "p2 state", agent2.current_state
                print moves[-1][0]
                print moves
                sys.exit("error occurred in play_game 2 ")
            #if moves[i] not in [(0, 0), (0, 1), (1, 0), (1, 1)]: 
            #    print "p1", agent1.behaviour
            #    print "p2", agent2.behaviour
            #    print moves, moves[i], moves[i][0]
            #    sys.exit("error occurred in play_game 3")
    if noise:
        for i in range(turns):
            # the states are updated based off of the other agent's last move

            p1rand, p2rand = r.random(), r.random() 
            move= [0, 0] 
            if joss_ann1[0] < p1rand < joss_ann1[1]: 
                move[0] = 1
            elif joss_ann1[1] <= p1rand: 
                move[0] = agent1.move() 
                if move[0] == None:
                    print "P1 empty move, current_state =", agent1.current_state
                    print "behaviour =", agent1.behaviour 
                    print "turn # = ", i
            if joss_ann2[0] < p2rand < joss_ann2[1]: 
                move[1] = 1
            elif joss_ann2[1] <= p2rand: 
                
                if move[1] == None:
                    print "P2 empty move, current_state =", agent2.current_state
                    print "behaviour =", agent2.behaviour
                    print "turn # = ", i
            moves.append(tuple(move))
            defections+= move[0] +move[1]
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
    cooperations= turns*2 - defections  #moves.count((0, 0)) * 2 + moves.count((0, 1))  + moves.count((1, 0)) 
 #saves a surprising amount of time compared to counting again
    stats=(cooperations,
            defections)
    #stat tracking ^

    
    
    #print agent1.score, agent2.score
    result = tally_score(moves, game)
    agent1.score += result[0]
    agent2.score += result[1]
    #print result
    #print agent1.score, agent2.score
    #print stats
    #print agent1.behaviour
    #print agent2.behaviour
    #raw_input("sadasd")
    #print len(moves)
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
    assert isinstance((play_game(agent1, agent2, game, turns = 30,noise=False)), tuple)
    assert play_game(agent1, agent2, game, turns = 30,noise=False) == (0,60)
    agent1.score,agent2.score = 0,0
    
    play_game(agent1, agent2, game, turns = 25,noise=False)
    assert  (agent1.score,agent2.score)== (25, 25)
    agent1.score,agent2.score = 0,0
    
    play_game(agent1, agent3, game, turns = 40,noise=False) 
    assert  (agent1.score,agent3.score) == (200,0)
    agent1.score,agent3.score = 0,0
    
    play_game(agent4, agent5, game, turns = 12,noise=False) 
    assert (agent4.score,agent5.score) == (28,33)
    agent4.score,agent5.score = 0,0
    
    play_game(agent4, agent6, game, turns = 12,noise=False)
    assert  (agent4.score,agent6.score) == (22,27)
    agent4.score,agent6.score = 0,0
    
    play_game(agent4, agent5, game, turns = 12,noise=False) 
    play_game(agent4, agent6, game, turns = 12,noise=False)
    play_game(agent5, agent6, game, turns = 6,noise=False)
    assert  (agent4.score , agent5.score , agent6.score) ==( 50, 43, 42)
    agent4.score, agent5.score, agent6.score = 0,0,0
    
    return 'test passes'



#print test_game_logic()    

