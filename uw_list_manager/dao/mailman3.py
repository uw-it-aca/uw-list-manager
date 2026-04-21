# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django_mailman3.lib.mailman import get_mailman_client, get_request_hooks
from mailmanclient import Client as MailmanClient
from uw_list_manager.models import ListExists
from urllib.error import HTTPError
import logging


logger = logging.getLogger(__name__)


class Mailman3:
    def __init__(self, *args, **kwargs):
        self._instances = getattr(settings, 'MAILMAN_CLUSTER', {})
        if len(self._instances) > 0:
            self._client = None
        else:
            self._client = get_mailman_client()
            super(Mailman3, self).__init__(*args, **kwargs)

    def get_list_existance_by_name(self, list_name):
        """
        Query mailman3 server for list_id

        Return True if the corresponding mailman list is avaliable
        for the given list name string
        @param list_name: a non_empty string
        """
        mlist = None
        if '@' not in list_name:
            for domain in self._mailman_domains():
                mlist = self._get_list(
                    f"{list_name}@{domain.mail_host}")
                if mlist:
                    break
        else:
            mlist = self._get_list(list_name)

        return ListExists(
            list_name=mlist.fqdn_listname if mlist else list_name,
            exists=mlist is not None,
            admin_url=self._list_admin_url(mlist))

    def _mailman_domains(self):
        if self._client:
            return self._client.domains

        domains = []
        hosts = set()
        for web_host, client in self._instance_mailman_clients():
            try:
                for domain in client.domains:
                    if domain.mail_host not in hosts:
                        domains.append(domain)
                        hosts.add(domain.mail_host)
            except HTTPError as ex:
                logger.error(f"Cannot connect to Mailman API at {web_host}: {ex}")

        return domains

    def _list_admin_url(self, mlist):
        return (f"https://{getattr(mlist, 'web_host', mlist.mail_host)}"
                f"/postorius/lists/{mlist.list_id}/") if (
                    mlist) else ""

    def _get_list(self, list_name):
        if self._client:
            return self._get_list_from_client(list_name)

        return self._get_list_from_cluster(list_name)

    def _get_list_from_client(self, list_name):
        """
        single instance deployment
        """
        try:
            return self._client.get_list(list_name)
        except HTTPError as ex:
            if ex.code == 404:
                return None
            else:
                raise

    def _get_list_from_cluster(self, list_name):
        """
        multiple instances, search for list across all instances
        """
        for web_host, client in self._instance_mailman_clients():
            try:
                mm_list = client.get_list(list_name)
                if mm_list:
                    mm_list.web_host = web_host
                    return mm_list
                # else query next instance
            except HTTPError as ex:
                if ex.code == 404:
                    pass
                else:
                    raise

        return None

    def _instance_mailman_clients(self):
        """
        instantiate a client for each cluster member
        """
        for web_host, instance in self._instances.items():
            api_url = instance.get('api_url')
            api_user = instance.get('api_user')
            api_pass = instance.get('api_pass')

            try:
                logger.debug(f"Connecting {api_url} as {api_user}")
                yield web_host, self._get_mailman_client(
                    api_url, api_user, api_pass)
            except HTTPError as ex:
                logger.error(f"Cannot connect to Mailman API at {api_url}: {ex}")

    def _get_mailman_client(
            self, api_url, api_user, api_pass, api_version='3.1'):
        """ Mailman Client for specific Mailman instance. """
        return MailmanClient(
            f"{api_url}/{api_version}",
            name=api_user, password=api_pass,
            request_hooks=get_request_hooks())

