import numpy as np
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os
import subprocess
from scipy import ndimage


def initialize_figure(avg_deal_data, data, **params):
    """Initializes the figures.

    Args:
      avg_deal_data:
      data:

    Returns:
        fig:
        axarr:
    """
    
    rounds = params['ROUNDS']

    # Set plot style to dark
    sns.set_style("dark")

    img = []
    cbar = []

    # INITIALIZE PLOTS

    # Create figure. Size is defined here.
    fig = plt.figure(figsize = (16, 9))

    # Create grid. I think this works as (rows, columns).
    grids = gridspec.GridSpec(2, 4)
    # Set up grid.
    subplotspec_centers = grids.new_subplotspec((0, 3), 1, 1)
    subplotspec_species = grids.new_subplotspec((1, 2), 1, 2)
    subplotspec_line = grids.new_subplotspec((1, 0), 1, 2)
    subplotspec1 = grids.new_subplotspec((0, 0), 1, 1)
    subplotspec2 = grids.new_subplotspec((0, 1), 1, 1)
    subplotspec3 = grids.new_subplotspec((0, 2), 1, 1)

    axarr = [fig.add_subplot(subplotspec1),
             fig.add_subplot(subplotspec_line), 
             fig.add_subplot(subplotspec2), 
             fig.add_subplot(subplotspec3),
             fig.add_subplot(subplotspec_centers),
             fig.add_subplot(subplotspec_species)]

    # Team A
    img.append(axarr[0].imshow(data[0], interpolation='nearest', 
                               cmap = plt.cm.ocean, 
                               extent = (0.5,  np.shape(data[0])[0] + 0.5, 0.5, 
                                         np.shape(data[0])[1] + 0.5)))

    axarr[0].set_ylabel("Give")
    axarr[0].set_xlabel("Accept")
    axarr[0].set_title("A")
    axarr[1].set_title("B")
    axarr[2].set_title("C")
    axarr[1].plot(avg_deal_data[0], color = "red")
    axarr[1].set_xlim(0, rounds)
    axarr[1].set_ylim(0, 100)
    axarr[1].set_ylabel("Average Cash per Deal")
    axarr[1].set_xlabel("Round Number")
    axarr[5].set_xlim(0, rounds)
    axarr[5].set_ylim(0, 1)

    cbar.append(plt.colorbar(img[0], ax = axarr[0], 
                label = "Prevalence vs. Uniform"))

    # Team B

    img.append(axarr[2].imshow(data[1], interpolation = 'nearest', 
                               cmap = plt.cm.ocean,
                               extent = (0.5, np.shape(data[1])[0] + 0.5, 0.5, 
                                         np.shape(data[1])[1] + 0.5)))

    axarr[2].set_ylabel("Give")
    axarr[2].set_xlabel("Accept")
    axarr[1].plot(avg_deal_data[1], color = "purple")

    cbar.append(plt.colorbar(img[1], ax = axarr[2], 
                label = "Prevalence vs. Uniform"))

    # Team C

    img.append(axarr[3].imshow(data[2], interpolation = 'nearest', 
                               cmap = plt.cm.ocean,
                               extent = (0.5, np.shape(data[2])[0] + 0.5, 0.5, 
                                         np.shape(data[2])[1] + 0.5)))

    axarr[3].set_ylabel("Give")
    axarr[3].set_xlabel("Accept")
    axarr[1].plot(avg_deal_data[2], color = "yellow")

    cbar.append(plt.colorbar(img[2], ax = axarr[3], 
                label = "Prevalence vs. Uniform"))

    axarr[4].axis([0, 100, 0 , 100])

    return (fig, axarr, img, cbar)
    

def update_figures(fig, axarr, img, cbar, teams, avg_deal_data, 
                   species_breakdown_history, center_of_mass, k, **params):
    
    dimension = params['DIMENSION']
    granularity = params['GRANULARITY']
    starting_pct = params['STARTING_PCT']
    
    # -----graphics-----
    img[0].set_array(teams[0] / starting_pct)
    img[1].set_array(teams[1] / starting_pct)
    img[2].set_array(teams[2] / starting_pct)

    cbar[0].set_clim(vmin = 0, vmax = np.max(teams[0] / starting_pct)) 
    cbar[0].draw_all() 
    cbar[1].set_clim(vmin = 0, vmax = np.max(teams[1] / starting_pct)) 
    cbar[1].draw_all() 
    cbar[2].set_clim(vmin = 0, vmax = np.max(teams[2] / starting_pct)) 
    cbar[2].draw_all() 

    axarr[1].set_title("Average Scores")
    axarr[1].plot(avg_deal_data[0], color="red")
    axarr[1].plot(avg_deal_data[1], color="purple")
    axarr[1].plot(avg_deal_data[2], color="yellow")

    axarr[5].set_title("Relative Population Size")
    axarr[5].plot(species_breakdown_history[0], color="red")
    axarr[5].plot(species_breakdown_history[1], color="purple")
    axarr[5].plot(species_breakdown_history[2], color="yellow")
    
    axarr[4].plot([center_of_mass[0][1]], [100 - center_of_mass[0][0]],'or') #adds dot at center of mass
    axarr[4].plot([center_of_mass[1][1]], [100 - center_of_mass[1][0]],'om') 
    axarr[4].plot([center_of_mass[2][1]], [100 - center_of_mass[2][0]],'oy') 
    
    axarr[0].axis((1,101,1,101))
    axarr[2].axis((1,101,1,101))
    axarr[3].axis((1,101,1,101))
    axarr[4].axis((1,101,1,101))


def create_video_from_frames(name, fps=10):
    """This is extremely hacked together.
    """

    tmp_directory = os.path.join("output", "tmp")
    output_directory = os.path.join("output", "videos")

    command = "avconv -f image2 -r %s -i " % str(fps)
    command += "%s.png" % (os.path.join(tmp_directory, name + "%04d"))
    command += " -c:v libx264 -r 30 %s.mp4" % (os.path.join(output_directory, name))
    print "Running command:"
    print command
    p = subprocess.Popen(command, shell=True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate()[0]
    print "output\n"+"*"*10+"\n"
    print output
    print "*"*10
    print "Video file has been written"