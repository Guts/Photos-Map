from fractions import Fraction
import pyexiv2

# http://stackoverflow.com/a/13839068/2556577


image_file = 'test\img\'

try:
    metadata = pyexiv2.metadata.ImageMetadata(image_file)
    metadata.read();
    thumb = metadata.exif_thumbnail

    try:
        latitude = metadata.__getitem__("Exif.GPSInfo.GPSLatitude")
        latitudeRef = metadata.__getitem__("Exif.GPSInfo.GPSLatitudeRef")
        longitude = metadata.__getitem__("Exif.GPSInfo.GPSLongitude")
        longitudeRef = metadata.__getitem__("Exif.GPSInfo.GPSLongitudeRef")

        latitude = str(latitude).split("=")[1][1:-1].split(" ");
        latitude = map(lambda f: str(float(Fraction(f))), latitude)
        latitude = latitude[0] + u"\u00b0" + latitude[1] + "'" + latitude[2] + '"' + " " + str(latitudeRef).split("=")[1][1:-1]

        longitude = str(longitude).split("=")[1][1:-1].split(" ");
        longitude = map(lambda f: str(float(Fraction(f))), longitude)
        longitude = longitude[0] + u"\u00b0" + longitude[1] + "'" + longitude[2] + '"' + " " + str(longitudeRef).split("=")[1][1:-1]

        latitude_value = dms_to_decimal(*metadata.__getitem__("Exif.GPSInfo.GPSLatitude").value + [metadata.__getitem__("Exif.GPSInfo.GPSLatitudeRef").value]);
        longitude_value = dms_to_decimal(*metadata.__getitem__("Exif.GPSInfo.GPSLongitude").value + [metadata.__getitem__("Exif.GPSInfo.GPSLongitudeRef").value]);

        print "--- GPS ---"
        print "Coordinates: " + latitude + ", " + longitude
        print "Coordinates: " + str(latitude_value) + ", " + str(longitude_value)
        print "--- GPS ---"
    except Exception, e:
        print "No GPS Information!"
        #print e

    # Check for thumbnail
    if(thumb.data == ""):
        print "No thumbnail!"
except Exception, e:
    print "Error processing image..."
    print e;