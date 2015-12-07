import os, urllib, imghdr

def create_if_needed(directory):
    try:
        os.makedirs(directory)
    except OSError:
        pass



class AlbumEntry: 

    def retrieve_cover_art(self, cover_art):

        folder = 'cover_art'
        create_if_needed(folder)

        tmp_file = folder + '/' + self.title.replace(' ', '_')
        urllib.request.urlretrieve(cover_art, tmp_file)

        image_ext = imghdr.what(tmp_file)

        #if image_ext == 'jpeg':
        #    image_ext = 'jpg'

        self.cover_art_file = os.path.abspath(tmp_file + "." + image_ext)
        os.rename(tmp_file, self.cover_art_file)


        #image_ext           = os.path.splitext(cover_art)[1]
        #self.cover_art_file = os.path.abspath(album_dir + '/cover_art' + image_ext)
        
        #urllib.request.urlretrieve(cover_art, self.cover_art_file)
