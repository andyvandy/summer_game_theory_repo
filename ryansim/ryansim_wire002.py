import numpy as np
'''
Ryan's game theory simulation written by Andrew van den Hoeven 2015
Teams are encoded as
(give,accept) = i,j
'''
import matplotlib.pylab as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
np.set_printoptions(threshold=np.inf)

GRANULARITY=1
DIMENSION=(100/GRANULARITY+1)

def main():
    rounds=500
    do_pause=1
    random_start=0
    starting_pct=1.0 /((100/GRANULARITY+1)**2)
    if random_start:
        teams=np.random.random( (DIMENSION,DIMENSION))
        teams = teams/teams.sum()   
    else:
        teams=[starting_pct]* DIMENSION**2
        teams=np.reshape(teams, (DIMENSION,DIMENSION))
    fig ,ax= plot_init(np.matrix(teams))
    for k in range(rounds):
        teams=update(teams,k)
        plot_update(fig ,ax,np.matrix(teams),k)
        #print teams.sum()
        if k%25==1 and do_pause: pause=raw_input("press enter to continue")
    pause=raw_input("press enter to exit")
      
def update(teams,i):
    scores=calc_scores( teams)
    if i%25==1:
        print "average score:" ,scores.sum()/(DIMENSION**2)
        #print teams
    print np.where(scores==scores.max()) # use this to see what team is doing the best
    new_scores=((scores)/scores.sum()-(1.0/((100/GRANULARITY+1)**2)))+1
    teams= teams +teams*scores
    teams= teams/teams.sum()
    return teams
    
def calc_scores( teams):
    #takes in a tuple representing the team and also the population breakdown
    #returns the teams fitness
    scores=np.zeros((DIMENSION,DIMENSION))
    interim=np.array( [[100-i*GRANULARITY for i in range(DIMENSION)]]*DIMENSION )
    teams_mod=teams*interim
    #print teams
    #print interim
    #print teams_mod
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            scores[i][j] =scores[i][j]+ 0.5* (100-i*GRANULARITY) * teams[:,(DIMENSION-i):DIMENSION].sum()      #points from being a dealmaker
            scores[i][j] =scores[i][j] + 0.5 * teams_mod[j:DIMENSION,:].sum()        #points from being a dealtaker  
    return scores

def plot_init(data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal')
    X,Y=np.meshgrid(np.linspace(0., float(DIMENSION-1),DIMENSION), np.linspace(float(DIMENSION-1),0, DIMENSION))
    ax.plot_surface(X, Y, data)
    plt.title(0)
    plt.ylabel("give")
    plt.xlabel("accept")
    plt.ion()
    plt.show()
    return fig ,ax
    
def plot_update(fig,ax,data,round):
    plt.clf()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal')
    X,Y=np.meshgrid(np.linspace(0., float(DIMENSION-1),DIMENSION), np.linspace(float(DIMENSION-1),0, DIMENSION))
    ax.plot_surface(X, Y, data)
    plt.title(round)
    plt.ylabel("give")
    plt.xlabel("accept")
    plt.draw()

if __name__=="__main__":
    main()