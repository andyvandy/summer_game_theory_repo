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

# TODO: Make the parameters below into arguments or put them in another file.

# Defines how fine the grid of strategies is. Higher granularity => less
# distinct strategies.
GRANULARITY = 1

# Calculate the dimension of the strategy array
DIMENSION = (100 / GRANULARITY + 1)

# Get the density of one stragegy from a uniform distribution over the strategy 
# array
STARTING_PCT = 1.0 / (DIMENSION ** 2)

rounds = 500

# Initialize average deal data list
avg_deal_data = []

# Set backend to Agg rendering to a GTK 2.x canvass
matplotlib.use('GTKAgg') 


def main():
    # Whether or not to have a noisy start. This should be a proper parameter.
    random_start = 0

    # What does this do?
    do_pause=1

    if random_start:
        # Randomize strategy distribution
        teams = np.random.random((DIMENSION,DIMENSION))
        # Normalize
        teams = teams / teams.sum()   
    else:
        # Create uniform strategy distribution
        teams = [STARTING_PCT] * DIMENSION ** 2
        teams = np.reshape(teams, (DIMENSION, DIMENSION))

    # Initialize plot with initial matrix? Not 100% sure
    fig, axarr = plot_init(np.matrix(teams))

    # Main loop
    for k in range(rounds):
        # Print current round to console
        print "round:", k

        # Update strategy distribution
        teams = update(teams, k)

        # Pause if appropriate
        if k % 25 == 0 and do_pause: plt.waitforbuttonpress()

        # Update screen
        plot_update(fig ,axarr,teams,k)
    
    # Pause
    pause = raw_input("press enter to exit")
    

def update(teams,k):
    """Updates the strategy distribution.

    Args:
        teams: the strategy distribution
        k: the current round

    Returns:
        teams: the new strategy distribution
    """

    # Calculate team scores
    scores = calc_scores(teams)

    # Calculate average deal and add to list. Currently global :|
    avg_deal_data.append(scores.sum() / (DIMENSION ** 2))

    # Print average deal to console
    print "avg cash per deal", avg_deal_data[-1]

    # Not sure what this is!
    max_locations = np.where(scores == scores.max()) #todo: print and parse this

    # Sum the scores over all of the strategies
    total_sum = np.sum(scores * teams)

    # Get the new scores
    new_scores = (((scores) / total_sum - (1.0 / (DIMENSION ** 2))) + 
                  np.ones((DIMENSION, DIMENSION)))

    # Update and normalize strategy distribution
    teams = teams * new_scores
    teams = teams / teams.sum()

    return teams
    

def calc_scores(teams):
    """Calculates the fitness matrix.

    Args:
        teams: a tuple representing the team and also the population breakdown.

    Returns:
        scores: the team's fitness
    """

    # Initialize array
    scores = np.zeros((DIMENSION, DIMENSION))

    # What does this do?
    interim = np.array([[100 - i * GRANULARITY for i in range(DIMENSION)]] * 
                       DIMENSION)

    # What does this do?
    teams_mod = teams * interim

    # Generate scores matrix
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            # points from being a dealmaker
            scores[i][j] = (scores[i][j] + 0.5 * (100 - i * GRANULARITY) * 
                            teams[:, (DIMENSION - i): DIMENSION].sum())
            # points from being a dealtaker
            scores[i][j] = scores[i][j] + 0.5 * teams_mod[j: DIMENSION, :].sum()

    return scores
    

def plot_init(data):
    """Initialize plot.

    Args:
        data: team matrix
    """

    # Set figure style
    sns.set_style("dark")

    # Create subplot grid
    fig = gridspec.GridSpec(2, 1)

    # Create subplots
    axarr = [plt.subplot(fig[0, 0]), plt.subplot(fig[1, 0])]

    # Plot data
    img = axarr[0].imshow(data, interpolation = 'nearest', cmap = plt.cm.ocean,
                          extent = (0.5, np.shape(data)[0] + 0.5, 0.5, 
                                    np.shape(data)[1] + 0.5))

    # Display round
    plt.title("Current Round:" + str(0))

    # Set labels
    axarr[0].set_ylabel("Give")
    axarr[0].set_xlabel("Accept")
    axarr[0].set_title("Distribution of Teams")

    # Plot average deal data
    axarr[1].plot(avg_deal_data)

    # Set labels
    axarr[1].set_xlim(0,rounds)
    axarr[1].set_ylabel("Average Cash per Deal")
    axarr[1].set_xlabel("Round Number")

    # Create colorbar for strategy distribution
    plt.colorbar(img, ax=axarr[0], label= "Prevalence vs. Uniform")

    # Interactive mode
    plt.ion()

    # Changed this to use 'normal' instead of 'zoomed' since it didn't work on
    # my system
    mng = plt.get_current_fig_manager()
    mng.window.state('normal')

    # Display everything
    plt.show()

    return fig, axarr
    

def plot_update(fig, axarr, data, round):
    """Update the plot.

    Args:
        fig: 
        axarr:
        data:
        round:
    """

    # Clear plots
    plt.cla()

    # Compare distribution to uniform
    dota = data / STARTING_PCT

    # Create subplots
    axarr = [plt.subplot(fig[0,0]), plt.subplot(fig[1, 0])]

    # Plot data (or dota, rather...)
    img = axarr[0].imshow(dota, interpolation='nearest', cmap = plt.cm.ocean,
                          extent = (0.5, np.shape(dota)[0] + 0.5, 0.5, 
                                    np.shape(dota)[1] + 0.5))

    # Plot average deal data
    axarr[1].plot(avg_deal_data)
    axarr[1].set_xlim(0, rounds)

    # Show round
    plt.title("Current Round:" + str(round))

    # Set labels
    axarr[0].set_ylabel("Give")
    axarr[0].set_xlabel("Accept")
    axarr[1].set_ylabel("Average Cash per Deal")
    axarr[1].set_xlabel("Round Number")

    # Set color bar
    plt.colorbar(img,ax=axarr[0],label= "Prevalence vs. Uniform")

    # Draw plots
    plt.draw()

    #plt.savefig("imageresult/" +str(round)+ ".png")
 

if __name__=="__main__":
    main()