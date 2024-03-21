# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_list_manager.views.api import UWListManagerAPI
from uw_list_manager.dao.mailman3 import Mailman3
from uw_list_manager.dao.mailman2 import Mailman2


class ListExistsView(UWListManagerAPI):
    """
    Class to query mail list existance
    """

    def __init__(self, *args, **kwargs):
        self._mailman2 = Mailman2()
        self._mailman3 = Mailman3()
        super(ListExists, self).__init__(*args, **kwargs)

    def get(self, request, list_name):
        exist = self._mailman2.get_list_existance_by_name(list_name)
        if not exist.exists:
            exist = self._mailman3.get_list_existance_by_name(list_name)

        return self.json_response(exist.json_data())
