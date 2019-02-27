from bs4 import BeautifulSoup
import requests
import json
from django.conf import settings
from Crawler.models import Links, Images
import re
from urlparse import urlparse

def GetLinksUtil(siteData):
	site=json.loads(siteData.body)
	siteInDB = None
	try:
		siteInDB = Links.objects.get(url=site['url'])
	except Exception as e:
		siteInDB = None
		pass
	if siteInDB != None:
		return siteInDB.json
	request = requests.get(site['url'])
	soup = BeautifulSoup(request.content, 'html.parser')
	parsed_url = urlparse(site['url'])
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
	siteIntoDB = Links(url=site['url'], json=json_links)
	siteIntoDB.save()
	return json_links

def GetImagesUtil(siteData):
	site=json.loads(siteData.body)
	siteInDB = None
	try:
		siteInDB = Images.objects.get(url=site['url'])
	except Exception as e:
		siteInDB = None
		pass
	if siteInDB != None:
		return siteInDB.json
	request = requests.get(site['url'])
	soup = BeautifulSoup(request.content, 'html.parser')
	parsed_url = urlparse(site['url'])
	links = list()
	for x in soup.find_all('img'):
		if x['src'].startswith('//'):
			x['src'] = parsed_url.scheme+':'+x['src']
		if x['src'].startswith('/') and parsed_url.scheme+'://'+parsed_url.hostname+x['src'] not in links:
			links.append(parsed_url.scheme+'://'+parsed_url.hostname+x['src'])
		elif x['src'].startswith(parsed_url.scheme+'://'+parsed_url.hostname) and x['src'] not in links and urlparse(x['src']).path != '/':
			links.append(x['src'])
	json_links = json.dumps(links)
	siteIntoDB = Images(url=site['url'], json=json_links)
	siteIntoDB.save()
	return json_links