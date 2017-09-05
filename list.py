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

utils.iterate_all_pages_and_do_stuff(onedrive_folder=onedrive_folder, func=utils.list)
