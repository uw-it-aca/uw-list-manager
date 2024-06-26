# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class UWListManagerAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def json_response(self, data):
        return Response(data, content_type="application/json")
