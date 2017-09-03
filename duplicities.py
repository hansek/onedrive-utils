import pprint

import time

import sys

from auth import authenticate_and_get_client
from utils import Util

client = authenticate_and_get_client()

utils = Util(client)

######################

t0 = time.time()

if len(sys.argv) < 2:
    print('Error: Path to target folder not specified')
    exit()

onedrive_folder = sys.argv[1]

collection = utils.get_collection_by_path(onedrive_folder)

for collection_item in collection:
    utils.check_duplicities(collection_item)

pp = pprint.PrettyPrinter(indent=4)

duplicates = {}
sizes = {}
for file, data in utils.files.items():
    sizes = {}

    if len(data) > 1:
        for item in data:
            for path in item:
                size = item[path]

                if size in sizes:
                    sizes[size].append(path)
                else:
                    sizes[size] = [path]

        for size, paths in sizes.items():
            if len(paths) > 1:
                if file not in duplicates:
                    duplicates[file] = {}

                duplicates[file][size] = paths

        # duplicates[file] = data

print()

pp.pprint(duplicates)

t1 = time.time()
total = t1-t0

print('Execution time: {} s'. format(total))
