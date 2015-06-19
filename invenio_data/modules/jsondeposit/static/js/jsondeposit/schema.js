/**
 * This file is part of CERN Analysis Preservation Framework.
 * Copyright (C) 2015 CERN.
 *
 * CERN Analysis Preservation Framework is free software; you can
 * redistribute it and/or modify it under the terms of the GNU General
 * Public License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * CERN Analysis Preservation Framework is distributed in the hope that
 * it will be useful, but WITHOUT ANY WARRANTY; without even the
 * implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
 * PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307,
 * USA.
 */

// use a renderjson placeholder, because AMD does not seem to work here
require(['jquery', 'renderjson'], function($, _renderjson) {
  'use strict';

  $(function() {
    function update() {
        if (location.hash.startsWith('#') && location.hash.length > 1) {
            var url = location.hash.substring(1);

            // security check
            if (url.startsWith(location.origin)) {
                jQuery.getJSON(url, function(data) {
                    var target = $('#jsonschema-detailed');

                    // set new detailed view
                    target.empty();

                    var rawlink_url = url;
                    if (rawlink_url.startsWith(location.origin)) {
                        rawlink_url = rawlink_url.replace(location.origin + '/gen/jsonschema/', '');
                    }

                    var rawlink = $('<a>');
                    rawlink.attr('href', url);
                    rawlink.text('Schema: ' + rawlink_url);
                    rawlink.addClass('rawlink');
                    target.append(rawlink);

                    renderjson.set_show_to_level(3);
                    target.append(renderjson(data));

                    // link all refs
                    $('.key', target).each(function() {
                        var element = this;

                        // test if the key is "$ref"
                        if ($(element).text() == '"$ref"') {
                            // now search the first '.string' element after
                            // the key element, on the same tree level
                            // (i.e. a sibling)
                            var parent = $(element).parent();
                            var siblings = $(parent).children();
                            var seen = false;
                            for (var i = 0; i < siblings.length; ++i) {
                                var sibling = siblings[i];
                                if (seen) {
                                    if ($(sibling).hasClass('string')) {
                                        // store text and empty node
                                        var txt = $(sibling).text();
                                        $(sibling).empty();

                                        // strip quotes
                                        var url = txt.substring(1, txt.length - 1);

                                        // create link element
                                        var a = $('<a>');
                                        a.attr('href', '#' + url);
                                        a.text(txt);

                                        // add link to element
                                        $(sibling).append(a);

                                        // done
                                        break;
                                    }
                                } else {
                                    if (sibling == element) {
                                        seen = true;
                                    }
                                }
                            }
                        }
                    });

                    // mark active link
                    $('.jsonschema-link').removeClass('active');
                    $(document.getElementById('link-' + url)).addClass('active');
                });
            }
        }
    }

    $(window).bind('hashchange', update);
    update();
  });
})
