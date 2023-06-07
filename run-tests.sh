#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

python -m check_manifest --ignore ".travis-*" && \
python -m pytest && \
tests_exit_code=$?
exit "$tests_exit_code"
