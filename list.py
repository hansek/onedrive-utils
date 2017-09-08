#!/usr/bin/env python3

from auth import authenticate_and_get_client
from utils import Util

client = authenticate_and_get_client()

utils = Util(client)

utils.iterate_over_folders_list(
    func=utils.list
)
