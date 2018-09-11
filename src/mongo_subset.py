import sys, json
import pandas as pd
from pymongo import MongoClient

def Mongo_subset():
    #read in the whole phx restaurant data
    #filename = './yelp_dataset/restaurant_review_user_phx.csv'
    #phx = pd.read_csv(filename, index_col=0)

    # only take smalll subset
    #sub_columns = ['user_id', 'business_id', 'categories']
    #phx_sub = phx[sub_columns]

    #read phx restaurant data which users with 5 or more reviews
    filename = './yelp_dataset/phx_review_5.csv'
    phx_sub = pd.read_csv(filename, index_col=0)
    # get subset of user with review counts greater or equals to 5
    phx_review_5 = phx_sub.groupby('user_id').filter(lambda x: x['business_id'].count() >= 5)

    # Connect to the hosted MongoDB instance
    client = MongoClient()

    # create database phx
    db = client['phx']

    # store the dataset into MongoDB phx under collection of review5up
    db['review5up'].insert_many(phx_review_5.to_dict('records'))

if __name__ == '__main__':
    Mongo_subset()