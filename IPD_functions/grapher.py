import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json  

# this file is still far from done , lol sry stuuuuu


def main():
    path = "C:/Users/Andrew/Documents/programs/summer game theory/data/test/"
    
    
    avg_turn_score_df=pd.io.json.read_json(path+"avgscore.json")
    
    generations,simulations=avg_turn_score_df.shape
    
    avg_turn_score_df=avg_turn_score_df.sort() # jesus this object is whiny
    print avg_turn_score_df
    sns.set(style = "darkgrid", palette = "muted",rc={"lines.linewidth":0.1})
    fig = plt.subplots(1, 1, figsize = (4, 2.5))
    b, g, r, p = sns.color_palette("muted", 4)
    #ax = sns.tsplot(result, color=g)
    cis = np.linspace(90, 10, 4) #acts like range does
    #ax = sns.tsplot(stats[0] ,err_style="boot_traces", n_boot=simulations)
    #balls=[avg_turn_score_df[22][i] for i in range(generations)]
    for i in range(simulations):
        plt.plot(range(generations), avg_turn_score_df[i], color='black', alpha=0.8)
    plt.savefig("overall_avg_turn_score.png") 
    
    #plt.show()
    
    
    plt.clf()
    plt.cla()
    
    avg_coop_pct_df=pd.io.json.read_json(path+"avgcoop.json")
    avg_defect_pct_df=pd.io.json.read_json(path+"avgdefect.json")
    
    avg_coop_pct_df=avg_coop_pct_df.sort() # tres important!
    avg_defect_pct_df=avg_defect_pct_df.sort() # do not forget!
    
    sns.set(style="darkgrid", palette="muted",rc={"lines.linewidth":0.1})
    fig = plt.subplots(1, 1, figsize=(4, 3))
    b, g, r, p = sns.color_palette("muted", 4)
    for i in range(simulations):
        #plt.plot(range(generations), avg_coop_pct_df[i], color='blue', alpha=0.8)
        plt.plot(range(generations), avg_defect_pct_df[i], color='red', alpha=0.8)
        
    plt.savefig("overall_cooppct.png") 
    
    
def asdsad():
    sns.set(style = "darkgrid", palette = "muted")
    fig = plt.subplots(1, 1, figsize = (4, 2.5))
    b, g, r, p = sns.color_palette("muted", 4)
    #ax = sns.tsplot(result, color=g)
    cis = np.linspace(90, 10, 4) #acts like range does
    #ax = sns.tsplot(stats[0] ,err_style="boot_traces", n_boot=simulations)
    for i in range(simulations):
        plt.plot(range(generations), stats[0][i], color='black', alpha=1/float(simulations))
    #ax.set(ylabel = "Average score per turn")
    #ax.set_xlabel("Generation")
    plt.show()

if __name__=="__main__":
    main()