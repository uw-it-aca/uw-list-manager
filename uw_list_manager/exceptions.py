# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Custom exceptions
"""


class ListNotFound(Exception):
    def __str__(self):
        return "List not found"
