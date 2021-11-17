# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Basic tests."""

from __future__ import absolute_import, print_function

import json

import pytest
from flask import url_for


@pytest.mark.parametrize(
    "app",
    [
        dict(
            endpoint=dict(
                search_as_you_type=dict(
                    text=dict(
                        fields=[
                            {
                                "field": "title_search_as_you_type",
                                "boost": "1"
                            }
                        ],
                        _source=["title", "control_number"],
                    ),
                    text_with_size=dict(
                        fields=[
                            {
                                "field": "title_search_as_you_type",
                                "boost": "1"
                            }
                        ],
                        _source=["title", "control_number"],
                        size=1,
                    ),
                ),
            )
        )
    ],
    indirect=["app"],
)
def test_valid_search_as_you_type(app, db, es, indexed_records):
    """Test VALID record creation request (GET .../records/)."""
    with app.test_client() as client:
        # Valid simple completion search_as_you_type
        res = client.get(
            url_for("invenio_records_rest.recid_search_as_you_type"),
            query_string={"text": "back"},
        )
        assert res.status_code == 200
        data = json.loads(res.get_data(as_text=True))

        assert len(data["text"][0]["options"]) == 2
        options = data["text"][0]["options"]
        assert all("_source" in op for op in options)

        def is_option(d, options):
            """Check if the provided suggestion 'd' exists in the options."""
            return any(
                d == dict((k, op["_source"][k]) for k in d.keys())
                for op in options
            )

        exp1 = {
            "control_number": "1",
            "title": "Back to the Future",
        }

        exp2 = {
            "control_number": "2",
            "title": "Back to the Past",
        }

        assert all(is_option(exp, options) for exp in [exp1, exp2])

        # Valid simple completion search_as_you_type with size
        res = client.get(
            url_for("invenio_records_rest.recid_search_as_you_type"),
            query_string={"text_with_size": "Back"},
        )
        data = json.loads(res.get_data(as_text=True))
        assert len(data["text_with_size"][0]["options"]) == 1
        assert is_option(exp1, data["text_with_size"][0]["options"])

        # Valid simple completion search_as_you_type with size
        res = client.get(
            url_for("invenio_records_rest.recid_search_as_you_type"),
            query_string={"text_with_size": "Back", "size": 2},
        )
        data = json.loads(res.get_data(as_text=True))
        assert len(data["text_with_size"][0]["options"]) == 2
        assert is_option(exp1, data["text_with_size"][0]["options"])

        # Missing  and invalid search_as_you_type
        res = client.get(
            url_for("invenio_records_rest.recid_search_as_you_type"),
            query_string={"invalid": "Back"},
        )
        assert res.status_code == 400
