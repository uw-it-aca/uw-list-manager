# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import re_path
from uw_list_manager.views.api.lists import ListView
from uw_list_manager.views.api.list_exists import ListExistsView


urlpatterns = [
    re_path(r'^api/v1/list/(?P<list_name>[\w\-]+)$',
            ListView.as_view(), name='list_name'),
    re_path(r'^api/v1/list/(?P<list_name>[\w\-]+)/exists$',
            ListExistsView.as_view(), name='list_name'),
]
