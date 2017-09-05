from auth import authenticate_and_get_client
from utils import Util

client = authenticate_and_get_client()

utils = Util(client)

response = input('Going to download: {}, are you sure? [y/...] '.format(
      utils.human_readable_size(
          client.item(drive='me', path=utils.args.path).get().size
      )
))

if response != 'y':
    print('Exiting....')
    exit()

utils.iterate_all_pages_and_do_stuff(onedrive_folder=None, func=utils.download)
