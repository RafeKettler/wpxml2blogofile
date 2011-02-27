## wpxml2blogofile.py ##

A script to convert WP XML dumps (WXR files) to [blogofile](http://www.blogofile.com) posts. The script requires you have Python 2.x installed (I know for a fact that it works with Python 2.7 on Fedora 14) and lxml (probably available through your friendly neighborhoob package manager, if not that then `sudo easy_install lxml`).

## Motivation ##

You're on shared hosting so you can't install SQLAlchemy or python-mysql on your server. You don't want to have to dump your database, install MySQL on your computer, load the database, install SQLAlchemy and python-mysql, and then run wordpress2blogofile.

## Usage ##

Go to your Wordpress admin panel, and go to Tools>>Export. Save the XML file in a convenient place. Then run

    $ python wpxml2blogofile.py [your_wp_xml_dump.xml]

A directory named _posts will be created along with your posts nicely converted. You can then drop that _posts directory straight into whatever folder you have a blogofile site set up in.

## Bugs ##

Don't know of any, but I've hardly tested this script. Please report any if you come across them. Patches and forks are welcome (see the file LICENSE).

Enjoy! 