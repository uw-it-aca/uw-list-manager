# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from django_mailman3.lib.mailman import get_mailman_client
import re
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
        raw_settings = options.get('settings', '').split(',')
        commit = options.get('commit', False)
        client = get_mailman_client()

        settings = self.parse_settings(raw_settings)

        page_number = 1
        page_count = 500

        while page_number > 0:
            lists = client.get_list_page(count=page_count, page=page_number)

            if len(lists) == 0:
                break

            for mlist in lists:
                changes = False
                for setting in settings:
                    name = setting['name']
                    new_value = setting['value']

                    if new_value is None:
                        print(f"{mlist.list_name}: "
                              f"{name} is {current_value}")
                    else:
                        current_value = mlist.settings[name]

                        if new_value == current_value:
                            continue

                        mlist.settings[name] = new_value
                        changes = True

                        print(f"{mlist.list_name}: {name} "
                              f"{'changed to' if commit else 'would be'} "
                              f"{new_value}")

                if changes and commit:
                    mlist.settings.save()
                    print(f"{mlist.list_name}: settings saved")

            page_number += 1

    def parse_settings(self, raw_settings):
        settings = []
        for setting in raw_settings:
            values = re.match(r'^([^=]+)(=([^=]+))?$', setting)

            if not values:
                raise ValueError(
                    f"Invalid setting format: {setting}. "
                    "Use <name> or <name>=<value>.")

            name = values.group(1)
            raw_value = values.group(3)
            new_value = None if raw_value is None else True if (
                raw_value.lower() == 'true') else False if (
                    raw_value.lower() == 'false') else raw_value

            settings.append({'name': name, 'value': new_value})

        return settings
