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


class Mailman2:
    def __init__(self):
        self._url_base = settings.get('MAILMAN_BASE_VERSION', '3.1')
        self._dao = Mailman2_DAO()

    def get_list_by_list_name(list_name):
        """
        Query mailman2 server for list_id
        """
        raise ListNotFound(list_name)


class  Mailman2_DAO(DAO):
    def service_name(self):
        return "mailman2"

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]
