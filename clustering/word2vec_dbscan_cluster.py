## import libraries
import pandas as pd
import numpy as np
import gensim.downloader as api
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

## load pre-trained Word2Vec model
# use the Google News vectors, which have a vector size of 300
model = api.load('word2vec-google-news-300')

## function to vectorize each skill
def vectorize_skill(skill, model):
    # split the skill into words
    words = skill.split()
    # initialize an empty list to store the vectors
    vectors = []
    # loop through each word in the skill
    for word in words:
        # if the word is in the vocabulary of the model
        if word in model.key_to_index:
            # get the vector of the word
            vector = model[word]
            # append the vector to the list of vectors
            vectors.append(vector)
    # if the skill is empty, return a vector of zeros
    if len(vectors) == 0:
        return [0] * model.vector_size
    # return the average vector
    return sum(vectors) / len(vectors)

def main():
    # load data
    data = pd.read_csv('csv_folder/Result_OpenRefine.csv')

    # # test with a subset of 40000 rows
    # data = data

    # vectorize each skill
    data['skill_vector'] = data['skill'].apply(lambda x: vectorize_skill(x, model))

    # normalize the vectors
    scaler = StandardScaler()
    normalized_vectors = scaler.fit_transform(data['skill_vector'].tolist())
    
    ## reduce the dimensionality of the vectors using PCA
    # n_components: # of dimensions to reduce to, random_state: set seed
    # need to find a good n_components to make sure it still captures the variance but not overfit the data
    # lower n_components will reduce the # of clusters from 300 to x, less values assigned to -1 (noise) cluster
    pca = PCA(n_components=105, random_state=0) 
    reduced_vectors = pca.fit_transform(normalized_vectors)

    # # initialize the DBSCAN object
    # higher eps will reduce the number of clusters, less values assigned to -1 (noise) cluster
    dbscan = DBSCAN(metric='cosine', eps=0.15, min_samples=2)

    # # fit the DBSCAN object to the reduced data
    clusters = dbscan.fit_predict(reduced_vectors)

    # # add the cluster labels to the data
    data = data.assign(cluster=clusters)

    # # set the display option to show all rows
    pd.set_option('display.max_rows', None)

    data = data[['job_id', 'skill', 'cluster']]
    # save the data to a csv file
    # data.to_csv('csv_folder/Result_OpenRefine_Cluster.csv', index=False)

    # # Data validation
    print(data.iloc[0:400])
    # print how many skills were assigned to either 0 or -1 for the first 400 rows
    # print(data['cluster'].value_counts().iloc[0:400])

if __name__ == '__main__':
    main()