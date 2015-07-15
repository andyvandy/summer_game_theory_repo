PARAMS = {'GRANULARITY': 1,
          'ROUNDS': 2000,
          'STARTING_DISTRIBUTION': 'cluster'}

"""
GRANULARITY: Represents how fine the strategy distribution is. Higher
    granularity implies fewer strategies.

ROUNDS: The number of rounds to run the simulation for.

STARTING_DISTRIBUTION: Determines the initial distribution of strategies.
    Options:
        'rand': completely random distribution of strategies
        'uniform': uniform distribution of strategies
        'cluster': clustered strategies based on a product of binomial
            distributions
"""

# FOR WINDOWS (MODIFY TO POINT TO YOUR FFMPEG AND IMAGEMAGICK):

VIDEO_LIB_PATHS = {'FFMPEG_PATH': 'C:/Users/Andrew/bin/ffmpeg/bin/ffmpeg',
                   'CONVERT_PATH': 'C:/Program Files/ImageMagick-6.9.1-Q16/convert'}

"""
# FOR UBUNTU LINUX:
VIDEO_LIB_PATHS = {'FFMPEG_PATH': '/usr/bin/avconv',
                   'CONVERT_PATH': '/usr/bin/convert'}
"""