from flask import Flask, render_template, jsonify
from flask import request as flask_request
import pickle
import pandas as pd
from pymongo import MongoClient
from collections import Counter
from yelp_helpers import request as yelp_request
from yelp_helpers import load_api_key
from yelp import *


app = Flask(__name__)


#with open('static/model.pkl', 'rb') as f:
#    model = pickle.load(f)


@app.route('/', methods=['GET'])
def index():
    """Render a simple splash page."""
    return render_template('index.html')

'''
@app.route('/submit', methods=['GET'])
def submit():
    """Render a page containing a textarea input where the user can paste an
    article to be classified.  """
    return render_template('form/submit.html')
'''

@app.route('/recommender', methods=['GET'])
def recommender():
    """Return restaurants for given userid and city.
    """
    #print(flask_request.form)
    #print(flask_request.args)
    # get the userid and location from the input
    #userid = flask_request.form['userid']
    userid = flask_request.args['userid']
    #print("Got UserID: ", userid)
    #userid = '--Nnm_506G_p8MxAOQna5w'
    #location = flask_request.form['location']
    location = flask_request.args['location']
    #print("Got City: ", location)
    #location = 'San Francisco'


    # Connect to the hosted MongoDB instance
    client = MongoClient()
    # using the phx database
    db = client.phx
    # reading the review5up collection
    cursor = db.review5up.find({'user_id': userid})
    review = pd.DataFrame(list(cursor))

    # get all the words from categories
    cat_words = []
    for i in range(len(review)):
        for word in review.categories[i].split(', '):
            cat_words.append(word)

    # find the most common words from categories
    words_count = Counter(cat_words)
    word_dict = dict(words_count.most_common())

    # Yelp api key and instances
    key = load_api_key()
    api_key = key['client_secret']
    host = 'https://api.yelp.com'
    path = '/v3/businesses/search'

    # retrive live data from Yelp
    # retrive the first 50 or less restaurants
    search_offset = 0
    search_limit = 50
    url_params = {'categories': "restaurants",
                'location': location,
                'limit': search_limit,
                'offset': search_offset
                }
    yelp = yelp_request(host, path, api_key, url_params)

    # continue to retrive upto 1000 restaurants
    total = min(yelp['total'], 950)
    if total > 50:
        for i in range(int(total/search_limit)):
            search_offset += search_limit
            url_params = {'categories': "restaurants",
                    'location': location,
                    'offset': search_offset,
                    'limit': search_limit
                    }
            yelp['businesses'] += yelp_request(host, path, api_key, url_params)['businesses']

    # convert the live data to pandas DataFrame
    df = pd.DataFrame(yelp['businesses'])

    # top 2 category words besides restaurants
    # list(word_dict)[1], list(word_dict)[2]
    index = []
    for i in range(len(df)):
        a = df.categories[i]
        if any((d['title'] == list(word_dict)[1]) for d in a) and \
           any((d['title'] == list(word_dict)[2]) for d in a):
            #print(i, 'Yes')
            index.append(i)
    df = df.iloc[index]

    # sort the review stars and counts by decending order
    df.sort_values(['rating', 'review_count'], ascending=False, inplace=True)

    # just get the top 5 or less restaurants
    if len(df) > 5:
        df = df[:5]

    # adding address0 and address1 columns for display address
    df['address0'] = ''
    df['address1'] = ''
    # adding review stars image url for Yelp-branded stars
    df['stars_url'] = '/static/yelp_stars/web_and_ios/regular/regular_'

    for index, row in df.iterrows():
        # update address0 and address1
        if len(row['location']['display_address']) >= 3:
            df['address0'][index] = row['location']['display_address'][0]+', '+row['location']['display_address'][1]
            df['address1'][index] = row['location']['display_address'][-1]
        if len(row['location']['display_address']) == 2:
            df['address0'][index] = row['location']['display_address'][0]
            df['address1'][index] = row['location']['display_address'][-1]
        # update stars_url based on rating
        if row['rating'] == 5.0:
            df['stars_url'][index] = row['stars_url'] +'5.png'
        if row['rating'] == 4.5:
            df['stars_url'][index] = row['stars_url'] +'4_half.png'
        if row['rating'] == 4.0:
            df['stars_url'][index] = row['stars_url'] +'4.png'
        if row['rating'] == 3.5:
            df['stars_url'][index] = row['stars_url'] +'3_half.png'
        if row['rating'] == 3.0:
            df['stars_url'][index] = row['stars_url'] +'3.png'
        if row['rating'] == 2.5:
            df['stars_url'][index] = row['stars_url'] +'2_half.png'
        if row['rating'] == 2.0:
            df['stars_url'][index] = row['stars_url'] +'2.png'
        if row['rating'] == 1.5:
            df['stars_url'][index] = row['stars_url'] +'1_half.png'
        if row['rating'] == 1.0:
            df['stars_url'][index] = row['stars_url'] +'1.png'
        if row['rating'] == 0.0:
            df['stars_url'][index] = row['stars_url'] +'0.png'


    return render_template('recommender.html', df=df)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
