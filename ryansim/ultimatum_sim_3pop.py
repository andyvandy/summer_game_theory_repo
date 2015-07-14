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

from initial_matrix_generators import binomial_product_array


plt.rcParams['animation.ffmpeg_path'] = 'C:/Users/Andrew/bin/ffmpeg/bin/ffmpeg'
plt.rcParams['animation.convert_path'] = 'C:/Program Files/ImageMagick-6.9.1-Q16/convert'

GRANULARITY=1
DIMENSION=(100/GRANULARITY+1)
STARTING_PCT=1.0 /((100/GRANULARITY+1)**2)
rounds=2000
avg_deal_data1,avg_deal_data2,avg_deal_data3=[],[],[]
matplotlib.use('Agg')


starting_dist='cluster' # 'cluster' , 'rand', 'uniform'
do_pause=1
if starting_dist== 'rand':
    teams1=np.random.random( (DIMENSION,DIMENSION))
    teams1 = teams1/teams1.sum()   
    teams2=np.random.random( (DIMENSION,DIMENSION))
    teams2 = teams2/teams2.sum()  
    teams3=np.random.random( (DIMENSION,DIMENSION))
    teams3 = teams3/teams3.sum()   
    
elif starting_dist == 'cluster':
    teams1= binomial_product_array((DIMENSION,DIMENSION),(0.3,0.7))
    teams2= binomial_product_array((DIMENSION,DIMENSION),(0.7,0.3))
    teams3= binomial_product_array((DIMENSION,DIMENSION),(0.5,0.5))
    
elif starting_dist =='uniform':
    teams1=[STARTING_PCT]* DIMENSION**2
    teams1=np.reshape(original_teams1, (DIMENSION,DIMENSION))
    teams2=[STARTING_PCT]* DIMENSION**2
    teams2=np.reshape(teams2, (DIMENSION,DIMENSION))
    teams3=[STARTING_PCT]* DIMENSION**2
    teams3=np.reshape(teams3, (DIMENSION,DIMENSION))


data1, data2,data3= teams1,teams2,teams3
sns.set_style("dark")
fig = plt.figure(figsize=(16, 9))
grids = gridspec.GridSpec(2, 3 )
subplotspec1 = grids.new_subplotspec((0, 0), 1, 1)
subplotspec2 = grids.new_subplotspec((1, 0), 1,3)
subplotspec3 = grids.new_subplotspec((0, 1), 1, 1)
subplotspec4 = grids.new_subplotspec((0, 2), 1, 1)

axarr= [fig.add_subplot(subplotspec1),fig.add_subplot(subplotspec2),fig.add_subplot(subplotspec3),fig.add_subplot(subplotspec4)]
img1=axarr[0].imshow(data1, interpolation='nearest', cmap=plt.cm.ocean,
    extent=(0.5,np.shape(data1)[0]+0.5,0.5,np.shape(data1)[1]+0.5))

axarr[0].set_ylabel("Give")
axarr[0].set_xlabel("Accept")
axarr[0].set_title("Player1")
axarr[2].set_title("Player2")
axarr[2].set_title("Player3")
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


img3=axarr[3].imshow(data3, interpolation='nearest', cmap=plt.cm.ocean,
    extent=(0.5,np.shape(data3)[0]+0.5,0.5,np.shape(data3)[1]+0.5))
axarr[3].set_ylabel("Give")
axarr[3].set_xlabel("Accept")
axarr[1].plot(avg_deal_data3, color="yellow")

cbar3= plt.colorbar(img3,ax=axarr[3],label= "Prevalence vs. Uniform")


    
def main():
    
    
    '''for k in range(rounds):
        print "round:" ,k
        teams1,teams2=update(teams1,teams2,k)
        if k%15==0 and do_pause: plt.waitforbuttonpress()
        plot_update(fig ,axarr,teams1,teams2,k)'''
    
    anim=animation.FuncAnimation(fig, lambda x: update(fig,axarr,x),interval=1, frames=rounds, repeat=False)
    mywriter = animation.FFMpegWriter()
    anim.save('C:/Users/Andrew/Documents/programs/summer game theory/ultimatum_ani_test.mp4',fps=10)
    print "jesus"
    
