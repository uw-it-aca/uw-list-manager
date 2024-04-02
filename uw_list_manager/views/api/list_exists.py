# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_list_manager.views.api import UWListManagerAPI
from uw_list_manager.dao.mailman2 import Mailman2
from uw_list_manager.dao.mailman3 import Mailman3
from urllib.error import HTTPError


class ListExistsView(UWListManagerAPI):
    """
    Class to query mail list existance
    """

    def get(self, request, list_name):
        exist = Mailman2().get_list_existance_by_name(list_name)
        if not exist.exists:
            exist = Mailman3().get_list_existance_by_name(list_name)

        return self.json_response(exist.json_data())
