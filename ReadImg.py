#-*-coding: utf-8-*-
#!/usr/bin/env python
from __future__ import unicode_literals
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
from fractions import Fraction
from os import path, walk
import geojson

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
            if path.splitext(path.join(root, i))[1] == u'.JPG' or path.splitext(path.join(root, i))[1] == u'.JPEG':
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


def dms_to_decimal(degrees, minutes, seconds, sign=' '):
    """Convert degrees, minutes, seconds into decimal degrees.

    >>> dms_to_decimal(10, 10, 10)
    10.169444444444444
    >>> dms_to_decimal(8, 9, 10, 'S')
    -8.152777777777779
    """
    return (-1 if sign[0] in 'SWsw' else 1) * (
        float(degrees)        +
        float(minutes) / 60   +
        float(seconds) / 3600
    )


def decimal_to_dms(decimal):
    """Convert decimal degrees into degrees, minutes, seconds.

    >>> decimal_to_dms(50.445891)
    [Fraction(50, 1), Fraction(26, 1), Fraction(113019, 2500)]
    >>> decimal_to_dms(-125.976893)
    [Fraction(125, 1), Fraction(58, 1), Fraction(92037, 2500)]
    """
    remainder, degrees = math.modf(abs(decimal))
    remainder, minutes = math.modf(remainder * 60)
    return [Fraction(n) for n in (degrees, minutes, remainder * 60)]



tup_photos = li_photos(r'test\img')
li_pts = []

for photo in tup_photos:
    """ explore exif geotags of each photo """
    print '\n', path.basename(photo)
    # with EXIF (https://github.com/ianare/exif-py)
    with open(photo, 'r') as tof:
        tags = EXIF.process_file(tof)
        coord_EXIF = (str(tags.get('GPS GPSLatitude')), str(tags.get('GPS GPSLongitude')), str(tags.get('GPS GPSAltitude')))
    # with pyexiv2
    md = pyexiv2.ImageMetadata(photo)
    md.read()
    lat = md.__getitem__("Exif.GPSInfo.GPSLatitude")
    latRef = md.__getitem__("Exif.GPSInfo.GPSLatitudeRef")
    lon = md.__getitem__("Exif.GPSInfo.GPSLongitude")
    lonRef = md.__getitem__("Exif.GPSInfo.GPSLongitudeRef")

    lat = str(lat).split("=")[1][1:-1].split(" ");
    lat = map(lambda f: str(float(Fraction(f))), lat)
    lat = lat[0] + u"\u00b0" + lat[1] + "'" + lat[2] + '"' + " " + str(latRef).split("=")[1][1:-1]

    lon = str(lon).split("=")[1][1:-1].split(" ");
    lon = map(lambda f: str(float(Fraction(f))), lon)
    lon = lon[0] + u"\u00b0" + lon[1] + "'" + lon[2] + '"' + " " + str(lonRef).split("=")[1][1:-1]

    lat_value = dms_to_decimal(*md.__getitem__("Exif.GPSInfo.GPSLatitude").value + [md.__getitem__("Exif.GPSInfo.GPSLatitudeRef").value])
    lon_value = dms_to_decimal(*md.__getitem__("Exif.GPSInfo.GPSLongitude").value + [md.__getitem__("Exif.GPSInfo.GPSLongitudeRef").value])
    alt_value = md.__getitem__("Exif.GPSInfo.GPSAltitude").value
    print "\n\n--- GPS ---"
    print "Coordinates: " + lat + ", " + lon
    print "Coordinates: " + str(lat_value) + ", " + str(lon_value)
    print "Altitude: " + str(alt_value)
    print "--- GPS ---"
    coord_pyexiv = (md['Exif.GPSInfo.GPSLatitude'].raw_value, md['Exif.GPSInfo.GPSLongitude'].raw_value, md['Exif.GPSInfo.GPSAltitude'].raw_value)
    # with pillow
    keys = get_exif(photo)
    coord_pillow = (keys.get('GPSInfo').get(2), keys.get('GPSInfo').get(4), keys.get('GPSInfo').get(6))

    # prints
    print "\navec pyEXIF", coord_EXIF
    print "avec pyexiv2", coord_pyexiv
    print "avec pillow", coord_pillow

    # geojsonning
    li_pts.append(geojson.Point([lon_value, lat_value]))

points = geojson.GeometryCollection(li_pts)

with open('photo_maps.geojson', 'w') as out_geojson:
    geojson.dump(points, out_geojson)


def main():
    pass

################################################################################
##### Stand alone execution #######
###################################

if __name__ == '__main__':
    main()
