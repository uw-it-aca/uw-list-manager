# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django_mailman3.lib.mailman import get_mailman_client
from uw_list_manager.models import ListExists
from urllib.error import HTTPError


class Mailman3:
    def __init__(self, *args, **kwargs):
        self._client = get_mailman_client()
        super(Mailman3, self).__init__(*args, **kwargs)

    def get_list_existance_by_name(self, list_name):
        """
        Query mailman3 server for list_id

        Return True if the corresponding mailman list is avaliable
        for the given list name string
        @param list_name: a non_empty string
        """
        mlist = None
        if '@' not in list_name:
            for domain in self._client.domains:
                mlist = self._get_list(
                    f"{list_name}@{domain.mail_host}")
                if mlist:
                    break
        else:
            mlist = self._get_list(list_name)

        return ListExists(
            list_name=mlist.fqdn_listname if mlist else list_name,
            exists=mlist is not None,
            admin_url=self._list_admin_url(mlist))

    def _list_admin_url(self, mlist):
        return (f"https://{mlist.mail_host}/postorius/"
                f"lists/{mlist.list_id}/") if mlist else None

    def _get_list(self, list_name):
        try:
            return self._client.get_list(list_name)
        except HTTPError as ex:
            if ex.code == 404:
                return None
            else:
                raise
