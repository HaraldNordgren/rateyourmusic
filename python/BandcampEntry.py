import sys, os, re, urllib
import AlbumEntry

from bs4 import BeautifulSoup


def extract_title_and_artist(string):
    m = re.match('(.*), by (.*)', string)

    if not m:
        raise Exception('Regex did not match')

    title  = m.group(1)
    artist = m.group(2)

    return (title, artist)


def bandcamp_url(url):
    parsed_uri = urllib.parse.urlparse(url)
    domain = parsed_uri.netloc

    domain_components = domain.split('.')
    if (len(domain_components) < 2):
        return False

    two_level_domain = "%s.%s" % (domain_components[-2], domain_components[-1])
    return two_level_domain == "bandcamp.com"


def parse_release_date(release):
    year    = release[0:4]
    month   = release[4:6]
    day     = release[6:8]

    return (year, month, day)


class BandcampEntry(AlbumEntry.AlbumEntry):

    def __init__(self, url):

        if not bandcamp_url(url):
            print("Not a Bandcamp url")
            sys.exit(1)

        req                 = urllib.request.urlopen(url)
        content             = req.read()
        soup                = BeautifulSoup(content, 'html.parser')

        self.source         = url

        title_and_artist = soup.find('meta', attrs={'name':'title'})['content']        
        (self.title, self.artist) = extract_title_and_artist(title_and_artist)
        
        print("Album title:\t%s" % self.title)
        print("Artist:\t\t%s" % self.artist)
        print

        tracknumber_cols = soup.findAll('td', attrs={'class':'track-number-col'})
        title_cols       = soup.findAll('td', attrs={'class':'title-col'})

        self.full_tracklist = ""

        print("Tracklist:")
        for (track_col, title_col) in zip(tracknumber_cols, title_cols):
            track_id = track_col.div.string.replace(".","")

            title_div = title_col.div
            track_title = title_div.a.span.string

            track_duration_span = title_div.find('span', attrs={'class':'time secondaryText'})
            track_duration = track_duration_span.string.strip()
        
            tracklist_string = '%s|%s|%s' % (track_id, track_title, track_duration)
            print(tracklist_string)
            self.full_tracklist += tracklist_string + "\n"

        release = soup.find('meta', attrs={'itemprop':'datePublished'})['content']
        
        (self.year, self.month, self.day) = parse_release_date(release)
        print("\nRelease date: %s-%s-%s" % (self.year, self.month, self.day))
       
        cover_art           = soup.find('link', attrs={'rel':'image_src'})['href']
        self.retrieve_cover_art(cover_art)
