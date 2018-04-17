from beets.plugins import BeetsPlugin
from beets.ui import Subcommand

ITEM_TAGS = ['acoustid_fingerprint', 'acoustid_id', 'added', 'album', 'album_id', 'albumartist', 'albumartist_credit', 'albumartist_sort', 'albumdisambig', 'albumstatus', 'albumtype', 'arranger', 'artist', 'artist_credit', 'artist_sort', 'asin', 'bitdepth', 'bitrate', 'bpm', 'catalognum', 'channels', 'comments', 'comp', 'composer', 'composer_sort', 'country', 'day', 'disc', 'disctitle', 'disctotal', 'encoder', 'filesize', 'format', 'genre', 'grouping', 'id', 'initial_key', 'label', 'language', 'length', 'lyricist', 'lyrics', 'mb_albumartistid', 'mb_albumid', 'mb_artistid', 'mb_releasegroupid', 'mb_trackid', 'media', 'month', 'mtime', 'original_day', 'original_month', 'original_year', 'path', 'r128_album_gain', 'r128_track_gain', 'rg_album_gain', 'rg_album_peak', 'rg_track_gain', 'rg_track_peak', 'samplerate', 'script', 'singleton', 'title', 'track', 'tracktotal', 'year']

import_txt = Subcommand('txtimport', help='Import tags from a .txt file', aliases=['txt'])

def txt_in(lib, opts, args):
    print("IMPORT TAGS FROM TXT FILE")
    filename = input("Please enter the .txt file of the tags: ")
    if filename[-4:] != '.txt':
        print("Sorry, this file is not a .txt file!")
        sys.exit()
    else:
        with open(filename) as f:
            for line in f:
                keys = {}
                line = line.strip()
                things = line.split(';')
                for i in things:
                    duo = i.split('=')
                    if len(duo) > 2:
                        print("ERROR: The file is not formatted correctly!")
                        print(duo)
                        sys.exit()
                    if duo[0] not in ITEM_TAGS:
                        print("ERROR:", duo[0], "is not a valid tag value!")
                        print("Run 'beet fields' to see all valid tag values!") 
                    keys[duo[0]] = duo[1]

                item = lib.items(query=keys['title'])
                if keys['id'] != None:
                    item = lib.get_item(keys['id'])
                print("\n\nPrevious File Info:\n")
                for k, v in item.items():
                    if k in keys:
                        print(k, ":", v)

                print("\n\nNew File Info:\n") 
                for k, v in keys.items():
                    item.set_parse(k, v)
                    print(k, ":", v)    
                st = input("\n\nDo you want to save these new tags? [Y/n] ")
                if st == 'Y' or st == 'y':
                    item.store()
                    print("Saved!")

import_txt.func = txt_in

class TagImport(BeetsPlugin):
    def commands(self):
        return [import_txt]