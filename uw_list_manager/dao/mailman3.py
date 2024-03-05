# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from uw_list_manager.exceptions import ListNotFound
from restclients_core.exceptions import DataFailureException
from restclients_core.dao import DAO
from uw_list_manager.models import List
from os.path import abspath, dirname
from base64 import b64encode
import os


class Mailman3:
    def __init__(self):
        self._url_base = settings.get('MAILMAN_BASE_VERSION', '3.1')
        self._dao = Mailman3_DAO()

    def _list_url(self, list_name):
        full_list_name = f"{list_name}@{settings.get('CLUSTER_NAME')}"
        return f"{self._url_base}/lists/{full_list_name}"

    def get_list_by_list_name(list_name):
        """
        Query mailman3 server for list_id
        """
        url = self._list_url(f"{list_name}@f{settings.get('CLUSTER_NAME')}}")
        return get_list(url)

    def get_list_by_list_id(list_name):
        """
        Query mailman3 server for list_name
        """
        url = self._list_url(f"{list_name}.f{settings.get('CLUSTER_NAME')}}")
        return get_list(url)

    def get_list(self, url):
        response = self._dao.getURL(url)

        if response.status == 404:
            raise ListNotFound(list_name)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return List(data=response.data)


class  Mailman3_DAO(DAO):
    def service_name(self):
        return "mailman3"

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]

    def _custom_headers(self, method, url, headers, body):
        user = settings.get('MAILMAN_REST_USER')
        password = settings.get('MAILMAN_REST_PASSWORD')
        if not (user and password):
            raise Exception(
                "MAILMAN_REST_USER and MAILMAN_REST_PASSWORD are required")

        basic_auth = b64encode(bytes('{user}:{password}', 'ascii'))
        return {"Authorization": f"Basic {basic_auth}"}
