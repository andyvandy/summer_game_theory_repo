

def fingerprint(genes,k):
    #takes in an agent's genes and outputs a fingerprint of the strategy
    '''We treated an agent as a ‘raven’ if for any value of its
        internal resource it fights an out-group agent but leaves the cell with an in-group
        agent. A ‘starling’ was defined as an agent that does not leave the cell in the
        presence of in-group individuals and fights out-group agents for any value of
        internal resource r # 0.5r max.'''
    scenarios=[[k,0.02,0.98,0,0,0,0,0,0,0,0,0,0 ], #low res, kin
                [k,0.5,0.5,0,0,0,0,0,0,0,0,0,0 ],  #mid res, kin
                [k,0.98,0.02,0,0,0,0,0,0,0,0,0,0 ],#high res, kin
                [k,0.02,0.98,2,2,0,0,0,0,0,0,0,0 ], #low res, non-kin
                [k,0.5,0.5,2,2,0,0,0,0,0,0,0,0 ],   #mid res, non-kin
                [k,0.98,0.02,2,2,0,0,0,0,0,0,0,0 ],]#high res, non-kin
    action_dict={0:0,
                 1:0,
                 2:0,
                 3:0,
                 4:1,
                 5:2,
                 6:3,}
    result=[0]*6            
    for i in range(6):
        output= genes*np.transpose(np.matrix(scenarios[i]))
        indices = [i for i, x in enumerate(output) if x==max(output)]
        result[i]=action_dict[r.choice(indices)]
        if len(indices)>1: 
            print "TIEEEEEEE"
    return tuple(result)