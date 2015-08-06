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


from __future__ import unicode_literals

from invenio.base.bundles import invenio as _invenio_js, \
    jquery as _j, \
    styles as _invenio_css
from invenio.ext.assets import Bundle, RequireJSFilter
from invenio.modules.deposit.bundles import js as _deposit_js, \
    styles as _deposit_css

from invenio.modules.deposit.filter import CSSUrlFixer

jsonedit_js = Bundle(
    "js/jsonedit/editor.js",
    filters=RequireJSFilter(),
    bower={
        'fuse.js': 'latest',
        'tv4': 'latest',
        'Sortable': 'latest',
    },
    output='jsoneditor.js'
)

jsonedit_css = Bundle(
    "less/jsonedit/editor.less",
    filters="less,cleancss",
    output='jsoneditor.css'
)
