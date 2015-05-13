from fingerprint import fingerprint


def log_population_mix(tick,agents,k):
    #Records the sorted population mix
    ravens=0
    starlings=0
    doves=0
    hawks=0
    others=0
    
    
    for agent in agents:
        total+=1
        fprint=fingerprint(agent.genes,k)
        if fprint==(1,1,1,2,2,2):
            ravens+=1
        elif fprint[0],fprint[1],fprint[2]!=1 and fprint[4],fprint[5]==2:
            starlings+=1
        elif  fprint[0],fprint[1],fprint[2],fprint[3],fprint[4],fprint[5]!=1:
            doves+=1
        elif  fprint[0],fprint[1],fprint[2],fprint[3],fprint[4],fprint[5]==1:
            hawks+=1
        else:
            others+=1
    
    
    return(tick, total,(ravens,starlings,doves,hawks,others)