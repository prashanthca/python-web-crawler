from bs4 import BeautifulSoup
import requests
import json
from django.conf import settings
import sqlite3
import re
from urlparse import urlparse

def GetLinksUtil(siteData):
	site=json.loads(siteData.body)
	request = requests.get(site['url'])
	soup = BeautifulSoup(request.content, 'html.parser')
	parsed_url = urlparse(site['url'])
	links = list()
	for x in soup.find_all('a'):
		if x.has_attr('href'):
			if x['href'] != '/' and x['href'].startswith('/') and parsed_url.scheme+'://'+parsed_url.hostname+x['href'] not in links:
				links.append(parsed_url.scheme+'://'+parsed_url.hostname+x['href'])
			elif re.search('(http|https):\/\/(.*?)\.gale\.agency', x['href']) is not None and x['href'] not in links and urlparse(x['href']).path != '/':
				links.append(x['href'])
	return links

def GetImagesUtil(siteData):
	site=json.loads(siteData.body)
	request = requests.get(site['url'])
	soup = BeautifulSoup(request.content, 'html.parser')
	parsed_url = urlparse(site['url'])
	links = list()
	for x in soup.find_all('img'):
		if x['src'].startswith('/') and parsed_url.scheme+'://'+parsed_url.hostname+x['src'] not in links:
			links.append(parsed_url.scheme+'://'+parsed_url.hostname+x['src'])
		elif re.search('(http|https):\/\/(.*?)\.gale\.agency', x['src']) is not None and x['src'] not in links and urlparse(x['src']).path != '/':
			links.append(x['src'])
	return links