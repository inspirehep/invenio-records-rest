# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Permissions tests."""

from __future__ import absolute_import, print_function

import json

from helpers import record_url


def test_default_permissions(
    app,
    default_permissions,
    test_data,
    search_url,
    test_records,
    indexed_records
):
    """Test default create permissions."""
    pid, _ = test_records[0]
    rec_url = record_url(pid)
    data = json.dumps(test_data[0])
    headers = {"Content-Type": "application/json"}
    headers_with_json_patch = {"Content-Type": "application/json-patch+json"}

    with app.test_client() as client:
        args = dict(data=data, headers=headers)
        args_with_json_patch_headers = dict(
            data=data, headers=headers_with_json_patch
        )

        assert client.get(search_url).status_code == 200
        assert client.get(rec_url).status_code == 200

        assert 401 == client.post(search_url, **args).status_code
        assert 405 == client.put(search_url, **args).status_code
        assert 405 == client.patch(search_url).status_code
        assert 405 == client.delete(search_url).status_code

        assert 405 == client.post(rec_url, **args).status_code
        assert 401 == client.put(rec_url, **args).status_code
        assert 401 == client.patch(
            rec_url, **args_with_json_patch_headers
        ).status_code
        assert 401 == client.delete(rec_url).status_code


def test_default_permissions_with_logged_inuser(
    app,
    default_permissions,
    test_data,
    search_url,
    test_records,
    indexed_records
):
    """Test default create permissions."""
    pid, _ = test_records[0]
    rec_url = record_url(pid)
    data = json.dumps(test_data[0])
    headers = {"Content-Type": "application/json"}
    headers_with_json_patch = {"Content-Type": "application/json-patch+json"}

    with app.test_client() as client:
        query_str = {"user": "1"}
        args = dict(data=data, headers=headers, query_string=query_str)
        args_with_json_patch_headers = dict(
            data=data, headers=headers_with_json_patch,
            query_string=query_str
        )

        assert 403 == client.post(search_url, **args).status_code
        assert 403 == client.put(rec_url, **args).status_code
        assert 403 == client.patch(
            rec_url, **args_with_json_patch_headers
        ).status_code
        assert 403 == client.delete(
            rec_url, query_string=query_str
        ).status_code
