import re, images

class AlbumEntry:

    def __init__(self):

        self.primary_issue  = None
        self.genres         = set()
        self.lossless       = False
        self.bonus_tracks   = False

    def retrieve_cover_art(self, cover_art):

        self.cover_art_file = images.download_cover_art(cover_art, self)
    
    def print_info(self):

        print("\nGETTING ALBUM DATA FROM %s:\n" % self.sitename.upper())
        
        print("Album title:\t%s" % self.title)
        print("Artist:\t\t%s" % self.artist)
        print("Release date:\t%s-%s-%s\n" % (self.year, self.month, self.day))
        
        print("Tracklist:")
        print(self.full_tracklist)

        if len(self.genres) > 0:
            print("Genres:")
            
            for g in self.genres:
                print(g)

    def correct_capitalization(self):

        words = [ 'A', 'An', 'And', 'At', 'But', 'By', 'For',
                  'In', 'Nor', 'On', 'Or', 'The', 'To' ]

        for word in words:

            pattern = ' ' + word + '(?= )'
            repl    = ' ' + word.lower()

            self.title          = re.sub(pattern, repl, self.title)
            self.full_tracklist = re.sub(pattern, repl, self.full_tracklist)

    """
    def has_bonus_tracks(self):

        regex = '\((.* )?bonus( .*)?\)\|'
        return bool(re.search(regex, self.full_tracklist, re.IGNORECASE))
    """

    def detect_bonus_tracks(self):

        regex = '\((.* )?bonus( .*)?\)\|'
        self.bonus_tracks = \
                bool(re.search(regex, self.full_tracklist, re.IGNORECASE))
