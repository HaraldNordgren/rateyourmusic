#!/usr/bin/env python3

import spotipy

sp = spotipy.Spotify()

album = sp.album('spotify:album:18Zt1YUA1XpTPUdNnctCZ4')

images = album['images']
print(images[0]['url'])

print(album['release_date'])

for t in album['tracks']['items']:
    #print(t)

    dur_ms = t['duration_ms']
    dur_s = dur_ms / 1000
    (dur_m, dur_s_final) = divmod(dur_s, 60)
    dur_string = "%d:%d" % (int(dur_m), round(dur_s_final))

    rym_line = "%s|%s|%s" % (t['track_number'], t['name'], dur_string)
    
    print(rym_line)
    #print()


"""
results = sp.search(q='weezer', limit=20)
for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])
"""
