import json
import argparse
import numpy as np
from scipy.spatial import distance as dist


class Searcher:
    def __init__(self, index_arr):
        # store the index that we will be searching over
        self.index_arr = index_arr

    def search(self, input_query):
        # initialize our dictionary of results
        results = {}

        for input_image in input_query:
            min_distance = 1
            index = 0
            for model in index_array:
                for image in model:
                    d = dist.euclidean(input_image, image)
                    if d < min_distance:
                        min_distance = d
                    print index
                index = index + 1

        # sort our results, where a smaller distance indicates
        # higher similarity
        # results = sorted([(v, k) for (k, v) in results.items()])

        # return the results
        return results


ap = argparse.ArgumentParser()

ap.add_argument("-i", "--index", required=True,
                help="Path to where the index file is stored")
args = vars(ap.parse_args())
arbitrary_dict = {}

with open(args['index'], "r") as index_file:
    index_array = []
    i = 0
    for line in index_file:
        json_dict = json.loads(line)
        for key, value in json_dict.items():
            index_array.append(value)
            arbitrary_dict.update({i: key})
        i = i + 1
    index_array = np.array(index_array)

searcher = Searcher(index_array)
# searcher.search()
# def find_similar_model():
