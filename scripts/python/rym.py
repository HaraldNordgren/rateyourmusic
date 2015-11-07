# -*- coding: utf-8 -*-

import sys, config, time, importlib, credentials
from splinter import Browser

#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

def parse_release_date(release):
    year    = release[0:4]
    month   = release[4:6]
    day     = release[6:8]

    return (year, month, day)

def add_album_to_rym(args, config_file):
    br = Browser()

    br.visit('https://rateyourmusic.com/account/login')
    time.sleep(3)

    # Login
    br.fill('username', credentials.username)
    br.fill('password', credentials.password)
    br.find_by_id('login_submit').click()
    time.sleep(5)

    (title, artist, tracklist, release, cover) = config.read_config(config_file)
   

    """
    if args.update_album:

        br.visit(args.rym_album)

    else:
    """

    if args.add_artist:
        br.visit('https://rateyourmusic.com/artist_add')

        #br.fill('lastname', unicode(artist))
        br.fill('lastname', artist)
        br.fill('comments', args.url)

        br.find_by_id('submitbtn').click()

        time.sleep(3)
        
        br.find_by_text(artist).click()
    
    else:
        br.visit(args.rym_profile)
    
    time.sleep(3)
    
    br.click_link_by_partial_href('/releases/ac?artist_id=')
    
    # Add data
    #br.fill('title', unicode(title))
    br.fill('title', title)
    
    br.find_by_id('format58').click()

    br.find_by_id('goAdvancedBtn').click()
    tracks_div = br.find_by_id('tracks_adv')
    tracks_text_area = tracks_div.find_by_id('track_advanced')
    #tracks_text_area.fill(unicode(tracklist)) 
    tracks_text_area.fill(tracklist) 
    br.find_by_id('goSimpleBtn').click()

    br.fill('notes', args.url)
 
    (year, month, day)      = parse_release_date(release)

    release_month_selector  = br.find_by_id('month')
    release_month_selector.select(month)
    
    release_day_selector    = br.find_by_id('day')
    release_day_selector.select(day)
    
    release_year_selector   = br.find_by_id('year')
    release_year_selector.select(year)

    br.find_by_id('previewbtn').click()
    br.find_by_id('submitbtn').click()

    # Add cover art

    """
    coverart_img_element = br.find_by_xpath("//img[@class='coverart_img']")
    print(coverart_im_element)
    sys.exit(0)
    """

    br.click_link_by_partial_href('/images/upload?type=l&assoc_id=')
    br.attach_file('upload_file', cover)

    br.fill('source', args.url)
    br.find_by_id('uploadbutton').click()
    time.sleep(5)

    br.click_link_by_partial_href('javascript:setStatus')


    # Vote for genre
    br.click_link_by_partial_href('/release/')
    time.sleep(3)

    br.click_link_by_partial_href('/rgenre/set?')

    prigen_text_area = br.find_by_xpath("//input[@id='prigen']")
    prigen_text_area.fill('vaporwave')

    prigen_vote_button = br.find_by_xpath("//input[@value='+ propose']").first
    prigen_vote_button.click()

    # Done
    br.click_link_by_partial_href('/release/')
    print("Finished")