def update(fig,axarr,k):
    global teams1, teams2, teams3
    global avg_deal_data1,avg_deal_data2,avg_deal_data3
    scores1,scores2,scores3=calc_scores( )
    avg_deal_data1.append(scores1.sum()/(DIMENSION**2))
    avg_deal_data2.append(scores2.sum()/(DIMENSION**2))
    avg_deal_data3.append(scores3.sum()/(DIMENSION**2))
    print 
    print "ROUND:" , k
    print "avg cash per deal from team1: ", avg_deal_data1[-1]
    print "avg cash per deal from team2: ", avg_deal_data2[-1]
    print "avg cash per deal from team3: ", avg_deal_data3[-1]
    '''max_locations1= np.where(scores1==scores1.max()) #todo: print and parse this
    max_locations2= np.where(scores2==scores2.max()) #todo: print and parse this
    max_locations3= np.where(scores2==scores2.max()) #todo: print and parse this'''
    total_sum=np.sum(scores1*teams1 +scores2*teams2+scores3*teams3)
    new_scores1=((scores1)/total_sum-(0.5/((100/GRANULARITY+1)**2)))+np.ones((DIMENSION,DIMENSION))
    new_scores2=((scores2)/total_sum-(0.5/((100/GRANULARITY+1)**2)))+np.ones((DIMENSION,DIMENSION))
    new_scores3=((scores3)/total_sum-(0.5/((100/GRANULARITY+1)**2)))+np.ones((DIMENSION,DIMENSION))

    teams1,teams2,teams3= teams1*new_scores1 ,teams2*new_scores2,teams3*new_scores3
    teams1,teams2,teams3= teams1/teams1.sum(),teams2/teams2.sum(),teams3/teams3.sum()
    
    center_of_mass1= ndimage.measurements.center_of_mass(teams1/STARTING_PCT)
    center_of_mass2= ndimage.measurements.center_of_mass(teams2/STARTING_PCT)
    center_of_mass3= ndimage.measurements.center_of_mass(teams3/STARTING_PCT)
    
    # -----graphics-----
    img1.set_array(teams1/STARTING_PCT)
    img2.set_array(teams2/STARTING_PCT)
    img3.set_array(teams3/STARTING_PCT)
    cbar1.set_clim(vmin=0,vmax=np.max(teams1/STARTING_PCT)) 
    cbar1.draw_all() 
    cbar2.set_clim(vmin=0,vmax=np.max(teams2/STARTING_PCT)) 
    cbar2.draw_all() 
    cbar3.set_clim(vmin=0,vmax=np.max(teams3/STARTING_PCT)) 
    cbar3.draw_all() 
    axarr[1].set_title("Current Round:" +str(k))
    axarr[1].plot(avg_deal_data1, color="red")
    axarr[1].plot(avg_deal_data2, color="purple")
    axarr[1].plot(avg_deal_data3, color="yellow")
    
    axarr[0].plot([center_of_mass1[1]],[100-center_of_mass1[0]],'or') #adds dot at center of mass
    axarr[0].plot([center_of_mass2[1]],[100-center_of_mass2[0]],'om') 
    axarr[0].plot([center_of_mass3[1]],[100-center_of_mass3[0]],'oy') 
    
    axarr[2].plot([center_of_mass1[1]],[100-center_of_mass1[0]],'or') #adds dot at center of mass
    axarr[2].plot([center_of_mass2[1]],[100-center_of_mass2[0]],'om') 
    axarr[2].plot([center_of_mass3[1]],[100-center_of_mass3[0]],'oy') 
    
    axarr[3].plot([center_of_mass1[1]],[100-center_of_mass1[0]],'or') #adds dot at center of mass
    axarr[3].plot([center_of_mass2[1]],[100-center_of_mass2[0]],'om') 
    axarr[3].plot([center_of_mass3[1]],[100-center_of_mass3[0]],'oy') 
    
    
    
    axarr[0].axis((1,101,1,101))
    axarr[2].axis((1,101,1,101))
    axarr[3].axis((1,101,1,101))
    
    
def calc_scores( ):
    #takes in a tuple representing the team and also the population breakdown
    #returns the teams fitness
    scores1,scores2,scores3=np.zeros((DIMENSION,DIMENSION)),np.zeros((DIMENSION,DIMENSION)),np.zeros((DIMENSION,DIMENSION))
    interim=np.array( [[100-i*GRANULARITY for i in range(DIMENSION)]]*DIMENSION )
    teams_mod1=teams1*interim
    teams_mod2=teams2*interim
    teams_mod3=teams2*interim
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            points_deal_from_p1 = teams_mod1[j:DIMENSION,:].sum()   
            points_deal_to_p1 = (100-i*GRANULARITY) * teams1[:,(DIMENSION-i):DIMENSION].sum()
            points_deal_from_p2 = teams_mod2[j:DIMENSION,:].sum()   
            points_deal_to_p2 = (100-i*GRANULARITY) * teams2[:,(DIMENSION-i):DIMENSION].sum()
            points_deal_from_p3 = teams_mod3[j:DIMENSION,:].sum()   
            points_deal_to_p3 = (100-i*GRANULARITY) * teams3[:,(DIMENSION-i):DIMENSION].sum()
            
            scores1[i][j] = 0.25* ( points_deal_from_p2 +  points_deal_to_p2 + points_deal_from_p3 +  points_deal_to_p3 )
            scores2[i][j] = 0.25* ( points_deal_from_p1 +  points_deal_to_p1 + points_deal_from_p3 +  points_deal_to_p3 )
            scores3[i][j] = 0.25* ( points_deal_from_p1 +  points_deal_to_p1 + points_deal_from_p2 +  points_deal_to_p2 )
    return scores1,scores2,scores3
    


if __name__=="__main__":
    main()