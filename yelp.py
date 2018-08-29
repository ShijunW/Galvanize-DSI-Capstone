from timeit import Timer
from yelp_helpers import request
from yelp_helpers import load_api_key
from pymongo import MongoClient
import multiprocessing
import threading

key = load_api_key()

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
API_KEY = key['client_secret']

DB_NAME = "yelp"
COLLECTION_NAME = "business"
client = MongoClient()
db = client[DB_NAME]
coll = db[COLLECTION_NAME]


POOL_SIZE = 4
SEARCH_LIMIT = 20


def city_search_parallel(city):
    """
    Retrieves the JSON response that contains the top 20 business meta data for city.
    :param city: city name
    """
    params = {'location': city, 'limit': 20}
    json_response = request(API_HOST, SEARCH_PATH, API_KEY, url_params=params)
    business_info_concurrent(json_response)



def business_info_concurrent(ids):
    """
    Extracts the business ids from the JSON object and
    retrieves the business data for each id concurrently.
    :param json_response: JSON response from the search API.
    """
    businesses = json_response['businesses']
    ids = [x['id'] for x in businesses]
    threads = len(ids)  # Number of threads to create

    jobs = []
    for i in range(0, threads):
        thread = threading.Thread(target=scrape_business_info, args=(ids[i],))
        jobs.append(thread)
        thread.start()
    for j in jobs:
        j.join()


def scrape_parallel_concurrent(pool_size):
    """
    Uses multiple processes to make requests to the search API.
    :param pool_size: number of worker processes
    """
    coll.remove({})
    pool = multiprocessing.Pool(pool_size)

    with open('../data/cities') as f:
        cities = f.read().splitlines()
        pool.map(city_search_parallel, cities)
        pool.close()
        pool.join()


def business_info(business_id):
    """
    Makes a request to Yelp's business API and retrieves the business data in JSON format.
    Dumps the JSON response into mongodb.

    Creates a separate MongoClient instance for each thread.

    :param business_id:
    """
    client = MongoClient()
    db = client[DB_NAME]
    coll = db[COLLECTION_NAME]

    business_path = BUSINESS_PATH + business_id
    response = request(API_HOST, business_path, API_KEY)
    coll.insert(response)


def city_search(location):
    """
    Makes a request to Yelp's search API given the city name.
    :param city:
    :return: JSON meta data for top 20 businesses.
    """
    url_params = {
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, API_KEY, url_params=url_params)


def scrape_sequential():
    """
    Scrapes the business's meta data for a list of cities
    and for each business scrapes the content.
    """
    coll.remove({})  # Remove previous entries from collection in Mongodb.
    with open('../data/cities') as f:
        cities = f.read().splitlines()
        for city in cities:
            response = city_search(city)
            business_ids = [business['id'] for business in response['businesses']]
            for business_id in business_ids:
                business_info(business_id)


if __name__ == '__main__':
    t = Timer(lambda: scrape_sequential())
    print("Completed sequential in {} seconds.".format(t.timeit(1)))

    t2 = Timer(lambda: scrape_parallel_concurrent(POOL_SIZE))
    print("Completed parallel in {} seconds.".format(t2.timeit(1)))