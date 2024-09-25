from PIL import Image
import sys

def main():
    exif = Image.open(sys.argv[1])._getexif()
    if not exif:
        raise Exception('Image {0} does not have EXIF data.'.format(sys.argv[1]))
    print(exif[36867])
if __name__ == "__main__":
    main()
