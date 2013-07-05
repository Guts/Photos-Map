#-*-coding: utf-8-*-
#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Julien
#
# Created:     05/07/2013
# Copyright:   (c) Julien 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

################################################################################
######## Libraries import #########
###################################

# standard library
from os import path, walk
from geojson import *

# 3rd party libraries
from PIL import Image
from PIL.ExifTags import TAGS

import pyexiv2

from modules import EXIF


################################################################################
############# Classes #############
###################################

def li_photos(folder):
    photos = []
    for root, dirs, files in walk(folder):
        for i in files:
            if path.splitext(path.join(root, i))[1] == u'.JPG':
                photos.append(path.abspath(path.join(root, i)))
    # end of function
    return tuple(photos)


def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret


tup_photos = li_photos(r'test/img')


for photo in tup_photos:
    """ explore exif geotags of each photo """
    # with EXIF (https://github.com/ianare/exif-py)
    with open(photo, 'r') as tof:
        tags = EXIF.process_file(tof)
        coord_EXIF = (str(tags.get('GPS GPSLatitude')), str(tags.get('GPS GPSLongitude')), str(tags.get('GPS GPSAltitude')))
    # with pyexiv2
    md = pyexiv2.ImageMetadata(photo)
    md.read()
    coord_pyexiv = (md['Exif.GPSInfo.GPSLatitude'].raw_value, md['Exif.GPSInfo.GPSLongitude'].raw_value, md['Exif.GPSInfo.GPSAltitude'].raw_value)
    # with pillow
    keys = get_exif(photo)
    coord_pillow = (keys.get('GPSInfo').get(2), keys.get('GPSInfo').get(4), keys.get('GPSInfo').get(6))

    # prints
    print '\n', path.basename(photo)
    print "\navec pyEXIF", coord_EXIF
    print "avec pyexiv2", coord_pyexiv
    print "avec pillow", coord_pillow


def main():
    pass

################################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    main()
