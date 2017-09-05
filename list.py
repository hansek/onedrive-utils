from auth import authenticate_and_get_client
from utils import Util

client = authenticate_and_get_client()

utils = Util(client)

utils.iterate_all_pages_and_do_stuff(onedrive_folder=None, func=utils.list)
