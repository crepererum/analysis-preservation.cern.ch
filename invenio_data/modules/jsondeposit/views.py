# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2014, 2015 CERN.
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

"""Views for jsondeposit."""

from collections import OrderedDict

import os
import os.path

from flask import Blueprint, current_app, render_template

from flask_breadcrumbs import register_breadcrumb

from invenio.base.i18n import _

from .utils import internal_schema_url


blueprint = Blueprint(
    'data_jsondeposit',
    __name__,
    static_folder='static',
    template_folder='templates',
)


@blueprint.route('/jsonschema', methods=['GET', 'POST'])
@register_breadcrumb(blueprint, '.jsonschema', _('JSON Schema'))
def register():
    json_schema_path = current_app.config.get('JSON_SCHEMAPATH', 'jsonschema')
    schema_path_generated = os.path.join(
        current_app.static_folder,
        'gen',
        json_schema_path
    )

    def _split_path(string):
        result = []
        while string:
            head, tail = os.path.split(string)
            result.insert(0, tail)
            string = head
        return result

    def _tree_insert(tree, path, element):
        if path:
            current = path.pop(0)
            if current not in tree:
                tree[current] = dict()
            _tree_insert(tree[current], path, element)
        else:
            if '.' not in tree:
                tree['.'] = list()
            tree['.'].append(element)

    def _tree_sort(tree):
        result = OrderedDict()
        if '.' in tree:
            sub = tree.pop('.')
            result['.'] = list(sorted(sub, key=lambda e: e['name']))
        for k in sorted(tree.iterkeys()):
            result[k] = _tree_sort(tree[k])
        return result

    tree = dict()
    for root, dirs, files in os.walk(schema_path_generated):
        for name in files:
            path = _split_path(os.path.relpath(root, schema_path_generated))
            _tree_insert(tree, path, {
                'name': name,
                'link': internal_schema_url(*(path + [name]))
            })

    return render_template('jsondeposit/schema.html', tree=_tree_sort(tree))
