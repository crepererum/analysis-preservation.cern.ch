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

import json
import os
import os.path

from flask import current_app

from webassets.filter import Filter
from webassets.filter.cssrewrite.base import PatternRewriter, urltag_re

from .utils import internal_schema_url


__all__ = (
    'CSSUrlFixer',
    'JSONOptimize',
    'SchemaAllof',
)


# Helper class as a workaround for the strange cleancss URL handling
class CSSUrlFixer(PatternRewriter):

    """Helper to fix `url(...)` entries in CSS files."""

    patterns = {
        'rewrite_url': urltag_re
    }

    def __init__(self, subpath):
        """Create new CSSUrlFixer.

        :param subpath: relative subpath to the site URL, where all resources
            are located.
        """
        self.subpath = subpath
        super(CSSUrlFixer, self).__init__()

    def rewrite_url(self, m):
        """Rewrite found URL pattern."""
        # Get the regex matches; note how we maintain the exact
        # whitespace around the actual url; we'll indeed only
        # replace the url itself.
        text_before = m.groups()[0]
        url = m.groups()[1]
        text_after = m.groups()[2]

        # Normalize the url: remove quotes
        quotes_used = ''
        if url[:1] in '"\'':
            quotes_used = url[:1]
            url = url[1:]
        if url[-1:] in '"\'':
            url = url[:-1]

        url = self.replace_url(url) or url

        result = 'url(%s%s%s%s%s)' % (
            text_before, quotes_used, url, quotes_used, text_after)
        return result

    def replace_url(self, url):
        """Replace given URL with a new one."""
        return "{}/{}/{}".format(
            current_app.config.get('CFG_SITE_URL'),
            self.subpath,
            url
        )


class JSONOptimize(Filter):

    name = 'json_optimize'

    def output(self, _in, out, **kwargs):
        j = json.loads(_in.read())
        out.write(
            json.dumps(
                j,
                separators=(',', ':')
            )
        )


class SchemaAllof(Filter):

    """Combine multiple JSON schemas using `allOf`."""

    name = 'schema_allof'

    def input(self, _in, out, **kwargs):
        """Input filter, that transforms schemas into their URLs."""
        schema = kwargs['source_path']

        out.write('{"$ref":"')
        out.write(internal_schema_url(
            os.path.relpath(
                schema,
                os.path.join(
                    current_app.static_folder,
                    current_app.config.get('JSON_SCHEMAPATH', 'jsonschema')
                )
            )
        ))
        out.write('"},')

    def output(self, _in, out, **kwargs):
        """Output filter, that does the boilerplate."""
        out.write('{')
        out.write('"allOf": [')

        s = _in.read()
        if s.endswith(','):
            s = s[:-1]
        out.write(s)

        out.write(']')
        out.write('}')
