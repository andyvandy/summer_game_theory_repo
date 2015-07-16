import numpy as np
from scipy import ndimage # for center of mass calculation

def calc_scores(teams, species_breakdown, **params):
    # takes in a tuple representing the team and also the population breakdown
    # returns the teams fitness

    dimension = params['DIMENSION']
    granularity = params['GRANULARITY']

    scores = [np.zeros((dimension, dimension)) for i in range(len(teams))]

    interim = np.array([range(100, -granularity, -granularity)] * dimension)

    teams_mod = teams * interim

    i_ii = species_breakdown[0] / (species_breakdown[0] + species_breakdown[1])
    i_iii = species_breakdown[0] / (species_breakdown[0] + species_breakdown[2])

    ii_i = species_breakdown[1] / (species_breakdown[1] + species_breakdown[0])
    ii_iii = species_breakdown[1] / (species_breakdown[1] + species_breakdown[2])

    iii_i = species_breakdown[2] / (species_breakdown[2] + species_breakdown[0])
    iii_ii = species_breakdown[2] / (species_breakdown[2] + species_breakdown[1])

    j_mat1 = np.matrix([[teams_mod[0][j: dimension, :].sum()] * 
                        dimension for j in range(dimension)])
    i_mat1 = np.matrix([[(100 - i * granularity) * 
                         teams[0][:, (dimension - i): dimension].sum() for i in range(dimension)]] * dimension)

    j_mat2 = np.matrix([[teams_mod[1][j: dimension, :].sum()] * 
                        dimension for j in range(dimension)])
    i_mat2 = np.matrix([[(100 - i * granularity) * 
                         teams[1][:, (dimension - i): dimension].sum() for i in range(dimension)]] * dimension)

    j_mat3 = np.matrix([[teams_mod[2][j: dimension, :].sum()] * 
                        dimension for j in range(dimension)])
    i_mat3 = np.matrix([[(100 - i * granularity) * 
                         teams[2][:, (dimension - i): dimension].sum() for i in range(dimension)]] * dimension)

    scores[0] = np.array(0.5 * (ii_iii * (j_mat2 + i_mat2) + iii_ii * (j_mat2 + i_mat2)))
    scores[1] = np.array(0.5 * (i_iii * (j_mat1 + i_mat1) + iii_i * (j_mat3 + i_mat3)))
    scores[2] = np.array(0.5 * (i_ii * (j_mat1 + i_mat1) + ii_i * (j_mat2 + i_mat2)))

    """
    for i in range(dimension):
        for j in range(dimension):
            points_deal_from_p1 = teams_mod[0][j: dimension, :].sum()   
            points_deal_to_p1 = ((100 - i * granularity) * 
                                 teams[0][:, (dimension - i): dimension].sum())

            points_deal_from_p2 = teams_mod[1][j: dimension,:].sum()   
            points_deal_to_p2 = ((100 - i * granularity) * 
                                 teams[1][:, (dimension - i): dimension].sum())

            points_deal_from_p3 = teams_mod[2][j: dimension, :].sum()   
            points_deal_to_p3 = ((100 - i * granularity) * 
                                 teams[2][:, (dimension - i): dimension].sum())
            
            scores[0][i][j] = 0.25 * (points_deal_from_p2 + points_deal_to_p2 + 
                                      points_deal_from_p3 + points_deal_to_p3)

            scores[1][i][j] = 0.25 * (points_deal_from_p1 + points_deal_to_p1 + 
                                      points_deal_from_p3 + points_deal_to_p3)

            scores[2][i][j] = 0.25 * (points_deal_from_p1 + points_deal_to_p1 + 
                                      points_deal_from_p2 + points_deal_to_p2)
    """
            

    return scores


def update_data(teams, scores, avg_deal_data, species_breakdown, 
                species_breakdown_history, round_number, **params):
    """
    """

    dimension = params['DIMENSION']
    starting_pct = params['STARTING_PCT']

    avg_deal_data[0].append(scores[0].sum() / (dimension ** 2))
    avg_deal_data[1].append(scores[1].sum() / (dimension ** 2))
    avg_deal_data[2].append(scores[2].sum() / (dimension ** 2))

    print 
    print "ROUND:" , round_number
    print "avg cash per deal from team1: ", avg_deal_data[0][-1]
    print "avg cash per deal from team2: ", avg_deal_data[1][-1]
    print "avg cash per deal from team3: ", avg_deal_data[2][-1]

    '''max_locations1= np.where(scores[0]==scores[0].max()) #todo: print and parse this
    max_locations2= np.where(scores[1]==scores[1].max()) #todo: print and parse this
    max_locations3= np.where(scores[1]==scores[1].max()) #todo: print and parse this'''

    species_breakdown_history[0].append(species_breakdown[0])
    species_breakdown_history[1].append(species_breakdown[1])
    species_breakdown_history[2].append(species_breakdown[2])

    scores_sums = [scores[0].sum(),scores[1].sum(),scores[2].sum()]
    scores_sum = sum(scores_sums)
    species_multipliers = species_multipliers= scores_sums[0]/scores_sum+2.0/3,scores_sums[1]/scores_sum+2.0/3,scores_sums[2]/scores_sum+2.0/3
    species_breakdown_temp = species_breakdown[0]*species_multipliers[0],species_breakdown[1]*species_multipliers[1],species_breakdown[2]*species_multipliers[2]
    species_breakdown_sum=sum(species_breakdown_temp)
    species_breakdown=species_breakdown_temp[0]/species_breakdown_sum,species_breakdown_temp[1]/species_breakdown_sum,species_breakdown_temp[2]/species_breakdown_sum

    total_sum = np.sum(scores[0] * teams[0] + scores[1] * teams[1] + scores[2] * teams[2])

    new_scores = []

    new_scores.append(((scores[0]) / total_sum - (0.33 / (dimension ** 2))) + 1)
    new_scores.append(((scores[1]) / total_sum - (0.33 / (dimension ** 2))) + 1)
    new_scores.append(((scores[2]) / total_sum - (0.33 / (dimension ** 2))) + 1)

    teams = [teams[0] * new_scores[0], teams[1] * new_scores[1], teams[2] * new_scores[2]]
    teams = [teams[0] / teams[0].sum(), teams[1] / teams[1].sum(), teams[2] / teams[2].sum()]
    
    center_of_mass = []
    center_of_mass.append(ndimage.measurements.center_of_mass(teams[0] / starting_pct))
    center_of_mass.append(ndimage.measurements.center_of_mass(teams[1] / starting_pct))
    center_of_mass.append(ndimage.measurements.center_of_mass(teams[2] / starting_pct))

    return (teams, avg_deal_data, species_breakdown, species_breakdown_history, center_of_mass)