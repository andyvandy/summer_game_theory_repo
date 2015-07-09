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
from scipy import ndimage #for center of mass calculation


plt.rcParams['animation.ffmpeg_path'] = 'C:/Users/Andrew/bin/ffmpeg/bin/ffmpeg'
plt.rcParams['animation.convert_path'] = 'C:/Program Files/ImageMagick-6.9.1-Q16/convert'

GRANULARITY=1
DIMENSION=(100/GRANULARITY+1)
STARTING_PCT=1.0 /((100/GRANULARITY+1)**2)
rounds=500
avg_deal_data1=[]
avg_deal_data2=[]
matplotlib.use('Agg')


random_start=1
do_pause=1
if random_start:
    teams1=np.random.random( (DIMENSION,DIMENSION))
    teams1 = eams1/teams1.sum()   
    teams2=np.random.random( (DIMENSION,DIMENSION))
    teams2 = teams2/teams2.sum()   
else:
    oteams1=[STARTING_PCT]* DIMENSION**2
    teams1=np.reshape(original_teams1, (DIMENSION,DIMENSION))
    teams2=[STARTING_PCT]* DIMENSION**2
    teams2=np.reshape(teams2, (DIMENSION,DIMENSION))


data1=teams1
data2=teams2    
sns.set_style("dark")
fig = plt.figure(figsize=(16, 9))
grids = gridspec.GridSpec(2, 2 )
subplotspec1 = grids.new_subplotspec((0, 0), 1, 1)
subplotspec2 = grids.new_subplotspec((1, 0), 1,2)
subplotspec3 = grids.new_subplotspec((0, 1), 1, 1)

axarr= [fig.add_subplot(subplotspec1),fig.add_subplot(subplotspec2),fig.add_subplot(subplotspec3)]
img1=axarr[0].imshow(data1, interpolation='nearest', cmap=plt.cm.ocean,
    extent=(0.5,np.shape(data1)[0]+0.5,0.5,np.shape(data1)[1]+0.5))
plt.title("Current Round:" +str(0))
axarr[0].set_ylabel("Give")
axarr[0].set_xlabel("Accept")
axarr[0].set_title("Player1")
axarr[2].set_title("Player2")
axarr[1].plot(avg_deal_data1, color="red")
axarr[1].set_xlim(0,rounds)
axarr[1].set_ylabel("Average Cash per Deal")
axarr[1].set_xlabel("Round Number")
cbar1= plt.colorbar(img1,ax=axarr[0],label= "Prevalence vs. Uniform")

img2=axarr[2].imshow(data2, interpolation='nearest', cmap=plt.cm.ocean,
    extent=(0.5,np.shape(data2)[0]+0.5,0.5,np.shape(data2)[1]+0.5))
axarr[2].set_ylabel("Give")
axarr[2].set_xlabel("Accept")
axarr[1].plot(avg_deal_data2, color="purple")

cbar2= plt.colorbar(img2,ax=axarr[2],label= "Prevalence vs. Uniform")


    
def main():
    
    
    '''for k in range(rounds):
        print "round:" ,k
        teams1,teams2=update(teams1,teams2,k)
        if k%15==0 and do_pause: plt.waitforbuttonpress()
        plot_update(fig ,axarr,teams1,teams2,k)'''
    
    anim=animation.FuncAnimation(fig, lambda x: update(fig,axarr,x),interval=1, frames=rounds, repeat=False)
    mywriter = animation.FFMpegWriter()
    anim.save('C:/Users/Andrew/Documents/programs/summer game theory/ultimatum_ani.gif',writer="imagemagick",fps=10)
    print "jesus"
    
def update(fig,axarr,k):
    global teams1, teams2
    global avg_deal_data1,avg_deal_data2
    scores1,scores2=calc_scores( )
    avg_deal_data1.append(scores1.sum()/(DIMENSION**2))
    avg_deal_data2.append(scores2.sum()/(DIMENSION**2))
    print 
    print "ROUND:" , k
    print "avg cash per deal from team1: ", avg_deal_data1[-1]
    print "avg cash per deal from team2: ", avg_deal_data2[-1]
    max_locations1= np.where(scores1==scores1.max()) #todo: print and parse this
    max_locations2= np.where(scores2==scores2.max()) #todo: print and parse this
    total_sum=np.sum(scores1*teams1 +scores2*teams2)
    new_scores1=((scores1)/total_sum-(0.5/((100/GRANULARITY+1)**2)))+np.ones((DIMENSION,DIMENSION))
    new_scores2=((scores2)/total_sum-(0.5/((100/GRANULARITY+1)**2)))+np.ones((DIMENSION,DIMENSION))
    teams1,teams2= teams1*new_scores1 ,teams2*new_scores2
    teams1,teams2= teams1/teams1.sum(),teams2/teams2.sum()
    center_of_mass1= ndimage.measurements.center_of_mass(teams1/STARTING_PCT)
    center_of_mass2= ndimage.measurements.center_of_mass(teams2/STARTING_PCT)
    
    
    # -----graphics-----
    img1.set_array(teams1/STARTING_PCT)
    img2.set_array(teams2/STARTING_PCT)
    cbar1.set_clim(vmin=0,vmax=np.max(teams1/STARTING_PCT)) 
    cbar1.draw_all() 
    cbar2.set_clim(vmin=0,vmax=np.max(teams2/STARTING_PCT)) 
    cbar2.draw_all() 
    #cbar2.on_mappable_changed(img2)
    axarr[1].set_title("Current Round:" +str(k))
    axarr[1].plot(avg_deal_data1, color="red")
    axarr[1].plot(avg_deal_data2, color="purple")
    
    
    axarr[0].plot([center_of_mass1[1]],[center_of_mass1[0]],'or') #adds dot at center of mass
    axarr[0].plot([center_of_mass2[1]],[center_of_mass2[0]],'op') 
    
    axarr[2].plot([center_of_mass1[1]],[center_of_mass1[0]],'or') #adds dot at center of mass
    axarr[2].plot([center_of_mass2[1]],[center_of_mass2[0]],'op') 
    
    
    axarr[0].axis((1,101,1,101))
    axarr[2].axis((1,101,1,101))


        
    
def calc_scores( ):
    #takes in a tuple representing the team and also the population breakdown
    #returns the teams fitness
    scores1,scores2=np.zeros((DIMENSION,DIMENSION)),np.zeros((DIMENSION,DIMENSION))
    interim=np.array( [[100-i*GRANULARITY for i in range(DIMENSION)]]*DIMENSION )
    teams_mod1=teams1*interim
    teams_mod2=teams2*interim
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            scores1[i][j] =scores1[i][j]+ 0.5* (100-i*GRANULARITY) * teams2[:,(DIMENSION-i):DIMENSION].sum()      #points from being a dealmaker
            scores1[i][j] =scores1[i][j] + 0.5 * teams_mod2[j:DIMENSION,:].sum()        #points from being a dealtaker
            scores2[i][j] =scores2[i][j]+ 0.5* (100-i*GRANULARITY) * teams1[:,(DIMENSION-i):DIMENSION].sum()      #points from being a dealmaker
            scores2[i][j] =scores2[i][j] + 0.5 * teams_mod1[j:DIMENSION,:].sum()        #points from being a dealtaker
    return scores1,scores2
    


if __name__=="__main__":
    main()