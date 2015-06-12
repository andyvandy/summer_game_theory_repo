from log_utils import ensure_directory

import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import json  

import sys

def grapher(SIM_NAME):
    
    data_path= os.path.join("output", SIM_NAME, "logs")
    plots_path= os.path.join("output", SIM_NAME, "logs")

    ensure_directory(data_path) # make sure the directories exist
    ensure_directory(plots_path)

    # plot 1
    avg_turn_score_df=pd.io.json.read_json(path+"avg_score.json")
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
    

if __name__=="__main__":
    SIM_NAME=sys.argv[1]
    grapher(SIM_NAME)