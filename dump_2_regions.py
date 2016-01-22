#! /usr/bin/python

# Requires Python >2.7.2 

import json, re

with open("abcd_dump_2012Jun25.json","rb") as dump_f:
	abcd_dump = json.load(dump_f)

num_aff = 0
num_eff = 0
num_cnct =0

all_regions = {}
all_connections = {}
for r_id, r_data in abcd_dump.iteritems():
	if len(r_data) > 2:
		all_regions[r_id] = {}
		for key, val in r_data.items():
			if key == "afferents" or key == "efferents":
				# add projection to connections dict
				connections = val
				for region, info in connections.items():
					from_id = re.findall('(?<=\&sid\\=)\w+', info['url'])[0]
					to_id = re.findall('(?<=\&rid\\=)\w+', info['url'])[0]
					connection_id = re.findall('(?<=\&id\\=)\w+', info['url'])[0]
					if from_id == r_id:
						num_eff += 1
					elif to_id == r_id:
						num_aff += 1

					if not connection_id in all_connections.keys():
						num_cnct += 1
						cnct_info = {}
						cnct_info['from_region'] = from_id
						cnct_info['to_region'] = to_id
						cnct_info['id'] = connection_id
						cnct_info['url'] = info['url']
						if 'citations' in info.keys():
							cnct_info['citations'] = info['citations']
						all_connections[connection_id] = cnct_info
				pass
			else:
				all_regions[r_id][key] = val

with open("abcd_regions.json","wb") as regions_f:
	json.dump(all_regions, regions_f, sort_keys=True, indent=4)
with open("abcd_connections.json","wb") as regions_f:
	json.dump(all_connections, regions_f, sort_keys=True, indent=4)

print "afferents: %s, efferents %s, total: %s" % (num_aff, num_eff, num_cnct)