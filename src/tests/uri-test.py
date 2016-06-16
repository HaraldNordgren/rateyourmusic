#!/usr/bin/env python2

from urlparse import urlparse

parsed_uri = urlparse( 'https://macinsoft.bandcamp.com/album/w-e-b-c-a-m-h-o-n-e-y-m-o-o-n' )
domain = parsed_uri.netloc

print domain
