from configparser import SafeConfigParser

b = 'bandcamp'

def read_config(filename):
    cfg = SafeConfigParser()
    cfg.read(filename)

    title       = cfg.get(b, 'title')
    artist      = cfg.get(b, 'artist')
    tracklist   = cfg.get(b, 'tracklist')
    
    year        = cfg.get(b, 'year')
    month       = cfg.get(b, 'month')
    day         = cfg.get(b, 'day')
    
    cover       = cfg.get(b, 'cover')

    return (title, artist, tracklist, year, month, day, cover)


def write_config(filename, title, artist, tracklist, year, month, day, cover):
    cfg = SafeConfigParser()
    cfg.add_section(b)

    cfg.set(b, 'title', title)
    cfg.set(b, 'artist', artist)
    cfg.set(b, 'tracklist', tracklist)
    
    cfg.set(b, 'year', year)
    cfg.set(b, 'month', month)
    cfg.set(b, 'day', day)
    
    cfg.set(b, 'cover', cover)

    with open(filename, 'w') as f:
        cfg.write(f)
