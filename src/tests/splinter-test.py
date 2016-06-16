#!/usr/bin/env python3

from main import add_rym_info

br = splinter.Browser()
br.visit('https://rateyourmusic.com/release/album/%E9%AA%A8%E6%9E%B6%E7%9A%84/skeleton/')

#primary_shortcut_area = br.find_by_xpath("//album_title/album_shortcut")
#print(primary_shortcut_area)
#print(primary_shortcut_area.value)
