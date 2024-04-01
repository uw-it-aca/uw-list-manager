# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_mailman.basic_list import exists, get_admin_url


class Mailman2:
    def get_list_existance_by_name(self, list_name):
        """
        Query mailman2 server for list_name

        Return True if the corresponding mailman list is avaliable
        for the given list name string
        @param list_name: a non_empty string
        """
        exists = False
        admin_url = None
        try:
            exists = exists(list_name)
            admin_url = get_admin_url(list_name)
        except HTTPError as ex:
            if ex.code == 404:
                pass
            else:
                raise

        return ListExists(
            list_name=list_name, exists=exists, admin_url=admin_url)
