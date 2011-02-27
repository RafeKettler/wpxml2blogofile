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

from lxml import etree
from os import mkdir
from os.path import join
from datetime import datetime

def setup():
    '''Set up for parsing and conversion.'''
    mkdir("_posts")
    
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
    # Join all unique categories with commas
    categories = ', '.join(set([category.text for category in item.findall("category")]))
    # Make a datetime object from the <pubDate>
    date = datetime.strptime(item.find("{http://wordpress.org/export/1.0/}post_date").text, 
                             "%Y-%m-%d %H:%M:%S")
    guid = item.find("guid").text
    title = item.find("title").text
    permalink = item.find("link").text
    # Write the post
    # Make the post name and file handle
    post = open(join("_posts", "%04d. %s.html" % (post_id, 
                                                  path_title(title))), 'w')
    # Write the yaml
    post.write("---\n")
    post.write("categories: %s\n" % categories)
    post.write("date: %s\n" % date.strftime("%Y/%m/%d %H:%M:%S"))
    post.write("guid: %s\n" % guid)
    post.write("title: %s\n" % title)
    post.write("permalink: %s\n" % permalink)
    post.write("---\n")
    # Write the content
    post.write(item.find("{http://purl.org/rss/1.0/modules/content/}encoded").text)
    post.close()

def path_title(title):
    '''Make a title suitable for paths.'''
    t = re.sub(r'[/!:?\-,\']', '', title.strip().lower().replace(' ', '_'))
    return t

if __name__ == '__main__':
    setup()
    parse()

    
