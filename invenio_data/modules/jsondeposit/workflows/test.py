# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2015 CERN.
#
# CERN Analysis Preservation Framework is free software; you can
# redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# CERN Analysis Preservation Framework is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307,
# USA.

"""Simple test workflow for JSON-schema based deposits."""

from flask import current_app

from invenio.modules.deposit.types import JsonRecordDeposition

from .. import forms

from invenio.modules.deposit.json_utils import json2blob

__all__ = ['test']


class test(JsonRecordDeposition):

    """Submit a simple test record."""

    name = "JSON Deposition Test"
    name_plural = "JSON Deposition Test"
    group = "JSON Deposition"
    enabled = True
    draft_definitions = {
        'default': forms.TestForm,
    }
