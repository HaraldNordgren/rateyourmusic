#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, os
from splinter import Browser

reload(sys)
sys.setdefaultencoding('utf-8')

br = Browser()

file_prefix = 'file://'
dir_name    = os.path.dirname(os.path.realpath(__file__))
file_name   = "output.html"

full_path   = file_prefix + dir_name + '/' + file_name

br.visit(full_path)
br.click_link_by_partial_href('/releases/ac?artist_id=')
