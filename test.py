import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
import re

url = 'https://gale.agency'
site = requests.get(url)
soup = BeautifulSoup(site.content, 'html.parser')
parsed_url = urlparse(url)
links = list()
for x in soup.find_all('img'):
	if x['src'].startswith('/') and parsed_url.scheme+'://'+parsed_url.hostname+x['src'] not in links:
		links.append(parsed_url.scheme+'://'+parsed_url.hostname+x['src'])
	elif re.search('(http|https):\/\/(.*?)\.gale\.agency', x['src']) is not None and x['src'] not in links and urlparse(x['src']).path != '/':
		links.append(x['src'])
print links