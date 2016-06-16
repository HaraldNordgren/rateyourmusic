import spotipy, AlbumEntry
import pprint

def parse_release_date(release):
    year    = release[0:4]
    month   = release[5:7]
    day     = release[8:10]

    return (year, month, day)


class SpotifyEntry(AlbumEntry.AlbumEntry):

    def __init__(self, uri):
        
        super().__init__()

        # TODO: Test if Spotify URI
        # Maybe also URL and decide dynamically what to do
        
        sp = spotipy.Spotify()
        album = sp.album(uri)

        self.artist         = album['artists'][0]['name']
        self.title          = album['name']

        release = album['release_date']
        (self.year, self.month, self.day) = parse_release_date(release)

        self.full_tracklist = ""

        for t in album['tracks']['items']:

            dur_ms = t['duration_ms']
            dur_s = dur_ms / 1000
            (dur_m, dur_s_final) = divmod(dur_s, 60)
            dur_string = "%d:%d" % (int(dur_m), round(dur_s_final))

            self.full_tracklist += "%s|%s|%s\n" % \
                    (t['track_number'], t['name'], dur_string)
        
        self.correct_capitalization()
        self.detect_bonus_tracks()
        
        cover_art           = album['images'][0]['url']
        self.retrieve_cover_art(cover_art)

        self.source         = album['external_urls']['spotify']
