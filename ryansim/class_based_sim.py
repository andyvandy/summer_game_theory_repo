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
from graphics_functions_oo import initialize_figure, create_video_from_frames
from graphics_functions_oo import update_figures
from utility_functions import clear_directory, remove_file
from game_class import Game

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
    params['UNIT_VALUE'] = 1.0 / (params['DIMENSION'] ** 2)

    params['NUMBER_OF_TEAMS'] = len(params['TEAM_SPEC'])

    # Initialize game
    game = Game(**params)

    # Initialize plot
    fig, axarr, img, cbar = initialize_figure(game, **params)

    # MAIN LOOP
    for round_number in range(params['ROUNDS']):
        game.calc_scores(**params)

        game.update_data(round_number, **params)

        print "*******************************"
        print "round_number:", round_number

        for team in game.teams:
            print team.stats.loc[round_number]

        print "*******************************"

        fig, axarr, img, cbar = update_figures(fig, axarr, img, cbar, game, 
                                               round_number, **params)

        filename = params['SIM_NAME'] + "%04d.png" % round_number
        fig.savefig(os.path.join("output", "tmp", filename), dpi=120)

    remove_file(os.path.join("output", "videos", params["SIM_NAME"] + ".mp4"))

    create_video_from_frames(params['SIM_NAME'])

    clear_directory(os.path.join("output", "tmp"))


if __name__=="__main__":
    main()