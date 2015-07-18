import numpy as np
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os
import subprocess
from scipy import ndimage


def initialize_figure(game, **params):
    """Initializes the figures.

    Args:
      game: the game object
      params:


    Returns:
        axarr:
        img:
        cbar:
    """
    
    # Unpack parameters
    rounds = params['ROUNDS']
    number_of_teams = params['NUMBER_OF_TEAMS']

    # Set plot style to dark
    sns.set_style("dark")

    # Initialize img, cbar, axarr lists
    img = []
    cbar = []
    axarr = []

    # Create figure. Size is defined here.
    fig = plt.figure(figsize = (16, 9))

    # Create grid.
    if number_of_teams > 1 and number_of_teams <= 3:
        grids = gridspec.GridSpec(2, 4)
    elif number_of_teams > 3 and number_of_teams <= 7:
        grids = gridspec.GridSpec(3, 4)
    else:
        print "Too many teams, or invalid TEAM_SPEC. Check your parameters."
        sys.exit()

    # Set up grid.
    if number_of_teams > 1 and number_of_teams <= 3:
        subplotspec_centers = grids.new_subplotspec((0, 3), 1, 1)
        subplotspec_species = grids.new_subplotspec((1, 2), 1, 2)
        subplotspec_deals = grids.new_subplotspec((1, 0), 1, 2)

    elif number_of_teams > 3 and number_of_teams <= 7:
        subplotspec_centers = grids.new_subplotspec((1, 3), 1, 1)
        subplotspec_species = grids.new_subplotspec((2, 2), 1, 2)
        subplotspec_deals = grids.new_subplotspec((2, 0), 1, 2)

    # Add stats subplots
    axarr.append(fig.add_subplot(subplotspec_centers))
    axarr.append(fig.add_subplot(subplotspec_species))
    axarr.append(fig.add_subplot(subplotspec_deals))

    # Make the first two distribution subplots. These will be the same no matter
    # what number of teams there are.

    subplotspec_dists = [grids.new_subplotspec((0, 0), 1, 1), 
                         grids.new_subplotspec((0, 1), 1, 1)]

    # Make the other distribution subplots
    if number_of_teams >= 3:
        subplotspec_dists.append(grids.new_subplotspec((0, 2), 1, 1))

    if number_of_teams >= 4:
        subplotspec_dists.append(grids.new_subplotspec((0, 3), 1, 1))

    if number_of_teams >= 5:
        for i in range(number_of_teams - 4):
            subplotspec_dists.append(grids.new_subplotspec((1, i), 1, 1))

    for subplot in subplotspec_dists:
        axarr.append(fig.add_subplot(subplot))

    """ THIS CAN BE REMOVED. KEEPING FOR REFERENCE TEMPORARILY.
    axarr = 0[fig.add_subplot(subplotspec1),
            1 fig.add_subplot(subplotspec_line), 
            2 fig.add_subplot(subplotspec2), 
            3 fig.add_subplot(subplotspec3),
            4 fig.add_subplot(subplotspec_centers),
            5 fig.add_subplot(subplotspec_species)]
    """

    # Set up stats plots

    # Setup centres plot. It would be nice to make this smaller to match the
    # distribution plots.
    axarr[0].axis([0, 100, 0 , 100])
    axarr[0].set_title("Centres of Mass")
    axarr[0].set_xlabel("Accept")
    axarr[0].set_ylabel("Give")

    # Setup species plot.
    axarr[1].set_xlim(0, rounds)
    axarr[1].set_ylim(0, 1)
    axarr[1].set_title("Relative Population Size")
    axarr[1].set_xlabel("Round Number")
    axarr[1].set_ylabel("Proportion of Population")

    # Set scores plot range
    axarr[2].set_xlim(0, rounds)
    axarr[2].set_ylim(0, 100)
    axarr[2].set_title("Average Scores")
    axarr[2].set_ylabel("Average Cash per Deal")
    axarr[2].set_xlabel("Round Number")

    # Set up strategy distribution plots

    pos = 3
    
    for team in game.teams: 
        axarr[pos] = fig.add_subplot(subplotspec_dists[pos - 3])
        img.append(axarr[pos].imshow(team.distribution, 
                                     interpolation = 'nearest',
                                     cmap = plt.cm.ocean,
                                     extent = (0.5, 
                                               np.shape(team.distribution)[0] + 
                                               0.5, 0.5,
                                               np.shape(team.distribution)[1] + 
                                               0.5)))

        axarr[pos].set_ylabel("Give")
        axarr[pos].set_xlabel("Accept")
        axarr[pos].set_title(team.name)

        cbar.append(plt.colorbar(img[pos - 3], ax = axarr[pos],
                                 label = "Prevalence vs. Uniform"))

        pos += 1    

    return (fig, axarr, img, cbar)
    

def update_figures(fig, axarr, img, cbar, game, round_number, **params):
    
    dimension = params['DIMENSION']
    granularity = params['GRANULARITY']
    unit_value = params['UNIT_VALUE']
    number_of_teams = params['NUMBER_OF_TEAMS']
    colors = ["red", "purple", "yellow", "green", "blue", "orange", "black"]
    # -----graphics-----

    for i in range(3, number_of_teams + 3):
        j = i - 3
        img[j].set_array(game.teams[j].distribution / unit_value)
        cbar[j].set_clim(vmin = 0, 
                             vmax = np.max(game.teams[j].distribution / 
                                           unit_value))
        cbar[j].draw_all()

        deal_data = game.teams[j].stats['average_deal'][:round_number + 1]
        axarr[2].plot(deal_data, color = colors[j])

        pop_data = game.teams[j].stats['population'][:round_number + 1]
        axarr[1].plot(pop_data, color = colors[j])

        cm = game.teams[j].stats['center_of_mass'][round_number]
        axarr[0].plot([cm[1]], [100 - cm[0]], marker = 'o', color = colors[j])

        axarr[i].axis((1,101,1,101))
    
    axarr[0].axis((1,101,1,101))

    return (fig, axarr, img, cbar)


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