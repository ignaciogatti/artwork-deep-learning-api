import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

df_artworks = pd.read_csv('/home/ignacio/Devel/art-retrieval-api/app/main/service/train_mayors_style_encoded.csv')
artwork_code_matrix = np.load('/home/ignacio/Devel/art-retrieval-api/app/main/service/train_mayors_style_encode.npy')

def get_sim_arworks(image_id):
    #get similarity matrix for image_id
    sim_matrix = cosine_similarity(artwork_code_matrix[int(image_id)].reshape((1,-1)), artwork_code_matrix)
    
    #get top-n most similar
    index_sorted = np.argsort(sim_matrix)
    top_n = index_sorted[0][-11:-1]
    top_n_matrix = np.take(a=sim_matrix, indices=top_n)
    
    df_top_n = df_artworks.iloc[top_n]
    df_top_n['sim_distance'] = top_n_matrix
    
    df_top_ten = df_top_n.sort_values(by=['sim_distance'], ascending=False)
    #df_top_ten = df_top_ten.head(10)
    return list(df_top_ten['filename'].values)
