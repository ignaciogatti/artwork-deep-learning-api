import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from google.cloud import storage
import os.path

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(os.getcwd(),'static/model')
JSON_CREDENTIALS = os.path.join( BASE_DIR, 'artwork-retrieval.json' )
METADATA_FILE_NAME = os.path.join( MODEL_DIR, 'train_mayors_style_encoded.csv' )
MATRIX_FILE_NAME = os.path.join( MODEL_DIR, 'train_mayors_style_encode.npy' )


def get_file_from_cloud_storage(filename):
    
    client = storage.Client.from_service_account_json(JSON_CREDENTIALS)
    # https://console.cloud.google.com/storage/browser/[bucket-id]/
    bucket = client.get_bucket('artwork-retrieval-data')
    # # get bucket data as blob
    blob = bucket.get_blob(os.path.basename(filename))
    blob.download_to_filename(filename)


def get_sim_arworks(image_id):

    #check if data is available
    if not( os.path.isfile( METADATA_FILE_NAME ) ):
        get_file_from_cloud_storage( METADATA_FILE_NAME )
    if not( os.path.isfile( MATRIX_FILE_NAME ) ):
        get_file_from_cloud_storage( MATRIX_FILE_NAME )

    #Load data
    df_artworks = pd.read_csv( METADATA_FILE_NAME )
    artwork_code_matrix = np.load( MATRIX_FILE_NAME )

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
