import urllib

import os
from onedrivesdk.request.children_collection import ChildrenCollectionRequest


class Util:
    client = None

    request_options = {
        # 'top': 200  # limit of children per request by API
    }

    files = {}

    def __init__(self, client) -> None:
        self.client = client

        super().__init__()


    def list(self, item):
        if item.folder:
            self.item_print('{name}/', item)

            self.iterate_all_pages_and_do_stuff(onedrive_id=item.id, func=self.list)

        elif item.file:
            self.item_print('  - {name}', item)

        else:
            self.item_print('*** {name}', item)


    def download(self, item):
        if item.folder:
            self.item_print('{name}/', item)

            for child in self.get_collection_by_id(item.id):
                self.download(child)

        elif item.file:
            target_folder = './{}'.format(
                urllib.request.unquote(
                    item.parent_reference.path[13:]
                )
            )
            target_file = '/'.join([target_folder, urllib.request.unquote(item.name)])

            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            self.print(target_file, item)

            self.client.item(drive='me', id=item.id).download(target_file)

        else:
            self.item_print('*** {name}', item)


    def check_duplicities(self, item):
        if item.folder:
            self.item_print('{name}/', item)

            for child in self.get_collection_by_id(item.id):
                self.check_duplicities(child)

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
        if onedrive_folder:
            collection = self.get_collection_by_path(onedrive_folder)
        elif onedrive_id:
            collection = self.get_collection_by_id(onedrive_id)
        else:
            raise Exception('Bubububu')

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
        print('{string} [{size}]'.format(
            string = string,
            size = self.human_readable_size(item.size)
        ))
