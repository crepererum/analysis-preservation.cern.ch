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

"""Special fields for JSON-schema based deposits."""

from invenio.ext.template import render_template_to_string
from invenio.modules.deposit.field_base import WebDepositField

import jsonschema

import wtforms.validators
from wtforms.widgets import HTMLString

from .utils import blob2json, json2blob, validate_json

__all__ = ['JsonField']


def validate_schema(_form, field):
    """Check if submitted data is valid according to field schema."""
    try:
        # trust the schema stored in the field instead the one stored in the
        # json itself (`json['$schema']`)
        validate_json(
            json=field.data,
            schema=field.schema,
            additional_properties=False
        )
    except jsonschema.ValidationError as e:
        raise wtforms.validators.ValidationError(e.message)


class JsonWidget(object):

    """Widget for auto-generated schema-based forms.

    Should be used with a field that provides a `schema` attribute, which is
    an URI to a JSON-schema.
    """

    def __call__(self, field, **kwargs):
        template = 'jsondeposit/jsonwidget.html'
        field_id = kwargs.pop('id', field.id)

        return HTMLString(
            render_template_to_string(
                template,
                field=field,
                field_id=field_id,
                **kwargs
            )
        )


class JsonField(WebDepositField):

    """Field that provides an auto-generated form based on a schema."""

    def __init__(self, **kwargs):
        """Set up new `JsonField`.

        :param schema: URI to JSON-schema
        """
        self.schema = kwargs.pop('schema')

        defaults = dict(
            validators=[validate_schema],
            widget_classes='form-control',
            widget=JsonWidget()
        )
        defaults.update(kwargs)

        super(JsonField, self).__init__(**defaults)

    def process_formdata(self, valuelist):
        """Transform frontend JSON-blob into internal JSON object (dict)."""
        if valuelist:
            self.blob = valuelist[0]
        else:
            self.data = None

    @property
    def blob(self):
        """Get JSON data as base64 blob."""
        return json2blob(self.data)

    @blob.setter
    def blob(self, b):
        """Set JSON data from base64 blob."""
        self.data = blob2json(b)
        self.data['$schema'] = self.schema
