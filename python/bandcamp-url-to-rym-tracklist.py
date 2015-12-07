#!/usr/bin/env python3

import sys, os, re, argparse, urllib, splinter, time
import rym, config, credentials
from bs4 import BeautifulSoup

import BandcampEntry, SpotifyEntry


subparser_string    = 'subparser'
add_artist          = 'add-artist'
add_album           = 'add-album'
update_album        = 'update-album'
info                = 'info'
cover               = 'cover'


def parse_command_line_args():
    
    parser = argparse.ArgumentParser(description='Add/Update RYM albums from a Bandcamp/Spotify link')

    parser.add_argument('-u', '--url', help='Bandcamp URL')
    parser.add_argument('-s', '--spotify-uri', help='Spotify URI')
    
    parser.add_argument('--nudity', action='store_true')

    subparsers = parser.add_subparsers(dest=subparser_string)

    add_artist_subparser = subparsers.add_parser(add_artist, help='Add new artist to RYM')

    add_album_subparser = subparsers.add_parser(add_album, help='Add album to RYM aritst page')
    add_album_subparser.add_argument('-r', '--rym-profile', help='RateYourMusic artist profile URL')
    
    update_subparser = subparsers.add_parser(update_album, help='Update RYM album with Bandcamp info')
    update_subparser.add_argument('-a', '--rym-album', required=True)
    update_subparser.add_argument('--update', nargs='+', type=str, choices=[info, cover])

    args = parser.parse_args()

    if args.url is not None:
        album_entry = BandcampEntry.BandcampEntry(args.url)
    
    elif args.spotify_uri is not None:
        album_entry = SpotifyEntry.SpotifyEntry(args.spotify_uri)

    else:
        sys.exit(1)


    return (args, album_entry)


def get_attribute(obj, string):
    
    return getattr(obj, string)


def login(br):
    
    br.visit('https://rateyourmusic.com/account/login')
    time.sleep(3)
    
    br.fill('username', credentials.username)
    br.fill('password', credentials.password)
    br.find_by_id('login_submit').click()
    
    time.sleep(5)


def submit_info(br, title, tracklist, year, month, day):
    br.fill('title', title)
    
    br.find_by_id('format58').click()

    br.find_by_id('goAdvancedBtn').click()
    tracks_div = br.find_by_id('tracks_adv')
    tracks_text_area = tracks_div.find_by_id('track_advanced')
    tracks_text_area.fill(tracklist) 
    br.find_by_id('goSimpleBtn').click()

    br.fill('notes', album_entry.source)
 
    release_month_selector  = br.find_by_id('month')
    release_month_selector.select(month)
    
    release_day_selector    = br.find_by_id('day')
    release_day_selector.select(day)

    if 2005 < int(year) < 2020:
        release_year_selector   = br.find_by_id('year')
        release_year_selector.select(year)
    
    br.find_by_id('previewbtn').click()
    br.find_by_id('submitbtn').click()


def upload_cover(br, album_entry):

    print(album_entry.cover_art_file)
    br.attach_file('upload_file', album_entry.cover_art_file)

    if args.nudity:
        br.find_by_id('content_nudity').click()

    br.fill('source', album_entry.source)
    br.find_by_id('uploadbutton').click()
    time.sleep(10)

    br.click_link_by_partial_href('javascript:setStatus')
    br.click_link_by_partial_href('/release/')


def add_album_to_rym(args, album_entry):
    
    br = splinter.Browser()
    login(br)

    if get_attribute(args, subparser_string) == update_album:
        
        br.visit(args.rym_album)
        time.sleep(2)
         
        if info in args.update:

            br.find_by_text('Correct this entry').click()    
            submit_info(br, album_entry.title, album_entry.tracklist, 
                    album_entry.year, album_entry.month, album_entry.day)
            time.sleep(2)
            
            br.visit(args.rym_album)
            time.sleep(2)

        if cover in args.update:
            
            br.find_by_text('Upload cover art').click()
            
            upload_cover(br, album_entry)
            time.sleep(2)
            
            br.visit(args.rym_album)
            time.sleep(2)

    else:

        if get_attribute(args, subparser_string) == add_artist:
            br.visit('https://rateyourmusic.com/artist_add')

            br.fill('lastname', album_entry.artist)
            br.fill('comments', album_entry.source)

            br.find_by_id('submitbtn').click()

            time.sleep(3)
            
            br.find_by_text(album_entry.artist).click()
        
        else:
            br.visit(args.rym_profile)
        
        time.sleep(3)

        br.click_link_by_partial_href('/releases/ac?artist_id=')
        submit_info(br, album_entry.title, album_entry.full_tracklist, 
                album_entry.year, album_entry.month, album_entry.day)
        
        br.click_link_by_partial_href('/images/upload?type=l&assoc_id=')
        upload_cover(br, album_entry)

    # Vote for genre
    time.sleep(3)

    br.click_link_by_partial_href('/rgenre/set?')

    prigen_text_area = br.find_by_xpath("//input[@id='prigen']")
    prigen_text_area.fill('vaporwave')

    prigen_vote_button = br.find_by_xpath("//input[@value='+ propose']").first
    prigen_vote_button.click()

    # Done
    br.click_link_by_partial_href('/release/')
    print("Finished")


(args, album_entry) = parse_command_line_args()
add_album_to_rym(args, album_entry)
