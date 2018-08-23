import multiprocessing
import requests
import sys
import threading
from timeit import Timer
import warnings


def request_item(item_id):
    print("Thread {} starts ...".format(threading.currentThread().getName()))
    try:
        r = requests.get("http://hn.algolia.com/api/v1/items/{}".format(item_id))
        
    except requests.RequestException as e:
        warnings.warn(f"Request for {item_id} failed\n{e.message}")
        #warnings.warn("Request for {item_id} failed\n{message}".format(item_id=item_id, message=e.message))
        return None
    print("Thread {} is completed.".format(threading.currentThread().getName()))
    return r.json()


def request_sequential(id_min=1, id_max=21):
    sys.stdout.write("Requesting sequentially...\n")
    
    # get the metadata of all posts with an item_id ranging from 1 to 20
    
    for item_id in range(id_min, id_max):
        request_item(item_id)

    sys.stdout.write("done.\n")

def request_concurrent(id_min=1, id_max=21):
    sys.stdout.write("Requesting in parallel...\n")
    
    jobs = []
    for i in range(id_min, id_max):
        thread = threading.Thread(name=i, target=request_item, args=(i, ))
        jobs.append(thread)
        thread.start()
    print("Waiting for threads to finish execution.")
    for j in jobs:
        j.join()
    
    sys.stdout.write("done.\n")

if __name__ == '__main__':
    t = Timer(lambda: request_sequential())
    print("Completed sequential in {} seconds.".format(t.timeit(1)))
    print("--------------------------------------")

    t = Timer(lambda: request_concurrent())
    print("Completed using threads in {} seconds.".format(t.timeit(1)))
