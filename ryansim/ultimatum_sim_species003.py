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
SP_BD=[1.0/3]*3 #SPECIES BREAKDOWN
SP_BD_HIST1=[]
SP_BD_HIST2=[]
SP_BD_HIST3=[]
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
grids = gridspec.GridSpec(2, 4 )
subplotspec_centers = grids.new_subplotspec((0, 3), 1,1)
subplotspec_species = grids.new_subplotspec((1, 3), 1,1)
subplotspec_line = grids.new_subplotspec((1, 0), 1,3)
subplotspec1 = grids.new_subplotspec((0, 0), 1, 1)
subplotspec2 = grids.new_subplotspec((0, 1), 1, 1)
subplotspec3 = grids.new_subplotspec((0, 2), 1, 1)

axarr= [fig.add_subplot(subplotspec1),fig.add_subplot(subplotspec_line),fig.add_subplot(subplotspec2),fig.add_subplot(subplotspec3),fig.add_subplot(subplotspec_centers),fig.add_subplot(subplotspec_species)]
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

axarr[4].axis([0,100,0,100])


    
def main():
    
    
    '''for k in range(rounds):
        print "round:" ,k
        teams1,teams2=update(teams1,teams2,k)
        if k%15==0 and do_pause: plt.waitforbuttonpress()
        plot_update(fig ,axarr,teams1,teams2,k)'''
    
    anim=animation.FuncAnimation(fig, lambda x: update(fig,axarr,x),interval=1, frames=rounds, repeat=False)
    mywriter = animation.FFMpegWriter()
    anim.save('C:/Users/Andrew/Documents/programs/summer game theory/ultimatum_ani_spec.mp4',fps=10)
    print "jesus"
    
def update(fig,axarr,k):
    global teams1, teams2, teams3
    global avg_deal_data1,avg_deal_data2,avg_deal_data3
    global SP_BD, SP_BD_HIST1,SP_BD_HIST2,SP_BD_HIST3
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
    
    SP_BD_HIST1.append(SP_BD[0])
    SP_BD_HIST2.append(SP_BD[1])
    SP_BD_HIST3.append(SP_BD[2])
    
    scores_sums=[scores1.sum(),scores2.sum(),scores3.sum()]
    scores_sum=sum(scores_sums)
    species_multipliers= scores_sums[0]/scores_sum+2.0/3,scores_sums[1]/scores_sum+2.0/3,scores_sums[2]/scores_sum+2.0/3
    SP_BD_temp= SP_BD[0]*species_multipliers[0],SP_BD[1]*species_multipliers[1],SP_BD[2]*species_multipliers[2]
    SP_BD_sum=sum(SP_BD_temp)
    SP_BD=SP_BD_temp[0]/SP_BD_sum,SP_BD_temp[1]/SP_BD_sum,SP_BD_temp[2]/SP_BD_sum
    
    total_sum=np.sum(scores1*teams1 +scores2*teams2+scores3*teams3)
    new_scores1=((scores1)/total_sum-(0.33/(DIMENSION**2)))+1
    new_scores2=((scores2)/total_sum-(0.33/(DIMENSION**2)))+1
    new_scores3=((scores3)/total_sum-(0.33/(DIMENSION**2)))+1
    
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
    
    
    axarr[5].set_title("Species distribution")
    axarr[5].plot(SP_BD_HIST1, color="red")
    axarr[5].plot(SP_BD_HIST2, color="purple")
    axarr[5].plot(SP_BD_HIST3, color="yellow")
    
    
    axarr[4].plot([center_of_mass1[1]],[100-center_of_mass1[0]],'or') #adds dot at center of mass
    axarr[4].plot([center_of_mass2[1]],[100-center_of_mass2[0]],'om') 
    axarr[4].plot([center_of_mass3[1]],[100-center_of_mass3[0]],'oy') 


    axarr[0].axis((1,101,1,101))
    axarr[2].axis((1,101,1,101))
    axarr[3].axis((1,101,1,101))
    axarr[4].axis((1,101,1,101))
    
    
