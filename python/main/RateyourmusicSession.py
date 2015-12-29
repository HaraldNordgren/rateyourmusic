import splinter, time, sys, datetime, re
import AlbumEntry, credentials, images

from bs4 import BeautifulSoup
from attribute_strings import *
from PIL import Image


class RateyourmusicSession:

    def login(self):
        
        self.br.visit('https://rateyourmusic.com/account/login')
        time.sleep(3)
        
        self.br.fill('username', credentials.username)
        self.br.fill('password', credentials.password)
        
        self.br.find_by_id('login_submit').click()
        time.sleep(5)

    def __init__(self):

        self.br = splinter.Browser()
        self.login()

    def submit_info(self, album_entry):

        if album_entry.primary_issue:

            self.br.find_by_id('parent_id').select('other')
            self.br.find_by_id('parent_shortcut').fill(album_entry.primary_issue)

            self.br.find_by_id('filed_under_same_as_parent_yes').click()

        # Set release type to EP only if title ends with " EP"
        if bool(re.search(' EP$', album_entry.title)):
            self.br.find_by_id('categorye').click()

        self.br.fill('title', album_entry.title)

        if album_entry.lossless:
            self.br.find_by_id('format59').click()
        else:
            self.br.find_by_id('format58').click()

        self.br.find_by_id('goAdvancedBtn').click()
        tracks_text_area = self.br.find_by_id('tracks_adv').find_by_id('track_advanced')
        tracks_text_area.fill(album_entry.full_tracklist) 
        self.br.find_by_id('goSimpleBtn').click()

        self.br.fill('notes', album_entry.source)
     
        # Only add if release year is reasonable
        if 2010 <= int(album_entry.year) <= datetime.date.today().year:

            self.br.find_by_id('year').select(album_entry.year)
            self.br.find_by_id('month').select(album_entry.month)
            self.br.find_by_id('day').select(album_entry.day)
        
        self.br.find_by_id('previewbtn').click()
        time.sleep(2)
        
        self.br.find_by_id('submitbtn').click()

    def upload_cover(self, args, album_entry):

        self.br.attach_file('upload_file', album_entry.cover_art_file)
        self.br.fill('source', album_entry.source)

        if args.nudity:
            self.br.find_by_id('content_nudity').click()

        self.br.find_by_id('uploadbutton').click()
        time.sleep(10)

        # Approve image
        self.br.click_link_by_partial_href('javascript:setStatus')
        self.br.click_link_by_partial_href('/release/')

    def add_artist_to_rym(self, album_entry):

        self.br.visit('https://rateyourmusic.com/artist_add')

        self.br.fill('lastname', album_entry.artist)
        self.br.fill('comments', album_entry.source)

        self.br.find_by_id('submitbtn').click()
        time.sleep(3)
        
        # Go to newly created artist page
        self.br.find_by_text(album_entry.artist).click()

    def vote_for_genres(self, album_entry):

        # Go to genre voting page
        self.br.click_link_by_partial_href('/rgenre/set?')

        for genre in album_entry.genres:
            
            # Fill the primary genre text area and propose the genre
            self.br.find_by_xpath("//input[@id='prigen']").fill(genre)
            self.br.find_by_xpath("//input[@value='+ propose']").first.click()

        # Go back to release
        self.br.click_link_by_partial_href('/release/')

    def update_rym_album(self, args, album_entry):
            
        self.br.visit(args.rym_album)
        time.sleep(2)
         
        if info in args.update:

            self.br.find_by_text('Correct this entry').click()    
            self.submit_info(album_entry)
            time.sleep(2)

        self.br.visit("%s/buy" % args.rym_album)
        time.sleep(1)
        
        rym_cover_url = self.br.find_by_text('View cover art')['href']
        rym_cover_path = images.download_cover_art(rym_cover_url,
                album_entry, rateyourmusic_original=True)

        rym_cover = Image.open(rym_cover_path)
        new_cover = Image.open(album_entry.cover_art_file)

        if new_cover.size[0] > rym_cover.size[0]:
            
            self.br.visit(args.rym_album)
            time.sleep(3)
            
            self.br.find_by_text('Upload cover art').click()
            
            self.upload_cover(args, album_entry)
            time.sleep(2)
            
        self.br.visit(args.rym_album)
        time.sleep(3)

    def add_album_to_rym(self, args, album_entry):

        subparser_option = getattr(args, subparser_string)
        
        if subparser_option == update_album:

            self.update_rym_album(args, album_entry)
            return

        if subparser_option == add_artist:
            
            self.add_artist_to_rym(album_entry)
        
        elif subparser_option == add_issue:
               
            self.br.visit(args.primary_url)
            time.sleep(2)

            album_title_div = self.br.find_by_xpath("//div[@class='album_title']")
            primary_shortcut_area = \
                    album_title_div.find_by_xpath(".//input[@class='album_shortcut']")
            
            album_entry.primary_issue = primary_shortcut_area['value']

            artist_name_box = album_title_div.find_by_xpath(".//a")
            self.br.visit(artist_name_box['href'])
        
        else:
            
            self.br.visit(args.rym_profile)
        
        time.sleep(3)
        self.br.click_link_by_partial_href('/releases/ac?artist_id=')
        self.submit_info(album_entry)
        
        self.br.click_link_by_partial_href('/images/upload?type=l&assoc_id=')
        self.upload_cover(args, album_entry)

        time.sleep(3)
