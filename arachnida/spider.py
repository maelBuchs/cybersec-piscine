import requests
import sys
import os
from bs4 import BeautifulSoup


class color:
	RED = '\033[91m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	DEFAULT = '\033[0m'

def downloadImages(link, imgs, nbr):
	success = 0
	mainDir = link.lstrip('htps:/.')
	# if not os.path.exists(mainDir):
		# os.mkdir(mainDir)
	for img in imgs:
		# if not os.path.exists(mainDir + '/' + img[:img.rfind('/')]):
		if img.startswith('https://') or img.startswith('http://'):
			os.makedirs(mainDir + '/' + img[:img.rfind('/')], exist_ok = True)
			imgfile = requests.get(img)
		else:
			os.makedirs(mainDir + '/' + img[:img.rfind('/')], exist_ok = True)
			imgfile = requests.get(link + '/' + img)
		if not imgfile.ok:
			if img.startswith('https://') or img.startswith('http://'):
				print(color.RED + "Error: couldn't download " + img + color.DEFAULT)
			else:
				print(color.RED + "Error: couldn't download " + link + '/' + img + color.DEFAULT)
		else:
			success += 1
			if img.startswith('https://') or img.startswith('http://'):
				print(color.GREEN + "Succes : " + color.DEFAULT + img + "was downloaded")
			else:
				print(color.GREEN + "Succes : " + color.DEFAULT + link + img + "was downloaded")
			with open(mainDir + '/' + img, 'wb') as f:
				f.write(imgfile.content)
	print(color.YELLOW + str(success) + "/" + str(nbr) +" images downloaded" + color.DEFAULT)
				

def main():
	if len(sys.argv) != 2:
		print("Error: missing target")
		exit()
	link = sys.argv[1]
	site = requests.get(link)
	soup = BeautifulSoup(site.content, features="html.parser")
	if not site.ok:
		print("Error: target returned the " + str(site.status_code) + " error code.")
	print("Ping was successful !")
	imgs = soup.find_all('img')
	imgsLinks = []
	for img in imgs:
		imgLink = img.get('src')
		imgsLinks.append(imgLink)
	print(str(len(imgsLinks)) + " images found")
	downloadImages(link, imgsLinks, len(imgsLinks))



main()

