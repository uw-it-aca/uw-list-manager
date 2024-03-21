# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from uw_mailman3.mailman3 import Mailman3


class Command(BaseCommand):
    help = "Query all lists for the given configuration setting"

    def add_arguments(self, parser):
        parser.add_argument(
            'settings', type=str,
            help='Comma delimited list of list settings to query')

    def handle(self, *args, **options):
        settings = options.get('settings', '').split(',')
        for l in Mailman3().get_all_lists():
            for setting in settings:
                print(f"{l.name}: {setting} = "
                      f"{l.mailman3.get_list_sub_resource(l.name, setting)}")
