from log_utils import ensure_directory

import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import json
import os

import sys

def grapher(SIM_NAME):
    
    data_path= os.path.join("output", SIM_NAME, "logs")
    plots_path= os.path.join("output", SIM_NAME, "logs")

    #ensure_directory(data_path) # make sure the directories exist
    #ensure_directory(plots_path) 
    # omg the above functions were emptying the directories...

    # plot 1 - avg score
    avg_turn_score_df=pd.io.json.read_json(os.path.join(data_path, "avg_score.json"))
    generations,simulations=avg_turn_score_df.shape
    
    avg_turn_score_df=avg_turn_score_df.sort() 
    sns.set(style = "darkgrid", palette = "muted",rc={"lines.linewidth":1})
    fig = plt.subplots(1, 1, figsize = (16, 12))
    b, g, r, p = sns.color_palette("muted", 4)
    plt.plot(range(generations), avg_turn_score_df, color='black', alpha=1)
    plt.xlabel('Generation')
    plt.ylabel('Average score per turn')
    plt.title('Distribution of Average Scores per Turn')
    plt.savefig(plots_path+"avg_turn_score.png") 
    
    plt.clf()
    plt.cla()
    
    #plot 2 -avg gifts
    
    avg_gift_a_df=pd.io.json.read_json(os.path.join(data_path, "avg_gift_a.json"))
    avg_gift_b_df=pd.io.json.read_json(os.path.join(data_path, "avg_gift_b.json"))

    generations,simulations=avg_turn_score_df.shape
    
    avg_gift_a_df=avg_gift_a_df.sort() 
    avg_gift_b_df=avg_gift_b_df.sort() 

    sns.set(style = "darkgrid", palette = "muted",rc={"lines.linewidth":1})
    fig = plt.subplots(1, 1, figsize = (16, 12))
    b, g, r, p = sns.color_palette("muted", 4)
    gift_a, = plt.plot(range(generations), avg_gift_a_df, color=p, alpha=1)
    gift_b, = plt.plot(range(generations), avg_gift_b_df, color=g, alpha=1)

    plt.xlabel('Generation')
    plt.ylabel('Average gift per turn by Player Role')
    plt.legend([gift_a, gift_b], ["Investors", "Trustees"])
    plt.title('Distribution of Average gifts per Turn')
    plt.savefig(plots_path+"avg_respective_gift.png") 
    
    plt.clf()
    plt.cla()
    
    
    #plot 3- respective avg scores

    avg_score_a_df=pd.io.json.read_json(os.path.join(data_path, "avg_score_a.json"))
    avg_score_b_df=pd.io.json.read_json(os.path.join(data_path, "avg_score_b.json"))

    generations,simulations=avg_turn_score_df.shape
    
    avg_score_a_df=avg_score_a_df.sort()
    avg_score_b_df=avg_score_b_df.sort() 

    sns.set(style = "darkgrid", palette = "muted",rc={"lines.linewidth":1})
    fig = plt.subplots(1, 1, figsize = (16, 12))
    b, g, r, p = sns.color_palette("muted", 4)
    a_score, = plt.plot(range(generations), avg_score_a_df, color=p, alpha=1)
    b_score, = plt.plot(range(generations), avg_score_b_df, color=g, alpha=1)

    plt.xlabel('Generation')
    plt.ylabel('Average score per turn by Player Role')
    plt.legend([a_score, b_score], ["Investors", "Trustees"])
    plt.title('Distribution of Average Scores per Turn')
    plt.savefig(plots_path+"avg_respective_score.png") 
    
    plt.clf()
    plt.cla()
   
    

if __name__=="__main__":
    SIM_NAME=sys.argv[1]
    grapher(SIM_NAME)