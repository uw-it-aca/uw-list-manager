# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from uw_mailman3.mailman3 import Mailman3


class Command(BaseCommand):
    help = "Query all lists for the given configuration setting"

    def add_arguments(self, parser):
        parser.add_argument(
            'setting', type=str, help='The setting to query for')

    def handle(self, *args, **options):
        setting = options['setting']
        self.mailman3 = Mailman3()
        for l in self.mailman3.get_all_lists():
            print(f"{l.name}: {settings} = "
                  f"{l.mailman3.get_list_sub_resource(l.name, setting)}")
