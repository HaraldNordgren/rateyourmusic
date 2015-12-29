import os, urllib, imghdr

def create_if_needed(directory):

    if not os.path.isdir(directory):
        os.makedirs(directory)

def download_cover_art(cover_art, album_entry, rateyourmusic_original=False):

    folder = 'cover_art'
    create_if_needed(folder)

    tmp_file = folder + '/' + album_entry.title.replace(' ', '_')
    
    if rateyourmusic_original:
        tmp_file += "_rym"

    urllib.request.urlretrieve(cover_art, tmp_file)

    image_ext = imghdr.what(tmp_file)

    cover_art_file = os.path.abspath(tmp_file + "." + image_ext)
    os.rename(tmp_file, cover_art_file)

    return cover_art_file
