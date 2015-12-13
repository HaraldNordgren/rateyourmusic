#!/usr/bin/env python3

import spotipy, pprint

#s = SpotifyEntry.SpotifyEntry('spotify:album:18Zt1YUA1XpTPUdNnctCZ4')

sp = spotipy.Spotify()
album = sp.album('spotify:album:18Zt1YUA1XpTPUdNnctCZ4')

pprint.pprint(album)
