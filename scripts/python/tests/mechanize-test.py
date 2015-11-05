#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

from mechanize import Browser
import mechanize

reload(sys)
sys.setdefaultencoding('utf-8')

br = Browser()

#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Firefox')]

"""
print br._ua_handlers['_cookies'].cookiejar

br.open('https://rateyourmusic.com/account/login')
br.select_form(nr=1)
#print br.form

br.form['username'] = "holograms"
br.form['password'] = "Xds<2718"

#br.open('https://www.reddit.com/')
#br.select_form(nr=1)
#br.form['user'] = "mellowmymints"
#br.form['passwd'] = "Xds<2718"

#print br.form


#response = br.submit(id='login_submit', label="Log in >>")
br.click(type="submit")

print br._ua_handlers['_cookies'].cookiejar

#print response.read()
sys.exit(0)
"""


cookiejar = mechanize.MozillaCookieJar()
cookiejar.load('cookies.txt')
br.set_cookiejar(cookiejar)
print br._ua_handlers['_cookies'].cookiejar

vaporlist = br.open("https://rateyourmusic.com/")
#vaporlist = br.open("http://stackoverflow.com/")
print vaporlist.read()


sys.exit(0)

br.select_form(nr=0)

br.open("http://httpbin.org/forms/post")

br.select_form(nr=0)

br.form['custname'] = "Η Δύναμη 1996-2096"
br.form['comments'] = "https://theforcefuckedyourbitch.bandcamp.com/album/ch-i-m-ep"

#br.form['lastname'] = "Η Δύναμη 1996-2096"
#br.form['comments'] = "https://theforcefuckedyourbitch.bandcamp.com/album/ch-i-m-ep"

response = br.submit()

print response.read()

