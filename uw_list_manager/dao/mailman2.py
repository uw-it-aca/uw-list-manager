# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core.dao import DAO
from restclients_core.exceptions import DataFailureException
from uw_list_manager.models import ListExists
from uw_list_manager.exceptions import ListNotFound
import logging
import json
import os


logger = logging.getLogger(__name__)


class Mailman2:
    def __init__(self):
        self._dao = Mailman2_DAO()
        self._key = self._dao.get_service_setting("REST_KEY", None)

    def list_url(self, uwnetid):
        raise Exception("Not implemented")

    def list_existance_url(self, uwnetid):
        return f"/{self._key}/admin/v1.0/uwnetid/available/?uwnetid={uwnetid}"

    def list_admin_url(self, list_name):
        return f"https://mailman.u.washington.edu/mailman/admin/{list_name}"

    def get_list_existance_by_name(self, list_name):
        """
        Query mailman2 server for list_id

        Return True if the corresponding mailman list is avaliable
        for the given list name string
        @param list_name: a non_empty string
        """
        url = self.list_existance_url(list_name)
        exists = False
        admin_url = ""
        try:
            response = self._dao.get_resource(url)
            exists = response.get("Available", "True") == "False"
            if exists:
                admin_url = self.list_admin_url(list_name)
        except ListNotFound:
            pass

        return ListExists(
            list_name=list_name, exists=exists, admin_url=admin_url)


class  Mailman2_DAO(DAO):
    def service_name(self):
        return "mailman2"

    def service_mock_paths(self):
        return [os.abspath(os.path.join(os.dirname(__file__), "resources"))]

    def get_resource(self, url):
        try:
            response = self.getURL(url, {'Accept': 'application/json'})

            logger.debug("GET {} ==status==> {}".format(url, response.status))

            if response.status == 200:
                logger.debug("GET {} ==data==> {}".format(url, response.data))
                return json.loads(response.data.decode('utf-8'))

            if response.status != 404:
                raise DataFailureException(
                    list_url, response.status, response.data)

        except DataFailureException as ex:
            if ex.status != 404:
                raise ex

        raise ListNotFound()

