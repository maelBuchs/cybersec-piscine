import requests
import sys
import os
from bs4 import BeautifulSoup


def downloadImages(link, imgs):
	mainDir = link.lstrip('htps:/.')
	# if not os.path.exists(mainDir):
		# os.mkdir(mainDir)
	for img in imgs:
		# if not os.path.exists(mainDir + '/' + img[:img.rfind('/')]):
		os.makedirs(mainDir + '/' + img[:img.rfind('/')], exist_ok = True)
		imgfile = requests.get(link + '/' + img)
		with open(mainDir + '/' + img, 'wb') as f:
			f.write(imgfile.content)
				

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
	print(str(imgsLinks))
	downloadImages(link, imgsLinks)



main()