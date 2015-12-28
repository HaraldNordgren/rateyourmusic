import os, urllib, imghdr

def create_if_needed(directory):
    try:
        os.makedirs(directory)
    except OSError:
        pass



class AlbumEntry:

    def __init__(self):
        self.primary_issue = None

    def retrieve_cover_art(self, cover_art):

        folder = 'cover_art'
        create_if_needed(folder)

        tmp_file = folder + '/' + self.title.replace(' ', '_')
        urllib.request.urlretrieve(cover_art, tmp_file)

        image_ext = imghdr.what(tmp_file)

        self.cover_art_file = os.path.abspath(tmp_file + "." + image_ext)
        os.rename(tmp_file, self.cover_art_file)
