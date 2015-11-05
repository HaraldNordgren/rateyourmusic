#!/usr/bin/env python2

import sys, os
import urllib2, codecs

if len(sys.argv) != 2:
    print "Usage: %s <url>" % os.path.basename(sys.argv[0])
    sys.exit(1)

url                 = sys.argv[1]

url_basename        = os.path.basename(url)
url_no_extension    = os.path.splitext(url_basename)[0]

html_folder         = "html-files"
html_file           = "%s/%s.html" % (html_folder, url_no_extension)

req                 = urllib2.urlopen(url)
content             = req.read()

#print content

print req.headers['content-type']

with open(html_file, "w") as f:
    f.write(content)
