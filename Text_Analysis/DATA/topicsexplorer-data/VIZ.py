import json
import numpy as np
import os
import pyLDAvis


data_input['phi'] = np.loadtxt(open("topics.csv", "rb"), delimiter=",", skiprows=1)
data_input['theta'] =  np.loadtxt(open("document-topic-distribution.csv", "rb"), delimiter=",", skiprows=1)

print(data_input['theta'])



def load_model(filename):
    with open(filename, 'r') as j:
        data_input = json.load(j)
    data = {'topic_term_dists': data_input['phi'],
            'doc_topic_dists': data_input['theta'],
            'doc_lengths': data_input['doc.length'],
            'vocab': data_input['vocab'],
            'term_frequency': data_input['term.frequency']}
    return data

movies_model_data = load_model('data/movie_reviews_input.json')

print('Topic-Term shape: %s' % str(np.array(movies_model_data['topic_term_dists']).shape))
print('Doc-Topic shape: %s' % str(np.array(movies_model_data['doc_topic_dists']).shape))


movies_vis_data = pyLDAvis.prepare(**movies_model_data)



pyLDAvis.display(movies_vis_data)
