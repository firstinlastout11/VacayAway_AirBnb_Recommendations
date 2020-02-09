import pandas as pd

def score_noSA(feature_vector, weight_vector, bool_verbose): # outputs a score for a record
    feature_vector[weight_vector.columns] = feature_vector[weight_vector.columns].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    feature_vector['finalScore'] = 0
    for col in weight_vector.columns:
        if(bool_verbose):
    	    print("Factoring in column:", col)
        feature_vector['finalScore'] = feature_vector['finalScore'] + (weight_vector[col][0] * feature_vector[col]) # weighted sum
    return(feature_vector)