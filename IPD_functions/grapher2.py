import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json  

# this file is still far from done , lol sry stuuuuu


def main():
    path = "C:/Users/Andrew/Documents/GitHub/summer_game_theory_repo/"
    path2= "C:/Users/Andrew/Documents/GitHub/summer_game_theory_repo/IPD_output/images/"
    

    avg_turn_score_df=pd.io.json.read_json(path+"avgscore.json")
    
    generations,simulations=avg_turn_score_df.shape
    
    avg_turn_score_df=avg_turn_score_df.sort() # jesus this object is whiny
    print avg_turn_score_df
    sns.set(style = "darkgrid", palette = "muted",rc={"lines.linewidth":0.1})
    fig = plt.subplots(1, 1, figsize = (16, 12))
    b, g, r, p = sns.color_palette("muted", 4)
    stuff_t= np.transpose(np.array(avg_turn_score_df))
    #ax = sns.tsplot(result, color=g)
    cis = np.linspace(98, 10, 4) #acts like range does
    #ax = sns.tsplot(stats[0] ,err_style="boot_traces", n_boot=simulations)
    #balls=[avg_turn_score_df[22][i] for i in range(generations)]
    ax=sns.tsplot( stuff_t ,err_style="ci_band",ci = cis, color=p)
    ax.set_autoscale_on(False)
    ax.axis([0,generations,0,3]) #[xmin,xmax,ymin,ymax]
    '''for i in range(simulations):
        plt.plot(range(generations), avg_turn_score_df[i], color='black', alpha=0.4)'''
    plt.xlabel('Generation')
    plt.ylabel('Average score per turn')
    plt.title('Distribution of Average Scores per Turn')
    plt.savefig(path2+"overall_avg_turn_score.png") 
    
    #plt.show()
    
    
    plt.clf()
    plt.cla()
    
    avg_coop_pct_df=pd.io.json.read_json(path+"avgcoop.json")
    avg_defect_pct_df=pd.io.json.read_json(path+"avgdefect.json")
    
    avg_coop_pct_df=avg_coop_pct_df.sort() # tres important!
    avg_defect_pct_df=avg_defect_pct_df.sort() # do not forget!
    
    stuff_c=np.transpose(np.array(avg_coop_pct_df))
    stuff_d=np.transpose(np.array(avg_defect_pct_df))
    
    sns.set(style="darkgrid", palette="muted",rc={"lines.linewidth":0.5})
    fig = plt.subplots(1, 1, figsize=(16, 12))
    b, g, r, p = sns.color_palette("muted", 4)

    sns.tsplot( stuff_c ,err_style="ci_band",ci = cis, color=b)
    sns.tsplot( stuff_d ,err_style="ci_band",ci = cis, color=r)
    '''for i in range(simulations):
    
        plt.plot(range(generations), avg_coop_pct_df[i], color='blue', alpha=0.01)
        plt.plot(range(generations), avg_defect_pct_df[i], color='red', alpha=0.01)'''
    plt.xlabel('Generation')
    plt.ylabel('Percent')
    plt.title('Percentage of cooperation vs defection')
    
    plt.savefig(path2+"overall_cooppct.png") 
    
    
def asdsad():
    sns.set(style = "darkgrid", palette = "muted")
    fig = plt.subplots(1, 1, figsize = (16, 12))
    b, g, r, p = sns.color_palette("muted", 4)
    #ax = sns.tsplot(result, color=g)
    cis = np.linspace(90, 10, 4) #acts like range does
    ax = sns.tsplot(stats[0] ,err_style="boot_traces", n_boot=simulations)
    for i in range(simulations):
        plt.plot(range(generations), stats[0][i], color='black', alpha=1/float(simulations))
    #ax.set(ylabel = "Average score per turn")
    #ax.set_xlabel("Generation")
    plt.show()

if __name__=="__main__":
    main()