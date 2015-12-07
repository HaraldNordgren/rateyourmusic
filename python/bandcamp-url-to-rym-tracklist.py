#!/usr/bin/env python3

import sys, os, re, argparse, urllib, splinter, time
import rym, config, credentials
from bs4 import BeautifulSoup


soup        = None
cfg_file    = None
args        = None
album_dir   = None

subparser_string    = 'subparser'
add_artist          = 'add-artist'
add_album           = 'add-album'
update_album        = 'update-album'
info                = 'info'
cover               = 'cover'

def create_if_needed(directory):
    try:
        os.makedirs(directory)
    except OSError:
        pass

def bandcamp_url(url):
    parsed_uri = urllib.parse.urlparse(url)
    domain = parsed_uri.netloc

    domain_components = domain.split('.')
    if (len(domain_components) < 2):
        return False

    two_level_domain = "%s.%s" % (domain_components[-2], domain_components[-1])
    return two_level_domain == "bandcamp.com"


def parse_command_line_args():
    
    global soup, config_file, args, album_dir


    parser = argparse.ArgumentParser(description='Add/Update RYM albums from a Bandcamp link')

    parser.add_argument('-u', '--url', required=True, help='Bandcamp URL')
    parser.add_argument('--nudity', action='store_true')

    subparsers = parser.add_subparsers(dest=subparser_string)

    add_artist_subparser = subparsers.add_parser(add_artist, help='Add new artist to RYM')

    add_album_subparser = subparsers.add_parser(add_album, help='Add album to RYM aritst page')
    add_album_subparser.add_argument('-r', '--rym-profile', help='RateYourMusic artist profile URL')
    
    update_subparser = subparsers.add_parser(update_album, help='Update RYM album with Bandcamp info')
    update_subparser.add_argument('-a', '--rym-album', required=True)
    update_subparser.add_argument('--update', nargs='+', type=str, choices=[info, cover])

    args = parser.parse_args()

    if not bandcamp_url(args.url):
        print("Not a Bandcamp url")
        parser.exit(1)

    req             = urllib.request.urlopen(args.url)
    content         = req.read()
    soup            = BeautifulSoup(content, 'html.parser')
    
    album_dir       = 'data/' + os.path.basename(args.url)
    create_if_needed(album_dir)

    config_file     = album_dir + '/album_data.ini'


def extract_title_and_artist(string):
    m = re.match('(.*), by (.*)', string)

    if not m:
        raise Exception('Regex did not match')

    title = m.group(1)
    artist = m.group(2)

    return (title, artist)

def parse_tracklist():

    title_and_artist = soup.find('meta', attrs={'name':'title'})['content']
    
    (title, artist) = extract_title_and_artist(title_and_artist)
    
    print("Album title:\t%s" % title)
    print("Artist:\t\t%s" % artist)
    print

    tracknumber_cols = soup.findAll('td', attrs={'class':'track-number-col'})
    title_cols       = soup.findAll('td', attrs={'class':'title-col'})

    full_tracklist = ""

    print("Tracklist:")
    for (track_col, title_col) in zip(tracknumber_cols, title_cols):
        track_id = track_col.div.string.replace(".","")

        title_div = title_col.div
        track_title = title_div.a.span.string

        track_duration_span = title_div.find('span', attrs={'class':'time secondaryText'})
        track_duration = track_duration_span.string.strip()
    
        tracklist_string = '%s|%s|%s' % (track_id, track_title, track_duration)
        print(tracklist_string)
        full_tracklist += tracklist_string + "\n"

    release = soup.find('meta', attrs={'itemprop':'datePublished'})['content']
    print("\nRelease date: %s" % release)

    cover_art = soup.find('link', attrs={'rel':'image_src'})['href']
    image_ext = os.path.splitext(cover_art)[1]
    cover_art_file  = album_dir + '/cover_art' + image_ext
    #cover_art_file  = cover_art_file.replace('%', "")
    
    urllib.request.urlretrieve(cover_art, cover_art_file)

    config.write_config(config_file, title, artist, full_tracklist, 
            release, os.path.abspath(cover_art_file))


def parse_release_date(release):
    year    = release[0:4]
    month   = release[4:6]
    day     = release[6:8]

    return (year, month, day)


def get_attribute(obj, string):
    return getattr(obj, string)


def login(br):
    
    br.visit('https://rateyourmusic.com/account/login')
    time.sleep(3)
    
    br.fill('username', credentials.username)
    br.fill('password', credentials.password)
    br.find_by_id('login_submit').click()
    
    time.sleep(5)


def submit_info(br, title, tracklist, release):
    br.fill('title', title)
    
    br.find_by_id('format58').click()

    br.find_by_id('goAdvancedBtn').click()
    tracks_div = br.find_by_id('tracks_adv')
    tracks_text_area = tracks_div.find_by_id('track_advanced')
    tracks_text_area.fill(tracklist) 
    br.find_by_id('goSimpleBtn').click()

    br.fill('notes', args.url)
 
    (year, month, day)      = parse_release_date(release)

    release_month_selector  = br.find_by_id('month')
    release_month_selector.select(month)
    
    release_day_selector    = br.find_by_id('day')
    release_day_selector.select(day)

    if 2005 < int(year) < 2020:
        release_year_selector   = br.find_by_id('year')
        release_year_selector.select(year)
    
    br.find_by_id('previewbtn').click()
    br.find_by_id('submitbtn').click()


def upload_cover(br, cover_art_file, source):

    br.attach_file('upload_file', cover_art_file)

    if args.nudity:
        br.find_by_id('content_nudity').click()

    br.fill('source', source)
    br.find_by_id('uploadbutton').click()
    time.sleep(10)

    br.click_link_by_partial_href('javascript:setStatus')
    br.click_link_by_partial_href('/release/')


def add_album_to_rym(args, config_file):
    (title, artist, tracklist, release, cover_art_file) = config.read_config(config_file)
    
    br = splinter.Browser()
    login(br)

    if get_attribute(args, subparser_string) == update_album:
        
        br.visit(args.rym_album)
        time.sleep(2)
         
        if info in args.update:

            br.find_by_text('Correct this entry').click()    
            submit_info(br, title, tracklist, release)
            time.sleep(2)
            
            br.visit(args.rym_album)
            time.sleep(2)

        if cover in args.update:
            
            br.find_by_text('Upload cover art').click()
            
            upload_cover(br, cover_art_file, args.url)
            time.sleep(2)
            
            br.visit(args.rym_album)
            time.sleep(2)

    else:

        if get_attribute(args, subparser_string) == add_artist:
            br.visit('https://rateyourmusic.com/artist_add')

            br.fill('lastname', artist)
            br.fill('comments', args.url)

            br.find_by_id('submitbtn').click()

            time.sleep(3)
            
            br.find_by_text(artist).click()
        
        else:
            br.visit(args.rym_profile)
        
        time.sleep(3)

        br.click_link_by_partial_href('/releases/ac?artist_id=')
        submit_info(br, title, tracklist, release)
        
        br.click_link_by_partial_href('/images/upload?type=l&assoc_id=')
        upload_cover(br, cover_art_file, args.url)

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


parse_command_line_args()
parse_tracklist()

add_album_to_rym(args, config_file)
