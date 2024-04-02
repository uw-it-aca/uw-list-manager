# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from restclients_core import models


class ListExists(models.Model):
    list_name = models.CharField(max_length=256)
    exists = models.BooleanField()
    admin_url = models.CharField(max_length=256, null=True)

    def json_data(self):
        return {
            "list_name": self.list_name,
            "exists": self.exists,
            "admin_url": self.admin_url
        }

    def __str__(self):
        return self.json_data()
