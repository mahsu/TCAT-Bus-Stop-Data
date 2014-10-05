TCAT Bus Stop Data
==================

Scrapes the TCAT [website](http://tcat.nextinsight.com/allstops.php) for developers looking to create transit apps. The following data is currently scraped:
* Stop id
* Stop name
* Latitude
* Longitude
* Area
* Additional Stop Information

The scraped output can be found in `TCATstops.csv`.

##Running The Scraper
Install [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) and run `scrape.py` under python 3.
