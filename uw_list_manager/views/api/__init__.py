# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from coursedashboards.models import Term, Course, CourseOffering
from coursedashboards.dao.user import get_current_user
from coursedashboards.views.error import _make_response, MYUW_DATA_ERROR


class UWListMangagerPI(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
