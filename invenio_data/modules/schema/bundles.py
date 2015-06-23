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
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307,
# USA.

"""Bundles for jsondeposit."""

from __future__ import unicode_literals

import os
import os.path
import re

from flask import current_app

from invenio.base.bundles import invenio as _invenio_js, \
    jquery as _j
from invenio.ext.assets import Bundle, RequireJSFilter

from .filter import JSONOptimize, SchemaAllof

schema_js = Bundle(
    "js/schema/schema.js",
    output='jsonschema.js',
    filters=RequireJSFilter(
        exclude=[_j, _invenio_js],
    ),
    bower={
        'renderjson': 'latest',
    }
)

schema_css = Bundle(
    "less/schema/schema.less",
    output='jsonschema.css',
    filters="less,cleancss",
)


def _gen_bundlename(s, prefix):
    return prefix + re.sub(
        '[^a-z0-9]', '_',
        s.lower()
    )

# optimize all json files
schema_path_collected = os.path.join(
    current_app.static_folder,
    'schema'
)

for root, dirs, files in os.walk(schema_path_collected):
    for name in files:
        path = os.path.join('schema', os.path.relpath(root, schema_path_collected), name)
        bundle_name = _gen_bundlename(path, 'gen_schemaopt_')
        globals()[bundle_name] = Bundle(
            path,
            output=path,
            filters=JSONOptimize()
        )

# auto-generate record schemas
form_schema_path = os.path.join(
    current_app.static_folder,
    'schema',
    'forms'
)
record_schema_path = os.path.join(
    current_app.static_folder,
    'schema',
    'records'
)
if os.path.isdir(form_schema_path):
    if not os.path.exists(record_schema_path):
        os.mkdir(record_schema_path)

    form_schemas = (
        f
        for f in os.listdir(form_schema_path)
        if os.path.isfile(os.path.join(form_schema_path, f)) and
        f.endswith('.json')
    )
    for f in form_schemas:
        bundle_name = _gen_bundlename(f, 'gen_records_')
        source_path = os.path.join(
            'schema',
            'forms',
            f
        )
        base_path = os.path.join(
            'schema',
            'base',
            'record-v1.0.0.json'
        )
        target_path = os.path.join(
            'schema',
            'records',
            f
        )

        globals()[bundle_name] = Bundle(
            source_path,
            base_path,
            output=target_path,
            filters=[SchemaAllof(), JSONOptimize()]
        )
