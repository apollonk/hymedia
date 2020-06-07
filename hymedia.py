#!/bin/env python3
from __future__ import print_function
import os,sys
import magic
import ffmpeg
import argparse


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class MediaStream:
    """Representation of an AV media stream"""

    def __init__(self, stream):
        self.index = stream['index']
        self.codec_type = stream['codec_type'],
        self.language = stream['tags']['language'] if (
            'tags' in stream.keys() and
            'language' in stream['tags'].keys()) else '???'
        self.codec_name = stream['codec_name'] if 'codec_name' in stream.keys() else '???'

    def info(self):
        return "Stream %d - %s(%s): %s - %s" % (
            self.index,
            self.codec_type,
            self.language,
            self.codec_name,
            '...'
            )


class MediaFile:
    """Representation of an AV media container"""

    def __init__(self, filename):
        self.streams = []
        self.readable = False
        self.parseable = False
        self.filename = filename
        if os.path.isfile(filename) and \
          mime.from_file(filename).split('/')[0] == 'video':
            self.readable = True
            self.info = self.__get_info()
            if self.info is not None:
                self.parseable = True
                for stream in self.info['streams']:
                    self.streams.append( MediaStream(stream) )
            else:
                # TODO: raise an exception instead
                eprint("ffprobe FAIL on %s" % filename)
        else:
            # TODO: raise an exception instead
            eprint("FAIL on %s: Is not a mime type we can handle (%s)" % (
                filename, mime.from_file(filename) ))

    def get_info(self):
        return "Filename: %s -- Streams:\n%s" % ( self.filename,
            '\n'.join( [stream.info() for stream in self.streams] )
            )

    def __get_info(self):
        try:
            probe = ffmpeg.probe(self.filename)
        except ffmpeg.Error as e:
            #print(e.stderr)
            return None
        return probe

    def is_parseable(self):
        return self.parseable


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HyMedia')
    parser.add_argument('directory', type=str,
            help='the directory to recursively examine')
    args = parser.parse_args()
    if not os.path.isdir(args.directory):
        eprint("%s is not a directory!" % args.directory)
        parser.print_help()
        sys.exit(1)
    
    mime = magic.Magic(mime=True)
    medialist = []
    for folder, subs, files in os.walk(args.directory):
        for fn in files:
            try:
                mf = MediaFile("%s/%s" % ( folder, fn ))
                #print(mf.get_info())
                if mf.is_parseable():
                    medialist.append(mf)
            except:
                pass
    for media in medialist:
        print(media.filename)
        print(media.get_info())
        #pass
