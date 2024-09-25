from PIL import Image, ExifTags
import sys
from pathlib import Path

def printPerms():
    perms = oct(Path(sys.argv[1]).stat().st_mode)[-3:]
    rwx_mapping = {
        '0': '---',
        '1': '--x',
        '2': '-w-',
        '3': '-wx',
        '4': 'r--',
        '5': 'r-x',
        '6': 'rw-',
        '7': 'rwx',
    }
    return (rwx_mapping[perms[0]] + rwx_mapping[perms[1]] + rwx_mapping[perms[2]])

def returnTrueSize(size):
    if (size < 1024):
        return str(round(size, 2)) + " bytes"
    elif (size < 1048576):
        return str(round(size / 1024, 2)) + " KB"
    elif (size < 1073741824):
        return str(round(size / 1048576, 2)) + " MB"
    else:
        return str(round(size / 1073741824, 2)) + " GB"

def printInfo():
    img = Image.open(sys.argv[1])
    exif = img._getexif()
    if not exif:
        raise Exception('Image {0} does not have EXIF data.'.format(sys.argv[1]))
    print("Scorpion - Image Metadata Extractor\n")
    print("#### Image Information ####")
    print("File Name : " + Path(sys.argv[1]).stem)
    print("Image Format : " + img.format)
    fileSize = Path(sys.argv[1]).stat().st_size
    print("File Permissions : " + printPerms())
    print("File Size : " + returnTrueSize(fileSize))
    print("Image Size : " + str(img.size[0]) + "x" + str(img.size[1]) + " pixels\n\n")
    for tag, value in exif.items():
        if tag in ExifTags.TAGS:
            print(ExifTags.TAGS[tag] + " : " + str(value))

def main():
    printInfo()
if __name__ == "__main__":
    main()
