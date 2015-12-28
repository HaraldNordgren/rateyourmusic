#!/usr/bin/env python3

import sys, os, re, argparse, urllib, splinter, time, datetime
import credentials
from bs4 import BeautifulSoup

import BandcampEntry, SpotifyEntry


subparser_string    = 'subparser'

add_artist          = 'add-artist'
add_album           = 'add-album'
add_issue           = 'add-issue'
update_album        = 'update-album'

info                = 'info'
cover               = 'cover'


def parse_command_line_args():
    
    parser = argparse.ArgumentParser(description='Add/Update RYM albums from a Bandcamp or Spotify link')

    # Parse Bandcamp or Spotify link
    info_url_group = parser.add_mutually_exclusive_group(required=True)
    info_url_group.add_argument('-u', '--url',         help='Bandcamp URL')
    info_url_group.add_argument('-s', '--spotify-uri', help='Spotify URI')
    
    # Cover art nudity parameter
    parser.add_argument('--nudity', action='store_true')

    # Subparsers for flow control
    subparsers = parser.add_subparsers(dest=subparser_string)

    # Add artist and then album
    add_artist_subparser = subparsers.add_parser(add_artist, help='Add new artist to RYM')

    # Add album to given RYM profile
    add_album_subparser = subparsers.add_parser(add_album, help='Add album to RYM aritst page')
    add_album_subparser.add_argument('-r', '--rym-profile', help='RateYourMusic artist profile URL')

    # Add an issue to given RYM primary issue
    add_issue_subparser = subparsers.add_parser(add_issue, help='Add new issue to RYM album')
    add_issue_subparser.add_argument('-p', '--primary-url', required=True,
            help='RateYourMusic primary issue URL')
    
    # Update RYM album
    update_subparser = subparsers.add_parser(update_album, help='Update RYM album with Bandcamp info')
    update_subparser.add_argument('-a', '--rym-album', required=True)
    
    # Options to update info and/or cover art
    update_subparser.add_argument('--update', nargs='*', type=str,
            choices=[info, cover], default=[])


    args = parser.parse_args()

    if args.url is not None:
        album_entry = BandcampEntry.BandcampEntry(args.url)

    else:
        album_entry = SpotifyEntry.SpotifyEntry(args.spotify_uri)


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


def submit_info(br, album_entry):

    title       = album_entry.title
    tracklist   = album_entry.full_tracklist
    year        = album_entry.year
    month       = album_entry.month
    day         = album_entry.day

    if album_entry.primary_issue:

        br.find_by_id('parent_id').select('other')
        br.find_by_id('parent_shortcut').fill(album_entry.primary_issue)

        br.find_by_id('filed_under_same_as_parent_yes').click()

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

    if 2010 <= int(year) <= datetime.date.today().year:
        release_year_selector   = br.find_by_id('year')
        release_year_selector.select(year)
    
    br.find_by_id('previewbtn').click()
    time.sleep(2)
    
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


def add_artist_to_rym(album_entry):

    br.visit('https://rateyourmusic.com/artist_add')

    br.fill('lastname', album_entry.artist)
    br.fill('comments', album_entry.source)

    br.find_by_id('submitbtn').click()
    time.sleep(3)
    
    # Go to newly created artist page
    br.find_by_text(album_entry.artist).click()

def vote_for_genres(br, album_entry):

    # Go to genre voting page
    br.click_link_by_partial_href('/rgenre/set?')

    for genre in album_entry.genres:

        prigen_text_area = br.find_by_xpath("//input[@id='prigen']")
        prigen_text_area.fill(genre)

        prigen_vote_button = br.find_by_xpath("//input[@value='+ propose']").first
        prigen_vote_button.click()

    # Go back to release
    br.click_link_by_partial_href('/release/')


def add_album_to_rym(args, album_entry):
    
    br = splinter.Browser()
    login(br)

    if get_attribute(args, subparser_string) == update_album:
        
        br.visit(args.rym_album)
        time.sleep(2)
         
        if info in args.update:

            br.find_by_text('Correct this entry').click()    
            submit_info(br, album_entry)
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
            
            add_artist_to_rym(album_entry)
        
        elif get_attribute(args, subparser_string) == add_issue:
               
            br.visit(args.primary_url)
            time.sleep(2)

            album_title_div = br.find_by_xpath("//div[@class='album_title']")
            primary_shortcut_area = album_title_div.find_by_xpath(".//input[@class='album_shortcut']")
            
            album_entry.primary_issue = primary_shortcut_area['value']

            artist_name_box = album_title_div.find_by_xpath(".//a")
            br.visit(artist_name_box['href'])
        
        else:
            
            br.visit(args.rym_profile)
        
        time.sleep(3)

        br.click_link_by_partial_href('/releases/ac?artist_id=')
        submit_info(br, album_entry)
        
        br.click_link_by_partial_href('/images/upload?type=l&assoc_id=')
        upload_cover(br, album_entry)

    time.sleep(3)
    vote_for_genres(br, album_entry)
    
    print("Finished")


if __name__ == "__main__":
    (args, album_entry) = parse_command_line_args()
    add_album_to_rym(args, album_entry)
