#!/usr/bin/env python3

import sys, os, re, argparse, urllib
import rym, config
from bs4 import BeautifulSoup

#reload(sys)
#sys.setdefaultencoding('utf-8')

soup        = None
cfg_file    = None
args        = None
album_dir   = None

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
    
    parser = argparse.ArgumentParser(description='Get a RYM tracklist from Bandcamp')
    
    parser.add_argument('-u', '--url', required=True, help='Bandcamp URL')

    artist_group = parser.add_mutually_exclusive_group(required=True)
    artist_group.add_argument('--add-artist', action='store_true', help='Add artist to database also')
    artist_group.add_argument('-r', '--rym-profile', help='RateYourMusic artis profile URL')

    #parser.add_argument('--update-album', nargs='+', type=str, choices=['hej', 'nej'])
    #parser.add_argument('-a', '--rym-album')

    args = parser.parse_args()

    if not bandcamp_url(args.url):
        print("Not a Bandcamp url")
        parser.exit(1)

    #sys.exit(0)

    """
    if args.update_album and args.rym_album is None:
        print("Provide album to be updated!")
        parse.exit(1)
    """

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
    urllib.request.urlretrieve(cover_art, cover_art_file)

    config.write_config(config_file, title, artist, full_tracklist, 
            release, os.path.abspath(cover_art_file))


parse_command_line_args()
parse_tracklist()

rym.add_album_to_rym(args, config_file)
