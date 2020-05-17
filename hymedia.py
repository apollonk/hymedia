#!/bin/env python3
import os,sys
import magic
import ffmpeg

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

mime = magic.Magic(mime=True)
for folder, subs, files in os.walk('vault/Downloads'):
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
                print("ffprobe FAIL on %s" % filename)
        else:
            print("FAIL on %s" % filename)
