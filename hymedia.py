#!/bin/env python3
from __future__ import print_function
import os,sys
import magic
import ffmpeg
import argparse



def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_info(inputFile):
  try:
      probe = ffmpeg.probe(inputFile)
  except ffmpeg.Error as e:
      #print(e.stderr)
      return None
  return probe


def stream_info(stream):
    return "Stream %d - %s(%s): %s - %s" % (
        stream['index'],
        stream['codec_type'],
        stream['tags']['language'] if (
            'tags' in stream.keys() and
            'language' in stream['tags'].keys()) else '???',
        stream['codec_name'] if 'codec_name' in stream.keys() else '???',
        '...'
        )

parser = argparse.ArgumentParser(description='HyMedia')
parser.add_argument('directory', type=str,
        help='the directory to recursively examine')
args = parser.parse_args()
if not os.path.isdir(args.directory):
    eprint("%s is not a directory!" % args.directory)
    parser.print_help()
    sys.exit(1)

mime = magic.Magic(mime=True)
for folder, subs, files in os.walk(args.directory):
    for fn in files:
        filename = "%s/%s" % ( folder,fn )
        if os.path.isfile(filename) and \
          mime.from_file(filename).split('/')[0] == 'video':
            info = get_info(filename)
            if info is not None:
                print("File %s:" % filename)
                for stream in info['streams']:
                    print(stream_info(stream))
                print()
            else:
                eprint("ffprobe FAIL on %s" % filename)
        else:
            eprint("FAIL on %s" % filename)
