import sys 
import random as r

def tally_score(moves, game):
    # returns the agents' respective scores
    R1, S1, T1, P1 = game[0][0], game[1][0], game[2][0], game[3][0]
    R2, T2, S2, P2 = game[0][1], game[1][1], game[2][1], game[3][1]
    score1 = moves.count((0, 0)) * R1 + moves.count((0, 1)) * S1 + moves.count((1, 0)) * T1+ moves.count((1, 1)) * P1
    score2 = moves.count((0,0)) * R2 + moves.count((1, 0)) * S2 + moves.count((0,1)) * T2 + moves.count((1, 1)) * P2 
    return (score1, score2)
    # takes as input two agent strategies as strings returns their respective scores
    player1 = [i for i in agent1] #doing this since straight up assignment gives a pointer which messes stuff up.. BADLY
    player2 = [i for i in agent2]
    # print player1, player2
    moves = [(player1[2],player2[2])]
    # print player1
    # print player2
    for i in range(turns):
        # the states are updated based off of the other agent's last move
        # print moves[i]
        try: player1[0] = player1[player1[0] * 3 + moves[i][1]]
        except: 
            # used for debugging faulty mutation mechanism
            # the first number can vary here as it is used to track the player's current state
            print "check your mutation logic"
            print "p1", player1
            print "p2", player2
            print moves[-1][1]
            print moves
            sys.exit("error occurred in play_game")
        try: player2[0] = player2[player2[0] * 3 + moves[i][0]]
        except: 
            print "check your mutation logic"
            print "p1", player1
            print "p2", player2
            print moves[-1][0]
            print moves
            sys.exit("error occurred in play_game")
        try: moves.append((player1[player1[0] * 3 - 1],player2[player2[0] * 3 - 1]))
        except: 
            print"check your mutation logic"
            print player1,player2
            exit("error occurred in play_game")
        if moves[i] not in [(0, 0), (0, 1), (1, 0), (1, 1)]: 
            print "p1", player1
            print "p2", player2
            print moves, moves[i] ,moves[i][0]
            sys.exit("error occurred in play_game")
    
    return(tally_score(moves, game)) 
    

def play_game(agent1, agent2, game, turns=100, all_max=False, noise=True):
    
    # takes as input two agent strategies as strings returns their respective scores
    player1 = [i for i in agent1]
    player2 = [i for i in agent2]
    # print player1
    if sum(player1[1]) <= 1.0: joss_ann1 = (player1[1][0], player1[1][1] + player1[1][0])
    else: joss_ann1 = (1 - player1[1][1], 2 - player1[1][0] - player1[1][1]) # trippy geometry explains why we swap the values in this one
    if sum(player2[1]) <= 1.0: joss_ann2 = (player2[1][0], player2[1][0] + player2[1][1])
    else: joss_ann2 = (1 - player2[1][1], 2 - player2[1][1] - player2[1][0])
    if noise == False:
        joss_ann1, joss_ann2 = (0,0),(0,0) 
    moves = []
    
    for i in range(turns-1): # the first turn occurs right before this loop
        # the states are updated based off of the other agent's last move
        if noise: 
            p1rand,p2rand = r.random(),r.random()
        else:
            p1rand,p2rand = (1,1)
        move=[0,0]
        if joss_ann1[0] < p1rand <= joss_ann1[1] : move[0]=1
        elif joss_ann1[1] < p1rand: move[0]=player1[player1[0] * 3 - 1]
        if joss_ann2[0] < p2rand <= joss_ann2[1] : move[1]=1
        elif joss_ann2[1] < p2rand: move[1]=player2[player2[0] * 3 - 1]
        moves.append(tuple(move))
        try: player1[0] = player1[player1[0] * 3 + moves[i][1]]
        except: 
            # used for debugging faulty mutation mechanism
            # the first number can vary here as it is used to track the player's
            # current state
            print "check your mutation logic"
            print "p1", player1
            print "p2", player2
            print moves[-1][1]
            print moves
            sys.exit("error occurred in play_game 1")
        try: player2[0] = player2[player2[0] * 3 + moves[i][0]]
        except: 
            print "check your mutation logic"
            print "p1", player1
            print "p2", player2
            print moves[-1][0]
            print moves
            sys.exit("error occurred in play_game 2 ")
        if moves[i] not in [(0, 0), (0, 1), (1, 0), (1, 1)]: 
            print "p1", player1
            print "p2", player2
            print moves, moves[i], moves[i][0]
            sys.exit("error occurred in play_game 3")
        
    p1rand = r.random()
    p2rand = r.random()
    move=[0,0]
    if joss_ann1[0] < p1rand <= joss_ann1[1] : move[0]=1
    elif joss_ann1[1] < p1rand: move[0]=player1[player1[0] * 3 - 1]
    if joss_ann2[0] < p2rand <= joss_ann2[1] : move[1]=1
    elif joss_ann2[1] < p2rand: move[1]=player2[player2[0] * 3 - 1]
    moves.append(tuple(move))
    
    #stat tracking V
    cooperations= moves.count((0, 0)) * 2 + moves.count((0, 1))  + moves.count((1, 0)) 
    defections= moves.count((0, 1)) + moves.count((1, 0)) + moves.count((1, 1)) * 2
    stats=(cooperations,
            defections)
    #stat tracking ^
    return(tally_score(moves, game),stats)
    
    
def test_game_logic():
    game = [[3, 3], [0, 5], [5, 0], [1, 1]] 
    
    moves1 = ((0, 1), (0, 0))
    moves2 = ((0, 0), (0, 0), (0, 0), (0, 0))
    moves3 = ((0, 1), (1, 0), (1, 0), (1, 1), (0, 0))
    assert tally_score(moves1, game) == (3, 8)
    assert tally_score(moves2, game) == (12, 12)
    assert tally_score(moves3, game) == (14, 9)
    
    #TODO need to rewrite these test cases using r.seed() for new agent format
    agent1 = [1,[0.34,0.27], 1, 1, 1]
    agent2 = [1,[0.34,0.27], 1, 1, 1]
    agent3 = [1,[0.34,0.27], 0, 1, 1]
    agent4 = [1,[0.34,0.27], 0, 1, 2, 1, 1, 2]
    agent5 = [1,[0.34,0.27], 0, 2, 2, 1, 1, 1]
    agent6 = [1,[0.34,0.27], 0, 2, 2, 1, 3, 3, 1, 1, 1, 1, 1, 3]
    assert isinstance((play_game(agent1, agent2, game, turns = 30,noise=False)[0]), tuple)
    print play_game(agent1, agent2, game, turns =100,noise=False)[0]
    assert play_game(agent1, agent2, game, turns = 25,noise=False)[0] == (25, 25)
    assert play_game(agent1, agent3, game, turns = 40,noise=False)[0]  == (200,0)
    assert play_game(agent4, agent5, game, turns = 12,noise=False)[0]  == (28, 33)
    assert play_game(agent4, agent6, game, turns = 12,noise=False)[0]  == (22,27)
    return 'test passes'



#print test_game_logic()    

