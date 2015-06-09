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

"""Different utils for JSON handling."""

import base64
import copy
import json
import os.path
import urlparse

from flask import current_app

from jsonpointer import resolve_pointer

import jsonschema


class InsecureSchemaLocation(Exception):

    """The try to load a JSON schema from an insecure location."""

    pass


def json2blob(j):
    """Convert JSON object (dict) into a base64 blob.

    The blob format is the following:

    .. code-block::

        base64 encoded data:
            UTF8 encoded string:
                stringified JSON

    """
    if j:
        return base64.b64encode(json.dumps(j).encode('utf8'))
    else:
        return ""


def blob2json(b):
    """Convert base64 into a JSON object (dict).

    See :func:`json2blob` for an explanation about the blob format.
    """
    s = base64.b64decode(b).decode('utf8').strip()
    if s:
        return json.loads(s)
    else:
        return None


def urljoin(*args):
    """Join parts of a URL together, similar to `os.path.join`."""
    def _add_trailing_slash(s):
        if s.endswith('/'):
            return s
        else:
            return s + '/'

    if len(args) > 1:
        result = reduce(urlparse.urljoin, map(_add_trailing_slash, args[:-1]))
    else:
        result = ''

    if len(args) > 0:
        result = urlparse.urljoin(
            result,
            args[-1]
        )

    return result


def internal_schema_url(*parts):
    """Return the URL to an internal JSON schema."""
    return urljoin(
        current_app.config.get('CFG_SITE_SECURE_URL'),
        current_app.config.get('JSON_SCHEMAPATH', 'jsonschema'),
        *parts
    )


def get_schema(uri):
    """Get and parse a JSON schema from the given URI.

    Internal schemas are loaded from the file system. Caching may apply for
    internal and external schemas. JSON pointers given as fragment of the URI
    are supported.
    """
    # split the fragment
    uri_parsed = urlparse.urlparse(uri)

    # 1. interal resource?
    prefix = current_app.config.get('JSON_SCHEMAPATH', 'jsonschema')

    def calc_interal_path(base):
        """Calculate interal file path based on a `CFG_SITE[_SECURE]_URL`."""
        # FIXME does not work in case of username or password given as part of
        # the uri
        base_parsed = urlparse.urlparse(base)
        if base_parsed.scheme == uri_parsed.scheme \
                and base_parsed.netloc == uri_parsed.netloc \
                and uri_parsed.path.startswith('/' + prefix + '/'):
            return uri_parsed.path.split('/' + prefix + '/', 1)[1]

    interal_path = calc_interal_path(current_app.config.get('CFG_SITE_URL')) \
        or calc_interal_path(current_app.config.get('CFG_SITE_SECURE_URL'))

    if interal_path:
        with open(os.path.join(
                current_app.config.get('COLLECT_STATIC_ROOT'),
                prefix,
                interal_path)
                ) as f:
            return resolve_pointer(
                json.loads(f.read()),
                uri_parsed.fragment
            )

    # 2. external resource
    # FIXME support whitelisting of secure location
    raise InsecureSchemaLocation(
        'Requested schema located on insecure location: ' + uri
    )


def validate_json(json, schema=None, additional_properties=None):
    """Validate JSON against a given schema.

    If no schema is provided, the `$schema` attribute of the JSON object will
    be used. In both cases, schema URIs and parsed schemas are supported.
    """
    # should we get the schema from the JSON itself?
    if not schema:
        schema = json.get('$schema', {})

    # is the schema a link or the parsed schema?
    if isinstance(schema, basestring):
        schema = get_schema(schema)

    # allow additional properties?
    if additional_properties is not None:
        schema['additionalProperties'] = additional_properties

    # remove `$schema`, because jsonschema does not handle or ignore it
    # instead it would result in an validation error
    data = copy.deepcopy(json)
    data.pop('$schema', None)

    jsonschema.validate(data, schema)
    return True
