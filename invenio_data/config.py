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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# 02D111-1307, USA.

from invenio.base.config import PACKAGES as _PACKAGES, PACKAGES_EXCLUDE as _PACKAGES_EXCLUDE
from invenio.modules.oauthclient.contrib import cern

PACKAGES = [
    "invenio_data.base",
    "invenio_data.modules.*",
] + _PACKAGES

PACKAGES_EXCLUDE = [
    "invenio_annotations",
    "invenio_comments",
] + _PACKAGES_EXCLUDE

DEPOSIT_TYPES = [
    'invenio_data.modules.deposit.workflows.cms.cms',
    'invenio_data.modules.deposit.workflows.alice.alice',
    'invenio_data.modules.deposit.workflows.lhcb.lhcb',
    'invenio_data.modules.deposit.workflows.questions.questions',
    'invenio_data.modules.jsondeposit.workflows.test.test',
]

CFG_SITE_URL = 'http://data-demo.cern.ch'
CFG_SITE_SECURE_URL = 'https://data-demo.cern.ch'

CFG_SITE_LANGS = ["en", "fr"]

CFG_SITE_NAME = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL = {}
CFG_SITE_NAME_INTL['en'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['fr'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['de'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['es'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['ca'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['pt'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['it'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['ru'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['sk'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['cs'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['no'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['sv'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['el'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['uk'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['ja'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['pl'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['bg'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['hr'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['zh_CN'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['zh_TW'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['hu'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['af'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['gl'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['ro'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['rw'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['ka'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['lt'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['ar'] = 'CERN Analysis Preservation'
CFG_SITE_NAME_INTL['fa'] = 'CERN Analysis Preservation'

CFG_SITE_MISSION = 'Analysis Preservation for LHC experiments, CERN Lab experiments and other institutions (demo)'
CFG_SITE_MISSION_INTL = {
    'en': 'Analysis Preservation for LHC experiments, CERN Lab experiments and other institutions (demo)',
}

CFG_WEBSEARCH_DISPLAY_NEAREST_TERMS = 0

OAUTHCLIENT_REMOTE_APPS = dict(
    cern=cern.REMOTE_APP,
)

CERN_APP_CREDENTIALS = dict(
    consumer_key="changeme",
    consumer_secret="changeme",
)

JSONSCHEMAS_BASE_SCHEMA = 'base/record-v1.0.0.json'
