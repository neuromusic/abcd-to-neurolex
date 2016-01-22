#! /usr/bin/python

# Requires Python >2.7.2 and Beautiful Soup 4 
# >>> easy_install beautifulsoup4

from urllib import urlopen
from bs4 import BeautifulSoup
import re, time, json

abcd = {}
bds = (1,413)
all_rids = range(bds[0],bds[1]+1)
# all_rids = range(1,413)
for rid in all_rids:
	print "processing region number %s..." % rid

	region_dict = {}
	region_dict['id'] = rid # perhaps redundant
	region_dict['url'] = 'http://www.behav.org/abcd/abcd.php?id=%s&proc=arer' % rid

	detail_page = BeautifulSoup(urlopen(region_dict['url']).read().replace('\";', '\"'))
	time.sleep(0.2)
	table_rows = detail_page.find('table', attrs={'width': '600', 'cellspacing': '1'}).findAll('tr')

	for row in table_rows:
		row_items = row.findAll('td')
		if len(row_items) < 2:
			continue

		key = row_items[0].text.strip().lower().rstrip(':')

		if len(key) == 0:
			continue
		elif 'connections' in key:
			continue
		elif key == 'name':
			value = row_items[1].text.strip()
			if len(value) == 0: continue
		elif key == 'abbreviation':
			value = row_items[1].text.strip()
			if len(value) == 0: continue
		elif key == 'old name':
			value = row_items[1].text.strip()
			if len(value) == 0: continue
		elif key == 'old abbreviation':
			value = row_items[1].text.strip()
			if len(value) == 0: continue
		elif key == 'english name':
			value = row_items[1].text.strip()
			if len(value) == 0: continue
		elif key == 'other name(s)':
			value = []
			other_names = row_items[1].findAll('tr')
			for name in other_names:
				name_td = name.find('td')
				if len(name_td.text) == 0: continue
				value.append(name_td.text)
			if len(value) == 0: continue
		elif key == 'proposed mammalian homologue':
			value = row_items[1].text.strip()
			if len(value) == 0: continue
		elif key == 'subregion(s)':
			value = []
			subregions = row_items[1].findAll('tr')
			for region in subregions:
				region_td = region.find('td')
				url = region.find('td').find('a')['href']
				sub_rid = re.findall('(?<=id\\=)\w+', url)[0]
				if len(sub_rid) > 0:
					value.append(sub_rid)
			if len(value) == 0: continue
		elif key == 'superregion':
			url = row_items[1].find('a')['href']
			sup_rid = re.findall('(?<=id\\=)\w+', url)[0]
			if len(sup_rid) > 0:
				value = sup_rid
		elif key == 'functional keyword(s)':
			value = []
			func_keywords = row_items[1].findAll('tr')
			for keyword in func_keywords:
				keyword_td = keyword.find('td')
				if 'no entry' in keyword_td.text: continue
				value.append(keyword_td.text)
			if len(value) == 0: continue
		elif key == 'related images':
			continue
		elif 'no entry' in key:
			continue

		region_dict[key] = value

	connections_url = 'http://www.behav.org/abcd/abcd.php?proc=conrg&id=%s' % rid
	connections_page = BeautifulSoup(urlopen(connections_url).read().replace('\";', '\"'))
	connection_links = connections_page.findChildren('a', attrs={'title': 'details'})

	afferents_dict = {}
	efferents_dict = {}

	for link in connection_links: # now go through each connection and scrape from that page
		connection_dict = {}
		url_to_open = 'http://www.behav.org/abcd/%s' % link.attrs['href']
		connection_dict['url'] = url_to_open

		from_rid = re.findall('(?<=sid\\=)\w+', link.attrs['href'])[0]
		to_rid = re.findall('(?<=rid\\=)\w+', link.attrs['href'])[0]

		connection_details = BeautifulSoup(urlopen(url_to_open).read().replace('\";', '\"'))
		time.sleep(0.1)

		citation_links = connection_details.findAll('td', attrs={'bgcolor': '#EFF1E2'})[4].findChildren('a')

		citations = []
		if len(citation_links) > 0: # now go through each citation
			for cite in citation_links:
				cite_dict = {}
				cite_dict['url'] = cite['href']
				cite_dict['short'] = cite.text

				if 'pubmed' in cite_dict['url']:
					cite_dict['PMID'] = re.search('uids\=(\d+)',cite_dict['url']).groups()[0]
				elif 'amazon' in cite_dict['url']:
					cite_dict['ASIN'] = re.search('ASIN\/(\w+)',cite_dict['url']).groups()[0]

				citations.append(cite_dict)
		if len(citations) > 0:
			connection_dict['citations'] = citations

		if from_rid == str(region_dict['id']):
			efferents_dict[to_rid] = connection_dict 
		elif to_rid == str(region_dict['id']):
			afferents_dict[from_rid] = connection_dict

	if len(afferents_dict) > 0:
		region_dict['afferents'] = afferents_dict
	if len(efferents_dict) > 0:
		region_dict['efferents'] = efferents_dict

	abcd[rid] = region_dict

print "writing json..."
with open('abcd_dump_%s-%s.json' % bds,'wb') as fp:
	json.dump(abcd, fp, sort_keys=True, indent=4)


