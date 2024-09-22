import requests
import sys
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse

filesFound = 0
filesDownloaded = 0

class color:
	RED = '\033[91m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	DEFAULT = '\033[0m'


def getIndex(link):
    pos = -1
    count = 0
    for i, char in enumerate(link):
        if char == '/':
            count += 1
        if count == 3:
            pos = i
            break
    if pos != -1:
        return link[:pos]
    return link

def downloadImages(link, imgs):
	global filesDownloaded
	mainDir = link.lstrip('htps:/.')
	for img in imgs:
		if img.startswith('https://') or img.startswith('http://'):
			os.makedirs('data/' + mainDir  + '/' + img[:img.rfind('/')], exist_ok = True)
			imgfile = requests.get(img, timeout=10, verify=True)
		else:
			os.makedirs('data/' + mainDir + '/' + img[:img.rfind('/')], exist_ok = True)
			imgfile = requests.get(urljoin(link, img), timeout=10, verify=True)
		if not imgfile.ok:
			if img.startswith('https://') or img.startswith('http://'):
				print(color.RED + "Error: couldn't download " + img + color.DEFAULT)
			else:
				print(color.RED + "Error: couldn't download " + urljoin(link, img) + color.DEFAULT)
		else:
			filesDownloaded += 1
			if img.startswith('https://') or img.startswith('http://'):
				print(color.GREEN + "Succes : " + color.DEFAULT + img + " was downloaded")
			else:
				print(color.GREEN + "Succes : " + color.DEFAULT + link + img + " was downloaded")
			with open('./data/' + mainDir + '/' + img, 'wb') as f:
				f.write(imgfile.content)
				

def catchImages(link):
	global filesFound
	try:
		site = requests.get(link, timeout=10, verify=True)
	except requests.exceptions.RequestException as e:
		print(color.RED + "Error: couldn't reach " + link + color.DEFAULT)
		return []
	soup = BeautifulSoup(site.content, features="html.parser")
	if not site.ok:
		print("Error: target returned the " + str(site.status_code) + " error code.")
	print("Ping was successful !")
	imgs = soup.find_all('img')
	recursObjs = soup.find_all('a', href=True)
	recursLinks = []
	for i in recursObjs:
		if i.get('href').startswith('http') or i.get('href').startswith('https'):
			recursLinks.append(i.get('href').split('#')[0])
		else:
			recursLinks.append(urljoin(link, i.get('href').split('#')[0]))
	print(str(len(recursLinks)) + " links found")
	imgsLinks = []
	for img in imgs:
		imgLink = img.get('src').split('#')[0]
		if str(imgLink).endswith('.bmp') or str(imgLink).endswith('.png') \
			or str(imgLink).endswith('.jpeg') or str(imgLink).endswith('.jpg') or str(imgLink).endswith('.gif'):
			imgsLinks.append(imgLink)
	filesFound += len(imgsLinks)
	print(str(len(imgsLinks)) + " images found")
	downloadImages(getIndex(link), imgsLinks)
	return recursLinks



def main():
	recursions = 0
	argparser = argparse.ArgumentParser(description='Download images from a website')
	argparser.add_argument('-r', action='store_true', help='Recursively download images from the links found on the website')
	argparser.add_argument('-l', type=int, help='Select the depth of the recursion')
	argparser.add_argument('-p', action='store_true', help='Change the path of the download')
	argparser.add_argument('target', type=str, help='The target website')
		# print("Error: missing target")
		# exit()
	args = argparser.parse_args()
	if not args.target:
		print("Error: missing target")
		exit()
	if args.r:
		recursions = 5
	if args.l:
		if not args.r:
			print("ausage: spider.py [-h] [-r] [-l] [-p] [depth] target")
			exit()
		if args.depth:
			recursions = args.depth
		else:
			print("Error: missing depth")
			exit()
	if args.p:
		if args.path:
			os.chdir(args.path)
		else:
			print("Error: missing path")
			exit()
	list = [[]]
	if not args.target.startswith('http'):
		args.target = 'http://' + args.target
	list[0]+= catchImages(args.target)
	for i in range(recursions):
		list.append([])
		for j in list[i]:
			list[i + 1] += catchImages(j)
			# print(list)
	print(color.YELLOW + str(filesDownloaded) + "/" + str(filesFound) +" images downloaded" + color.DEFAULT)
	
	# catchImages(sys.argv[1])
	
if __name__ == "__main__":
    main()

