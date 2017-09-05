import argparse
import urllib

import os
from onedrivesdk.request.children_collection import ChildrenCollectionRequest


class Util:
    client = None

    args = argparse.Namespace

    depth = 0

    request_options = {
        # 'top': 200  # limit of children per request by API
    }

    files = {}

    def __init__(self, client) -> None:
        self.client = client

        self.parse_args()

        super().__init__()


    def list(self, item):
        if item.folder:
            self.item_print('/{name}/', item)

            if not self.args.depth or self.depth < self.args.depth:
                self.iterate_all_pages_and_do_stuff(onedrive_id=item.id, func=self.list)

                self.depth -= 1

        elif item.file:
            self.item_print('- {name}', item)

        else:
            self.item_print('*** {name}', item)


    def download(self, item):
        if item.folder:
            self.item_print('/{name}/', item)

            self.iterate_all_pages_and_do_stuff(onedrive_id=item.id, func=self.download)

        elif item.file:
            target_folder = './{}'.format(
                urllib.request.unquote(
                    item.parent_reference.path[13:]
                )
            )
            target_file = '/'.join([target_folder, urllib.request.unquote(item.name)])

            if os.path.exists(target_file) and os.path.getsize(target_file) == item.size:
                self.print('Skipping {}, file already exists with same size'.format(target_file), item)

                return

            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            self.print('Downloading {} ...'.format(target_file), item)

            self.client.item(drive='me', id=item.id).download(target_file)

        else:
            self.item_print('*** {name}', item)


    def check_duplicities(self, item):
        if item.folder:
            self.item_print('/{name}/', item)

            self.iterate_all_pages_and_do_stuff(onedrive_id=item.id, func=self.check_duplicities)

        elif item.file:
            if item.name in self.files:
                # self.item_print(' ### Duplicity {name}', item)
                # print('  ---> {}'. format(
                #     self.files[item.name]['path']
                # ))

                self.files[item.name].append({
                    urllib.request.unquote(item.parent_reference.path): item.size
                })
            else:
                self.files[item.name] = [{
                    urllib.request.unquote(item.parent_reference.path): item.size,
                }]
        else:
            self.item_print('*** {name}', item)

    @staticmethod
    def human_readable_size(file_size, precision=2):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
        suffix_index = 0

        while file_size > 1024 and suffix_index < 4:
            suffix_index += 1  # increment the index of the suffix
            file_size = file_size / 1024.0  # apply the division

        return "%.*f%s" % (precision, file_size, suffixes[suffix_index])


    def get_collection_by_id(self, item_id):
        return self.client.item(drive='me', id=item_id).children.request(**self.request_options).get()

    def get_collection_by_path(self, item_path):
        return self.client.item(drive='me', path=item_path).children.request(**self.request_options).get()

    def iterate_all_pages_and_do_stuff(self, onedrive_folder=None, onedrive_id=None, func=None):
        self.depth += 1

        if onedrive_folder:
            collection = self.get_collection_by_path(onedrive_folder)
        elif onedrive_id:
            collection = self.get_collection_by_id(onedrive_id)
        else:
            collection = self.get_collection_by_path(self.args.path)

        page = 1

        while True:
            # print('\nPAGE {}'.format(page))

            for item in collection:
                func(item)

            if hasattr(collection, '_next_page_link'):
                collection = ChildrenCollectionRequest.get_next_page_request(collection, self.client, self.request_options).get()

                page += 1
            else:
                break

    def item_print(self, format_string, item):
        self.print(format_string.format(
            name=item.name,
        ), item)

    def print(self, string, item):
        print('{indent}{string} [{size}]'.format(
            indent = '    ' * (self.depth - 1),
            string = string,
            size = self.human_readable_size(item.size)
        ))

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Process some integers.')

        parser.add_argument('path', metavar='<path>', type=str,
                            help='Path in OneDrive folder structure'
        )

        parser.add_argument('--depth', dest='depth', action='store', type=int,
                            help='Level for traversing folders')

        self.args = parser.parse_args()