def calc_scores( ):
    #takes in a tuple representing the team and also the population breakdown
    #returns the teams fitness
    scores1,scores2,scores3=np.zeros((DIMENSION,DIMENSION)),np.zeros((DIMENSION,DIMENSION)),np.zeros((DIMENSION,DIMENSION))
    interim=np.array( [[100-i*GRANULARITY for i in range(DIMENSION)]]*DIMENSION )
    teams_mod1=teams1*interim
    teams_mod2=teams2*interim
    teams_mod3=teams2*interim
    j_sums1= [teams_mod1[j:DIMENSION,:].sum() for j in range(DIMENSION) ]
    j_sums2= [teams_mod2[j:DIMENSION,:].sum() for j in range(DIMENSION) ]
    j_sums3= [teams_mod3[j:DIMENSION,:].sum() for j in range(DIMENSION) ]
    
    i_sums1 = [(100-i*GRANULARITY) * teams1[:,(DIMENSION-i):DIMENSION].sum() for i in range(DIMENSION)]
    i_sums2 = [(100-i*GRANULARITY) * teams2[:,(DIMENSION-i):DIMENSION].sum() for i in range(DIMENSION)]
    i_sums3 = [(100-i*GRANULARITY) * teams3[:,(DIMENSION-i):DIMENSION].sum() for i in range(DIMENSION)]
    
    i_ii=SP_BD[0]/(SP_BD[0]+SP_BD[1])
    i_iii=SP_BD[0]/(SP_BD[0]+SP_BD[2])
    ii_i=SP_BD[1]/(SP_BD[1]+SP_BD[0])
    ii_iii=SP_BD[1]/(SP_BD[1]+SP_BD[2])
    iii_i=SP_BD[2]/(SP_BD[2]+SP_BD[0])
    iii_ii=SP_BD[2]/(SP_BD[2]+SP_BD[1])
    
    j_mat1=np.matrix([[teams_mod1[j:DIMENSION,:].sum() ]*DIMENSION for j in range(DIMENSION) ])
    i_mat1=np.matrix([[(100-i*GRANULARITY) * teams1[:,(DIMENSION-i):DIMENSION].sum() for i in range(DIMENSION)]]*DIMENSION)
    j_mat2=np.matrix([[teams_mod2[j:DIMENSION,:].sum() ]*DIMENSION for j in range(DIMENSION) ])
    i_mat2=np.matrix([[(100-i*GRANULARITY) * teams2[:,(DIMENSION-i):DIMENSION].sum() for i in range(DIMENSION)]]*DIMENSION)
    j_mat3=np.matrix([[teams_mod3[j:DIMENSION,:].sum() ]*DIMENSION for j in range(DIMENSION) ])
    i_mat3 =np.matrix( [[(100-i*GRANULARITY) * teams3[:,(DIMENSION-i):DIMENSION].sum() for i in range(DIMENSION)]]*DIMENSION)
    
    scores1=np.array( 0.5*(ii_iii*(j_mat2+ i_mat2) +iii_ii*(j_mat2+ i_mat2)) )
    scores2=np.array( 0.5*(i_iii*(j_mat1+ i_mat1) +iii_i*(j_mat3+ i_mat3)) )
    scores3= np.array(0.5*(i_ii*(j_mat1+ i_mat1) +ii_i*(j_mat2+ i_mat2)) )
    
    
    '''for i in range(DIMENSION):
        for j in range(DIMENSION):
            points_deal_from_p1 = j_sums1[j] 
            points_deal_to_p1 =  i_sums1[i]
            points_deal_from_p2 =j_sums2[j]   
            points_deal_to_p2 = i_sums2[i]
            points_deal_from_p3 = j_sums3[j]   
            points_deal_to_p3 = i_sums3[i]
            
            scores1[i][j] = 0.5* ( ii_iii*(points_deal_from_p2 +  points_deal_to_p2) + iii_ii*(points_deal_from_p3 +  points_deal_to_p3) )
            scores2[i][j] = 0.5* ( i_iii*(points_deal_from_p1 +  points_deal_to_p1) + iii_i*(points_deal_from_p3 +  points_deal_to_p3 ))
            scores3[i][j] = 0.5* ( i_ii*(points_deal_from_p1 +  points_deal_to_p1) + ii_i*(points_deal_from_p2 +  points_deal_to_p2) )'''
    return scores1,scores2,scores3
    


if __name__=="__main__":
    main()