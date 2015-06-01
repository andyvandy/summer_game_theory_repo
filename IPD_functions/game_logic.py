import sys 
import random as r
from class_definitions import Agent
from collections import deque


def tally_score(play_records, game):
    # returns the agents' respective scores
    #needs to be fixed for games larger than 2x2
    R1, S1, T1, P1 = game[0][0], game[1][0], game[2][0], game[3][0]
    R2, T2, S2, P2 = game[0][1], game[1][1], game[2][1], game[3][1]
    #play=(moves.count((0, 0)),moves.count((0, 1)),moves.count((1, 0))) #so that we don't call count too many times
    #play0,play1,play2,play3=(play[0],play[1],play[2],len(moves)-play[0]-play[1]-play[2]) #more avoiding count
    
    play0,play1,play2,play3=play_records 
    score1 = play0 * R1 + play1  * S1 + play2 * T1+ play3  * P1
    score2 = play0 * R2 + play2 * S2 + play1 * T2 + play3 * P2 
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
    agent1.state_number = 1
    agent2.current_state = agent2.behaviour[0]
    agent1.state_number = 1
    
    
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
    
    playbook={ (0,0):0,  #needs to be fixed for games larger than 2x2 ,should maybe be passed as an argument
                (0,1):1,
                (1,0):2,
                (1,1):3,
                    }
    play_records=[0]*len(playbook)
    state_records=[]
    moves = [0]*turns
    defections=0
    loop_detected=False
    #state_logs=deque([(0,0)]*4 )  # use this to keep track of infinitely repeating loops
    first=True      #placeholder need to optimize this later
    if not noise: #separate versions for each condition to avoid constantly checking
        for i in range(turns):
            # the states are updated based off of the other agent's last move
            
            
            (move1,move2) = (agent1.current_state[0],agent2.current_state[0])

            defections+=move1 +move2
            

            

            moves[i]=(move1,move2)

            play_records[playbook[(move1,move2)]]+=1

            next_state_agent1=agent1.current_state[1 + move2]-1
            next_state_agent2=agent2.current_state[1 + move1]-1
            #check for infinite loops , should add more cases
            #if state_logs[-1][0]==state_logs[-2][0] and state_logs[-1][1]==state_logs[-2][1]:
            
            new_state_record_entry=(( agent1.state_number, agent2.state_number),(move1,move2))
            if new_state_record_entry not in state_records:
                state_records.append(new_state_record_entry)
            else:
                index=state_records.index(new_state_record_entry)
                #print "gassad" ,new_state_record_entry
                #print state_records
                if index: 
                    for j in range(index):
                       del  state_records[0]
                loop_detected=i
                break
            agent1.state_number=next_state_agent1 +1
            agent2.state_number=next_state_agent2 +1
            '''if  agent1.current_state == agent1.behaviour[agent1.current_state[1 + move2]-1]:
                if  agent2.current_state == agent2.behaviour[agent2.current_state[1 + move1]-1]:
                    #the agents are caught in an infinite loop, we can save some time
                    #this is the biggest time saver ever. omg omg omg makes it like 30 times faster
                    #for j in range(turns-i-1):
                        #moves[i]=(move1,move2)
                    #print "this happened!" 
                    defections+=(turns-i-1)*(move1 + move2)
                    play_records[playbook[(move1,move2)]]+=turns-i-1    
                    break'''
                
            '''elif state_logs[-1][0]==state_logs[-3][0] and state_logs[-2][0]==state_logs[-4][0]  and  state_logs[-1][1]==state_logs[-3][1] and state_logs[-2][1]==state_logs[-4][1] :
                defections+=((turns-i-1)/2)*(move1 + move2)
                #this needs to be tested
                play_records[playbook[(move1,move2)]]+=(turns-i-1  )/2
                #print "this happened too!" # apparently it does
                if first ==False:
                    break
                first=False'''
                
            
            try: agent1.current_state = agent1.behaviour[next_state_agent1]
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
            
            try: agent2.current_state = agent2.behaviour[next_state_agent2]
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
    #print play_records 
    #print state_records
    
    #print "hhhm", loop_detected
    if loop_detected:
        loop_length=len(state_records)
        counter=1%loop_length# took a while to realize this should be a 1 rather than 0
        
        turn =loop_detected
        #print turn 
        #print turns
        #print " tessstinggg 123 testtinng  123"
        while turn < turns-1:
            turn +=1
            #print turn
            move=state_records[counter][1]
            moves[turn]=move
            defections+=move[0] +move[1]
            play_records[playbook[move]]+=1
            counter= (counter+1)%loop_length
            
    #print play_records        
    #print moves       
    if noise:
        #separate version for noisy games since it's decently slower
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
            
            play_records[playbook[(move[0],move[1])]]+=1
            
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
    result = tally_score(play_records, game)
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
    #print tally_score(moves1, game)
    #assert tally_score(moves1, game) == (3, 8)
    #assert tally_score(moves2, game) == (12, 12)
    #assert tally_score(moves3, game) == (14, 9)
    
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
    print play_game(agent1, agent2, game, turns = 30,noise=False)
    assert play_game(agent1, agent2, game, turns = 30,noise=False) == (0,60)

    agent1.score,agent2.score = 0,0
    
    play_game(agent1, agent2, game, turns = 25,noise=False)
    assert  (agent1.score,agent2.score)== (25, 25)
    agent1.score,agent2.score = 0,0
    
    play_game(agent1, agent3, game, turns = 40,noise=False) 
    assert  (agent1.score,agent3.score) == (200,0)
    agent1.score,agent3.score = 0,0
    
    agent4.score,agent5.score = 0,0
    play_game(agent4, agent5, game, turns = 12,noise=False) 
    assert (agent4.score,agent5.score) == (28,33)
    agent4.score,agent5.score = 0,0
    
    play_game(agent4, agent6, game, turns = 12,noise=False)
    print (agent4.score,agent6.score)
    assert  (agent4.score,agent6.score) == (22,27)
    agent4.score,agent6.score = 0,0
    
    play_game(agent4, agent5, game, turns = 12,noise=False) 
    play_game(agent4, agent6, game, turns = 12,noise=False)
    play_game(agent5, agent6, game, turns = 6,noise=False)
    assert  (agent4.score , agent5.score , agent6.score) ==( 50, 43, 42)
    agent4.score, agent5.score, agent6.score = 0,0,0
    
    return 'test passes'



#print test_game_logic()    

