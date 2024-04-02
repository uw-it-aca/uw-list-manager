# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
import base64


class Command(BaseCommand):
    help = 'Create DRF Token for a given user'

    def add_arguments(self, parser):
        parser.add_argument('usernames', type=str, nargs='*')
        parser.add_argument(
            '-d',
            '--delete',
            action='store_true',
            dest='delete_token',
            default=False,
            help='Deete existing User token',
        )
        parser.add_argument(
            '-r',
            '--reset',
            action='store_true',
            dest='reset_token',
            default=False,
            help='Reset existing User token',
        )
        parser.add_argument(
            '-l',
            '--list',
            action='store_true',
            dest='list_tokens',
            default=False,
            help='List tokens for given users or all tokens',
        )

    def handle(self, *args, **options):
        usernames = options['usernames']
        delete_token = options['delete_token']
        reset_token = options['reset_token']
        list_token = options['list_tokens']

        if not usernames:
            if list_token:
                for token in Token.objects.all():
                    self._print_token(token)

            return

        users = []
        for username in usernames:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                if list_token:
                    self._print_error(f"{username} does not exist")
                    continue

                user = User(username=username)
                user.save()

            users.append(user)

        if delete_token or reset_token:
            Token.objects.filter(user__in=users).delete()

            if delete_token:
                return

        for user in users:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                if list_token:
                    self._print_error(f"{user.username} has no token")
                    continue

                token = Token(user=user)
                token.save()

            self._print_token(token)

    def _print_token(self, token):
        token64 = base64.b64encode(token.key.encode('ascii')).decode('ascii')

        self.stdout.write(f"{token.user.username}: {token.key} ({token64})")

    def _print_error(self, msg):
        self.stderr.write(msg)
