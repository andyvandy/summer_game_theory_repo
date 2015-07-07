import numpy as np
'''
Ryan's game theory simulation written by Andrew van den Hoeven 2015
Teams are encoded as
(give,accept) = i,j
'''
import matplotlib.pylab as plt
from matplotlib import animation
import matplotlib.gridspec as gridspec
import seaborn as sns
import matplotlib

GRANULARITY=1
DIMENSION=(100/GRANULARITY+1)
STARTING_PCT=1.0 /((100/GRANULARITY+1)**2)
rounds=500
avg_deal_data=[]
matplotlib.use('GTKAgg') 

def main():
    random_start=0
    do_pause=1
    if random_start:
        teams=np.random.random( (DIMENSION,DIMENSION))
        teams = teams/teams.sum()   
    else:
        teams=[STARTING_PCT]* DIMENSION**2
        teams=np.reshape(teams, (DIMENSION,DIMENSION))
    fig ,axarr= plot_init(np.matrix(teams))
    for k in range(rounds):
        print "round:" ,k
        teams=update(teams,k)
        if k%25==0 and do_pause: plt.waitforbuttonpress()
        plot_update(fig ,axarr,teams,k)
        
    pause=raw_input("press enter to exit")
    
def update(teams,k):
    scores=calc_scores( teams)
    avg_deal_data.append(scores.sum()/(DIMENSION**2))
    print "avg cash per deal", avg_deal_data[-1]
    max_locations= np.where(scores==scores.max()) #todo: print and parse this
    total_sum=np.sum(scores*teams)
    new_scores=((scores)/total_sum-(1.0/((100/GRANULARITY+1)**2)))+np.ones((DIMENSION,DIMENSION))
    teams= teams*new_scores
    teams= teams/teams.sum()
    return teams
    
def calc_scores( teams):
    #takes in a tuple representing the team and also the population breakdown
    #returns the teams fitness
    scores=np.zeros((DIMENSION,DIMENSION))
    interim=np.array( [[100-i*GRANULARITY for i in range(DIMENSION)]]*DIMENSION )
    teams_mod=teams*interim
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            scores[i][j] =scores[i][j]+ 0.5* (100-i*GRANULARITY) * teams[:,(DIMENSION-i):DIMENSION].sum()      #points from being a dealmaker
            scores[i][j] =scores[i][j] + 0.5 * teams_mod[j:DIMENSION,:].sum()        #points from being a dealtaker
    return scores
    
def plot_init(data):
    sns.set_style("dark")
    fig = gridspec.GridSpec(2, 1)
    axarr= [plt.subplot(fig[0,0]),plt.subplot(fig[1, 0])]
    img=axarr[0].imshow(data, interpolation='nearest', cmap=plt.cm.ocean,
        extent=(0.5,np.shape(data)[0]+0.5,0.5,np.shape(data)[1]+0.5))
    plt.title("Current Round:" +str(0))
    axarr[0].set_ylabel("Give")
    axarr[0].set_xlabel("Accept")
    axarr[0].set_title("Distribution of Teams")
    axarr[1].plot(avg_deal_data)
    axarr[1].set_xlim(0,rounds)
    axarr[1].set_ylabel("Average Cash per Deal")
    axarr[1].set_xlabel("Round Number")
    plt.colorbar(img,ax=axarr[0],label= "Prevalence vs. Uniform")
    plt.ion()
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()
    return fig ,axarr
    
def plot_update(fig,axarr,data,round):
    plt.cla()
    dota=  data/STARTING_PCT
    axarr= [plt.subplot(fig[0,0]),plt.subplot(fig[1, 0])]
    img=axarr[0].imshow(dota, interpolation='nearest', cmap=plt.cm.ocean,
        extent=(0.5,np.shape(dota)[0]+0.5,0.5,np.shape(dota)[1]+0.5)) 
    axarr[1].plot(avg_deal_data)
    axarr[1].set_xlim(0,rounds)
    plt.title("Current Round:" +str(round))
    axarr[0].set_ylabel("Give")
    axarr[0].set_xlabel("Accept")
    axarr[1].set_ylabel("Average Cash per Deal")
    axarr[1].set_xlabel("Round Number")
    plt.colorbar(img,ax=axarr[0],label= "Prevalence vs. Uniform")
    plt.draw()
    #plt.savefig("imageresult/" +str(round)+ ".png")
 
if __name__=="__main__":
    main()