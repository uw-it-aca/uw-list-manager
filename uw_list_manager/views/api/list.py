# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_list.views.api import UWListManagerAPI
from uw_list_manager.dao.mailman3 import Mailman3
from uw_list_manager.dao.mailman2 import Mailman2
from uw_list_manager.exceptions import ListNotFound


class ListView(UWListManagerAPI):
    """
    Class to laod mail list information
    """

    def get(self, request, list_name):
        try:
            list = Mailman3.get_list_by_name(list_name)
        except ListNotFound as ex:
            try:
                list = Mailman2.get_list_by_name(list_name)
            except ListNotFound as ex:
                return self.error_response(404, f"List {list_name} not found")

        return self.json_response(list.json_data())
