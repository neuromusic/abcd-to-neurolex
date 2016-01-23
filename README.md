# abcd-to-neurolex
scripts and data for getting pulling the Avian Brain Connectivity Database into Neurolex from the 2013 NIF Hackathon


# The Project

We wanted to get the regions and connections of the avian brain into the Neurolex Wiki.

Avian neuroanatomy poses an interesting case study in the challenges of maintaining a lexicon of brain regions, as the literature is a bit of a mess when it comes to naming. 

Much of the work in compiling the "state of the field" had been done already (see http://www.ncbi.nlm.nih.gov/pubmed/17889371) and deposited at http://behav.org/abcd

We contacted the grad student who had built the database, but they had moved on. Emails to the PI were not returned. So we decided to scrape the ABCD for avian brain regions and connections.

And it's a good thing we did, because the old ABCD hasn't been online since October 2014: http://web.archive.org/web/20141019130131/http://www.behav.org/abcd/abcd.php

So here are the scripts I used to scrape the database and the resulting data in JSON form.

Enjoy!

Justin Kiggins
@neuromusic

# Scripts

1. `abcd_scrape.py` to scrape the data from the ABCD
2. `dump_to_regions.py` to split the dump into "regions" and "connections"

# Data

- `abcd_dump_2012Jun25.json` is the raw dump from the ABCD
- `abcd_regions.json` is just the regions
- `abcd_connections.json` is just the connections
