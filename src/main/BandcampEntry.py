import sys, os, re, urllib
import AlbumEntry, genres

from bs4 import BeautifulSoup
from states import US_states


def bandcamp_url(url):
    parsed_uri = urllib.parse.urlparse(url)
    domain = parsed_uri.netloc

    domain_components = domain.split('.')
    if (len(domain_components) < 2):
        return False

    two_level_domain = "%s.%s" % (domain_components[-2], domain_components[-1])
    return two_level_domain == "bandcamp.com"


class BandcampEntry(AlbumEntry.AlbumEntry):
    
    def parse_release_date(self, release):

        self.year    = release[0:4]
        self.month   = release[4:6]
        self.day     = release[6:8]

    def extract_title_and_artist(self, title_artist_string):

        m = re.match('(.*), by (.*)', title_artist_string)

        if not m:
            raise Exception('Title-artist regex did not match')

        self.title  = m.group(1)
        self.artist = m.group(2)

    def parse_genres(self, tags):

        for tag in tags:

            if tag in genres.genre_map.values() or tag in genres.genre_list:
                self.genres.add(tag)

            elif tag in genres.genre_map:
                self.genres.add(genres.genre_map[tag])

    def extract_location(self, secondary_text):

        match = re.match('(.*), (.*)', secondary_text)

        if match:

            first_component = match.group(1)
            second_component = match.group(2)

            print("location:\t" + first_component + ", " + second_component) 

    def __init__(self, url):

        super().__init__()

        if not bandcamp_url(url):
            print('"%s" is not a Bandcamp url' % url)
            sys.exit(1)
        
        self.source     = url
        self.sitename   = "Bandcamp website"
        
        content         = urllib.request.urlopen(url).read()
        soup            = BeautifulSoup(content, 'html.parser')

        if soup.find('li', attrs={'class':'buyItem'}) is not None:
            self.lossless = True

        tags = soup.findAll('a', attrs={'class':'tag'})
        self.parse_genres(tag.getText().lower() for tag in tags)

        title_and_artist = soup.find('meta', attrs={'name':'title'})['content']
        self.extract_title_and_artist(title_and_artist)

        band_name_location = soup.find('p', attrs={'id': 'band-name-location'})
        band_name_location_title = \
                band_name_location.find('span', attrs={'class': 'title'})

        if band_name_location_title.getText() == self.artist:
            
            secondary_text = band_name_location.find('span',
                    attrs={'class': 'location secondaryText'}).getText()
            
            if secondary_text:
                self.extract_location(secondary_text)


        tracknumber_cols = soup.\
                findAll('td', attrs={'class':'track-number-col'})
        title_cols       = soup.findAll('td', attrs={'class':'title-col'})

        self.full_tracklist = ""

        for (track_col, title_col) in zip(tracknumber_cols, title_cols):

            track_id            = track_col.div.string.replace(".","")

            title_div           = title_col.div
            track_title         = title_div.a.span.string

            track_duration_span = title_div.\
                    find('span', attrs={'class':'time secondaryText'})
            track_duration      = track_duration_span.string.strip()
        
            tracklist_string    = '%s|%s|%s' % \
                    (track_id, track_title, track_duration)
            self.full_tracklist += tracklist_string + "\n"

        self.correct_capitalization()
        self.detect_bonus_tracks()

        release = soup.\
                find('meta', attrs={'itemprop':'datePublished'})['content']
        self.parse_release_date(release)
        
        cover_art = soup.find('link', attrs={'rel':'image_src'})['href']
        self.retrieve_cover_art(cover_art)

        self.print_info()
