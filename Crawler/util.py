from bs4 import BeautifulSoup
import requests
import json
from django.conf import settings
from Crawler.models import Links, Images
import re
from urlparse import urlparse
import hashlib
from datetime import datetime

def LoadChildren(site, tree, level):
	ljson = json.loads(GetLinksUtil(site))
	for sit in ljson:
		tree["children"].append({"name": sit, "id": hashlib.md5(sit+str(datetime.now())).hexdigest()[:8], "children": []})
	if level > 0:
		for child in tree["children"]:
			LoadChildren(child["name"], child, level-1)
	else:
		for child in tree["children"]:
			ijson = json.loads(GetImagesUtil(child["name"]))
			for image in ijson:
				tree["children"].append({"name": image, "id": hashlib.md5(image+str(datetime.now())).hexdigest()[:8]})

def GetTree(siteData):
	site=json.loads(siteData.body)
	siteTree = {"name": site["url"], "id": hashlib.md5(site["url"]+str(datetime.now())).hexdigest()[:8], "children": []}
	levels = int(site["level"])
	LoadChildren(site["url"], siteTree, levels-1)
	return [siteTree]
		
def GetLinksUtil(site):
	#site=json.loads(siteData.body)
	siteInDB = None
	try:
		siteInDB = Links.objects.get(url=site)
	except Exception as e:
		siteInDB = None
		pass
	if siteInDB != None:
		return siteInDB.json
	request = requests.get(site)
	soup = BeautifulSoup(request.content, 'html.parser')
	parsed_url = urlparse(site)
	links = list()
	for x in soup.find_all('a'):
		if x.has_attr('href'):
			if x['href'].startswith('//'):
				x['href'] = parsed_url.scheme+':'+x['href']
			if x['href'] != '/' and x['href'].startswith('/') and parsed_url.scheme+'://'+parsed_url.hostname+x['href'] not in links:
				links.append(parsed_url.scheme+'://'+parsed_url.hostname+x['href'])
			elif x['href'].startswith(parsed_url.scheme+'://'+parsed_url.hostname) and '#' not in x['href'] and x['href'] not in links and urlparse(x['href']).path != '/' and urlparse(x['href']).path != '':
				links.append(x['href'])
	json_links = json.dumps(links)
	siteIntoDB = Links(url=site, json=json_links)
	siteIntoDB.save()
	return json_links

def GetImagesUtil(site):
	#site=json.loads(siteData.body)
	siteInDB = None
	try:
		siteInDB = Images.objects.get(url=site)
	except Exception as e:
		siteInDB = None
		pass
	if siteInDB != None:
		return siteInDB.json
	request = requests.get(site)
	soup = BeautifulSoup(request.content, 'html.parser')
	parsed_url = urlparse(site)
	links = list()
	for x in soup.find_all('img'):
		if x['src'].startswith('//'):
			x['src'] = parsed_url.scheme+':'+x['src']
		if x['src'].startswith('/') and parsed_url.scheme+'://'+parsed_url.hostname+x['src'] not in links:
			links.append(parsed_url.scheme+'://'+parsed_url.hostname+x['src'])
		elif x['src'].startswith(parsed_url.scheme+'://'+parsed_url.hostname) and x['src'] not in links and urlparse(x['src']).path != '/':
			links.append(x['src'])
	json_links = json.dumps(links)
	siteIntoDB = Images(url=site, json=json_links)
	siteIntoDB.save()
	return json_links