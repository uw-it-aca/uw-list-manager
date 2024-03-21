# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_mailman3 import Mailman3
from uw_mailman3.exceptions import ListNotFound
from uw_list_manager.models import ListExists


class Mailman3:
    def __init__(self, *args, **kwargs):
        self._dao = Mailman3()
        super(Mailman3, self).__init__(*args, **kwargs)

    def get_list_existance_by_name(self, list_name):
        """
        Query mailman3 server for list_id

        Return True if the corresponding mailman list is avaliable
        for the given list name string
        @param list_name: a non_empty string
        """
        exists = False
        admin_url = None
        try:
            maillist = self._dao.get_list_by_name(list_name)
            exists = True
            admin_url = mailist.self_link
        except ListNotFound:
            pass

        return ListExists(
            list_name=list_name, exists=exists, admin_url=admin_url)
