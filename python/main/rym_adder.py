#!/usr/bin/env python3

import sys, os, re, argparse, urllib, splinter, time, datetime, re
import BandcampEntry, SpotifyEntry, credentials

from bs4 import BeautifulSoup
from attribute_strings import *
from RateyourmusicSession import RateyourmusicSession

def parse_command_line_args():
    
    parser = argparse.ArgumentParser(
            description='Add/Update RYM albums from a Bandcamp or Spotify link')

    # Parse Bandcamp or Spotify link
    info_url_group = parser.add_mutually_exclusive_group(required=True)
    info_url_group.add_argument('-u', '--url',         help='Bandcamp URL')
    info_url_group.add_argument('-s', '--spotify-uri', help='Spotify URI')
    
    # Cover art nudity parameter
    parser.add_argument('--nudity', action='store_true')

    # Subparsers for flow control
    subparsers = parser.add_subparsers(dest=subparser_string)

    # Add artist and then album
    add_artist_subparser = subparsers.add_parser(add_artist,
            help='Add new artist to RYM')

    # Add album to given RYM profile
    add_album_subparser = subparsers.add_parser(add_album,
            help='Add album to RYM aritst page')
    add_album_subparser.add_argument('-r', '--rym-profile',
            help='RateYourMusic artist profile URL')

    # Add an issue to given RYM primary issue
    add_issue_subparser = subparsers.add_parser(add_issue,
            help='Add new issue to RYM album')
    add_issue_subparser.add_argument('-p', '--primary-url', required=True,
            help='RateYourMusic primary issue URL')
    
    # Update RYM album
    update_subparser = subparsers.add_parser(update_album,
            help='Update RYM album with Bandcamp info')
    update_subparser.add_argument('-a', '--rym-album', required=True)
    
    # Options to update info and/or cover art
    update_subparser.add_argument('--update', nargs='*', type=str,
            choices=[info], default=[])

    return parser.parse_args()


if __name__ == "__main__":

    args = parse_command_line_args()
    
    if args.url is not None:
        album_entry = BandcampEntry.BandcampEntry(args.url)
    else:
        album_entry = SpotifyEntry.SpotifyEntry(args.spotify_uri)

    rym_session = RateyourmusicSession()
    
    rym_session.add_album_to_rym(args, album_entry)
    rym_session.vote_for_genres(album_entry)
    
    print("\nFinished")
