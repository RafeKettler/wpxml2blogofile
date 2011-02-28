#!/usr/bin/env python

'''wpxml2blogofile.py
Conversion script for changing Wordpress XML dumps to blogofile posts.
Copyright (c) 2011 Rafe Kettler.

MIT licensed, see http://www.github.com/RafeKettler/wpxml2blogofile/LICENSE for
the full license.

Usage: $ python wpxml2blogofile.py [your_wp_xml_dump.xml]
No output means success.
'''

import sys
import re

from os import mkdir
from os.path import join
from datetime import datetime

try:
    from lxml import etree
except ImportError:
    print('''lxml is required for this script. Try installing using
easy_install or your OS's package management system.''')
    exit()


def setup():
    '''Set up for parsing and conversion.'''
    try:
        mkdir("_posts")
    except OSError:
        # Directory already exists
        resp = raw_input("Warning: directory _posts already exists. Write anyway? (y/n)")
        if resp.startswith('n'):
            exit()

def parse():
    '''Parse the XML file in argv[1] and for each post call write_post.'''
    tree = etree.parse(open(sys.argv[1], 'r'))
    post_id = 1
    for item in tree.findall("channel/item"):
        if item.find("{http://wordpress.org/export/1.0/}post_type").text != "post":
            continue
        if item.find("{http://wordpress.org/export/1.0/}status").text != "publish":
            continue
        write_post(item, post_id)
        post_id += 1

def write_post(item, post_id):
    '''Write a post using data from the XML node item with id post_id.'''
    # Set up all the data to write to the file
    # Build categories and tags. Use sets to ensure no dupes
    categories = set()
    tags = set()
    for category in item.findall("category"):
        try:
            if category.attrib['domain'] == 'tag':
                tags.add(category.text)
            elif category.attrib['domain'] == 'category':
                categories.add(category.text)
        except KeyError:
            # Plain category tag with no domain attribute. Ignore it
            pass
    categories_str = ', '.join(categories)
    tags_str = ', '.join(tags)
    # Make a datetime object from the <pubDate>
    raw_date = item.find("{http://wordpress.org/export/1.0/}post_date").text
    date = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
    guid = item.find("guid").text
    title = item.find("title").text
    permalink = item.find("link").text
    # Write the post
    # Make the post name and file handle
    post = open(join("_posts", "%04d. %s.html" % (post_id,
                                                  path_title(title))), 'w')
    # Write the yaml
    post.write("---\n")
    post.write("categories: %s\n" % categories_str)
    post.write("date: %s\n" % date.strftime("%Y/%m/%d %H:%M:%S"))
    post.write("guid: %s\n" % guid)
    post.write("permalink: %s\n" % permalink)
    post.write("title: %s\n" % title)
    post.write("tags: %s\n" % tags_str)
    post.write("---\n")
    # Write the content
    post.write(item.find("{http://purl.org/rss/1.0/modules/content/}encoded").text)
    post.close()

def path_title(title):
    '''Make a title suitable for paths.'''
    title = re.sub(r'[/!:?\-,\']', '', title.strip().lower().replace(' ', '_'))
    return title

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Usage: $ python wpxml2blogofile.py [your_wp_xml_dump.xml]"
        exit()
    setup()
    parse()
