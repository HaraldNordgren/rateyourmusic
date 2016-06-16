# Rateyourmusic album adder

Add or update Rateyourmusic (RYM) albums using information from Bandcamp or Spotify.

Example: ` python3 src/main/rym_adder.py --url https://ailanthusrecordings.bandcamp.com/album/m-rec update-album --rym-album https://rateyourmusic.com/release/album/%ED%9A%8C%EC%82%ACauto/amireca
`

Run the program with `python3 src/main/rym_adder.py`. Either a Bandcamp URL or Spotify URI is mandatory and is specified using the `--url` or `--spotify-uri` options. Help can be accessed by supplying the `-h` option.

RYM options are entered without dashes as `add-artist` `add-album` `add-issue` `update-album`, and some of them come with their own sub-options like an URL to an artist or album page.

Get help for the RYM options like this: ` python3 python/main/rym_adder.py add-issue -h`
