import pandas as pd
from collections import Counter
from pymongo import MongoClient


def get_business(user_id):
    '''
    return business reviewed by a given user_id
    INPUT: string
    OUTPUT: pandas DataFrame
    '''
    # get all restaurants reviewed by the user_id
    row_list = []
    for id in review['business_id']:
        business_cursor = db.business.find({'business_id': id})
        row_list.append(list(business_cursor))
    # convert to pandas DataFrame
    business = pd.DataFrame()
    for i in range(len(row_list)):
    business = pd.concat([business, pd.DataFrame(row_list[i])], ignore_index=True)
    return business

def get_category_words(user_id):
    '''
    return category words for a given user_id
    INPUT: string
    OUTPUT: dict
    '''
    business = get_business(user_id)
    cat_words = []
    for i in range(len(business)):
        for word in business.categories[i].split(', '):
            cat_words.append(word)

    words_count = Counter(cat_words)
    word_dict = dict(words_count.most_common())
    return word_dict


