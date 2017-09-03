import sys

from auth import authenticate_and_get_client
from utils import Util

client = authenticate_and_get_client()

utils = Util(client)

######################

if len(sys.argv) < 2:
    print('Error: Path to target folder not specified')
    exit()

onedrive_folder = sys.argv[1]

collection = utils.get_collection_by_path(onedrive_folder)

for collection_item in collection:
    utils.do_something(collection_item)
