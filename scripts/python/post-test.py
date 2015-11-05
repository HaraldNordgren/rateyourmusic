#!/usr/bin/env python2

import urllib
import urllib2

url = 'http://requestb.in/x1lr1rx1'
values = {'custname' : 'Harald'}

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req) 
the_page = response.read()
