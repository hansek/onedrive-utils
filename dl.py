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

response = input('Going to download: {}, are you sure? [y/...] '.format(
      utils.human_readable_size(
          client.item(drive='me', path=onedrive_folder).get().size
      )
))

if response != 'y':
    print('Exiting....')
    exit()

items = client.item(drive='me', path=onedrive_folder).children.get()

for i in items:
    utils.download(i)
