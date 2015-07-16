# ultimatum_sim_stu_dev.py
# Authors: Andrew van den Hoeven, Stuart Squires
# Date: July 2015
# 
# This is a replicator dynamics ultimatum game simulation. Information on the
# model can be found in README.md. Parameters are set in graphics.

# Libraries required:
#
# numpy
# matplotlib
# matplotlib.pylab
# matplotlib.gridspec
# seaborn
# os
# subprocess
# shutil
# scipy ndimage

# import libraries
import matplotlib
import os

# import local functions
from game_logic import calc_scores, update_data
from graphics_functions import initialize_figure, create_video_from_frames
from graphics_functions import update_figures
from utility_functions import clear_directory, remove_file
from initial_matrix_generators import initialize_starting_distribution

# Import parameters
from ultimatum_params import PARAMS


def main():
    """Main script.
    """

    # Use Agg backend for matplotlib. Why?
    matplotlib.use('Agg')

    # Load in parameters
    params = PARAMS.copy()

    # Calculate dimension of the strategy arrays
    params['DIMENSION'] = (100 / params['GRANULARITY'] + 1)

    # Calculate the value of a single unit of a strategy based on uniform dist.
    params['STARTING_PCT'] = 1.0 / (params['DIMENSION'] ** 2)

    # Initialize teams
    teams = initialize_starting_distribution(**params)

    species_breakdown = [1.0 / 3.0] * 3

    species_breakdown_history = [[], [], []]

    # Initialize average deal data lists
    avg_deal_data = [[], [], []]

    data = teams

    fig, axarr, img, cbar = initialize_figure(avg_deal_data, data, **params)

    # MAIN LOOP
    for i in range(0, params['ROUNDS']):
        scores = calc_scores(teams, species_breakdown, **params)

        results = update_data(teams, scores, avg_deal_data, species_breakdown, 
                              species_breakdown_history, i, **params)

        teams = results[0]
        avg_deal_data = results[1]
        species_breakdown = results[2]
        species_breakdown_history = results[3]
        center_of_mass = results[4]

        update_figures(fig, axarr, img, cbar, teams, avg_deal_data, 
               species_breakdown_history, center_of_mass, i, **params)

        filename = params['SIM_NAME'] + "%04d.png" % i
        fig.savefig(os.path.join("output", "tmp", filename), dpi=150)

    remove_file(os.path.join("output", "videos", params["SIM_NAME"] + ".mp4"))

    create_video_from_frames(params['SIM_NAME'])

    clear_directory(os.path.join("output", "tmp"))


if __name__=="__main__":
    main()