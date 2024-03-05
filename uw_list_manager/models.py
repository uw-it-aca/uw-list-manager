# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db import models


class List(models.Model):
    list_id = models.CharField(max_length=128)
    list_name = models.CharField(max_length=128)
    mail_host = models.CharField(max_length=128)
    display_name = models.CharField(max_length=200)
    advertised = models.BooleanField(null=True)
    description = models.CharField(max_length=512)
    member_count = models.IntegerField()
    self_link = models.CharField(max_length=200)
    volume = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)

        data = kwargs.pop('data', None)
        self.list_name = data.get('list_name')
        self.mail_host = data.get('mail_host')
        self.advertised = data.get('advertised')
        self.description = data.get('description')
        self.display_name = data.get('display_name')
        self.list_id = data.get('list_id')
        self.member_count = data.get('member_count')
        self.self_link = data.get('self_link')
        self.volume = data.get('volume')

    @property
    def fqdn_listname(self):
        return f"{self.list_name}@{self.mail_host}"

    @property
    def manage_url(self):
        return f"https://{self.mail_host}/postorius/lists/{self.list_id}/"

    @property
    def archive_url(self):
        return (f"https://{self.mail_host}/hyperkitty"
                f"/list/{self.fqdn_listname}/")

    def json_data(self):
        return {
            "list_name": self.list_name,
            "mail_host": self.mail_host,
            "fqdn_listname": self.fqdn_listname,
            "manage_url": self.manage_url,
            "archive_url": self.archive_url,
            "advertised": self.advertised,
            "description": self.description,
            "display_name": self.display_name,
            "list_id": self.list_id,
            "member_count": self.member_count,
            "self_link": self.self_link,
            "volume": self.volume
        }

    def __str__(self):
        return self.json_data()
