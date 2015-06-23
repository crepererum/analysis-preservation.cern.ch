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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# 02D111-1307, USA.

from __future__ import print_function, unicode_literals

from invenio.testsuite import InvenioTestCase, make_test_suite, run_test_suite


class UtilsTest(InvenioTestCase):
    def test_blob(self):
        from invenio_data.modules.jsondeposit.utils import blob2json, json2blob

        json = {
            'key 01': 1,
            'key 02': True,
            'key 03': 1.0,
            'key 04': 'foo',
            'key 05': None,
            'key 06': [1, 2, 3],
            'key 07': {
                'foo': 'bar'
            },
            u'key unicode 👍': u'I enjoyed staying -- באמת! -- at his house.'
        }

        blob = json2blob(json)
        self.assertDictEqual(
            json,
            blob2json(blob),
            'incorrect full serializaion + deserialization'
        )

    def test_urljoin(self):
        from invenio_data.modules.jsondeposit.utils import urljoin

        self.assertEqual(
            urljoin('http://test.org'),
            'http://test.org',
            'touches normal URL'
        )
        self.assertEqual(
            urljoin('http://test.org', 'foo'),
            'http://test.org/foo',
            'cannot do a simple append'
        )
        self.assertEqual(
            urljoin('http://test.org', 'foo/'),
            'http://test.org/foo/',
            'does not respect trailing slash'
        )
        self.assertEqual(
            urljoin('http://test.org/', 'foo'),
            'http://test.org/foo',
            'does not handle trailing slash in first component correctly'
        )
        self.assertEqual(
            urljoin('http://test.org', '/foo'),
            'http://test.org/foo',
            'does not handle leading slash in second component correctly'
        )
        self.assertEqual(
            urljoin('http://test.org/', '/foo'),
            'http://test.org/foo',
            'does not handle trailing + leading slash correctly'
        )
        self.assertEqual(
            urljoin('http://test.org/', 'foo', 'bar'),
            'http://test.org/foo/bar',
            'does not handle 3 components'
        )
        self.assertEqual(
            urljoin('http://test.org/', 'foo', 'bar', 'x', 'y', 'z'),
            'http://test.org/foo/bar/x/y/z',
            'does not handle 6 components'
        )
        self.assertEqual(
            urljoin(),
            '',
            'does not handle zero components'
        )
        self.assertEqual(
            urljoin('http://test.org/', '/foo?p=1'),
            'http://test.org/foo?p=1',
            'does not handle query parameters correctly'
        )
        self.assertEqual(
            urljoin('http://test.org/', '/foo#bar'),
            'http://test.org/foo#bar',
            'does not handle fragments correctly'
        )


TEST_SUITE = make_test_suite(UtilsTest)

if __name__ == '__main__':
    run_test_suite(TEST_SUITE)
