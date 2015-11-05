#!/usr/bin/env python2

import sys, os
import argparse, urllib2, urlparse

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

def parse_tracklist():

    tracknumber_cols = soup.findAll('td', attrs={'class':'track-number-col'})
    title_cols       = soup.findAll('td', attrs={'class':'title-col'})

    for (track_col, title_col) in zip(tracknumber_cols, title_cols):
        track_id = track_col.div.string.replace(".","")

        title_div = title_col.div
        track_title = title_div.a.span.string

        track_duration_span = title_div.find('span', attrs={'class':'time secondaryText'})
        track_duration = track_duration_span.string.strip()
    
        print '%s|%s|%s' % (track_id, track_title, track_duration)


reload(sys)
sys.setdefaultencoding('utf-8')

parse_command_line_args()
parse_tracklist()
