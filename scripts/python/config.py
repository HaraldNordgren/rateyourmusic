#!/usr/bin/env python2

from ConfigParser import SafeConfigParser

b = 'bandcamp'

def read_config(filename):
    cfg = SafeConfigParser()
    cfg.read(filename)

    title       = cfg.get(b, 'title')
    artist      = cfg.get(b, 'artist')
    tracklist   = cfg.get(b, 'tracklist')
    release     = cfg.get(b, 'release')
    cover       = cfg.get(b, 'cover')

    return (title, artist, tracklist, release, cover)


def write_config(filename, title, artist, tracklist, release, cover):
    cfg = SafeConfigParser()
    cfg.add_section(b)

    cfg.set(b, 'title', title)
    cfg.set(b, 'artist', artist)
    cfg.set(b, 'tracklist', tracklist)
    cfg.set(b, 'release', release)
    cfg.set(b, 'cover', cover)

    with open(filename, 'w') as f:
        cfg.write(f)
