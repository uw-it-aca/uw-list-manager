# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from django_mailman3.lib.mailman import get_mailman_client
import logging

logging.getLogger().setLevel(logging.INFO)


class Command(BaseCommand):
    help = "Query all lists for the given configuration setting"

    def add_arguments(self, parser):
        parser.add_argument(
            'settings', type=str,
            help=('Comma separated settings list to report. '
                  '<name>=<value> sets setting to value.'))

        parser.add_argument(
            '--commit',
            action='store_true',
            default=False,
            help='Confirm specified values should be saved.',
        )

    def handle(self, *args, **options):
        settings = options.get('settings', '').split(',')
        commit = options.get('commit', False)
        client = get_mailman_client()

        page_number = 1
        page_count = 500

        while page_number > 0:
            lists = client.get_list_page(
                count=page_count, page=page_number)

            if len(lists) == 0:
                break

            for mlist in lists:
                for setting in settings:
                    setting_name, new_value = setting.split('=')
                    print(f"{mlist.list_name}: "
                          f"{setting_name} is {mlist.settings[setting_name]}")
                    if new_value:
                        actual_value = True if (
                            new_value == 'True') else False if (
                                new_value == 'False') else new_value

                        if commit:
                            mlist.settings[setting_name] = actual_value
                            mlist.settings.save()

                        print(f"{mlist.list_name}: {setting_name} "
                              f"{'changed to' if commit else 'would be'} "
                              f"{actual_value}")

            page_number += 1
