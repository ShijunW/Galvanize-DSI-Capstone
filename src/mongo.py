import sys, json, pymongo
from pymongo import MongoClient


def read_json(file_name):
    '''
    Read the json file into a list
    INPUT: string
    OUTPUT: list
    '''
    with open(file_name, 'r') as json_file:
        list_json = json_file.readlines()
    return list_json

def json_to_mongo(file_name, db_name, collection_name):
    '''
    Read json file and store to mongodb
    INPUT: string, string, string
    OUTPUT: None
    '''
    list_json = read_json(file_name)
    client = MongoClient()
    db = client[db_name]
    collection = db[collection_name]
    for json_item in list_json:
        record = json.loads(json_item)
        collection.insert_one(record)