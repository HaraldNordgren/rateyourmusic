#!/usr/bin/env python2

import sys, os, argparse, urllib2, urlparse, re
from bs4 import BeautifulSoup

soup = None

def bandcamp_url(url):
    parsed_uri = urlparse.urlparse(url)
    domain = parsed_uri.netloc

    domain_components = domain.split('.')
    if (len(domain_components) < 2):
        return False

    two_level_domain = "%s.%s" % (domain_components[-2], domain_components[-1])
    return two_level_domain == "bandcamp.com"

def parse_command_line_args():
    parser = argparse.ArgumentParser(description='Get a RYM tracklist from Bandcamp')
    parser.add_argument('-u', '--url')
    parser.add_argument('-d', '--data-file')
    args = parser.parse_args()

    global soup

    if args.url is not None:
        if not bandcamp_url(args.url):
            print "Not a Bandcamp url"
            parser.exit(1)
        
        req     = urllib2.urlopen(args.url)
        content = req.read()
        soup    = BeautifulSoup(content, 'html.parser')

    elif args.data_file is not None:
        with open (args.data_file) as f:
            soup = BeautifulSoup(f, 'html.parser')

    else:
        parser.print_help()
        parser.exit(1)

def extract_title_and_artist(string):
    m = re.match('(.*), by (.*)', string)

    if not m:
        raise Exception('Regex did not match')

    title = m.group(1)
    artist = m.group(2)

    return (title, artist)

def parse_tracklist():

    title_and_artist = soup.find('meta', attrs={'name':'title'})['content']
    (album_title, artist_name) = extract_title_and_artist(title_and_artist)
    
    print "Album title:\t%s" % album_title
    print "Artist:\t\t%s" % artist_name
    print


    tracknumber_cols = soup.findAll('td', attrs={'class':'track-number-col'})
    title_cols       = soup.findAll('td', attrs={'class':'title-col'})

    print "Tracklist:"
    for (track_col, title_col) in zip(tracknumber_cols, title_cols):
        track_id = track_col.div.string.replace(".","")

        title_div = title_col.div
        track_title = title_div.a.span.string

        track_duration_span = title_div.find('span', attrs={'class':'time secondaryText'})
        track_duration = track_duration_span.string.strip()
    
        print '%s|%s|%s' % (track_id, track_title, track_duration)

    release_date = soup.find('meta', attrs={'itemprop':'datePublished'})['content']
    print "\nRelease date: %s" % release_date


reload(sys)
sys.setdefaultencoding('utf-8')

parse_command_line_args()
parse_tracklist()
