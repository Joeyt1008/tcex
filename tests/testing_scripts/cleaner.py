#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Delete indicators and groups which have been created for the tests."""

import hashlib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
import validator


def _create_xid(type_, name):
    xid_string = '{}-{}'.format(type_, name)
    hash_object = hashlib.sha256(xid_string.encode('utf-8'))
    return hash_object.hexdigest()


def _delete_groups(tcex):
    batch = tcex.batch(tcex.args.api_default_org, action='Delete')
    groups = validator.get_groups(tcex)
    for group in groups:
        group['xid'] = _create_xid(group['type'], group['name'])
        batch.add_group(group)
    batch.submit_all()


def _delete_indicators(tcex):
    # TODO: implement
    pass
    # tcex.args.api_default_org


def clean(tcex):
    """Delete all indicators and groups in the source."""
    _delete_groups(tcex)
    _delete_indicators(tcex)
