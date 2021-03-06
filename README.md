# property_scraper
Property Scraper

## Running the project


The project has two parts:

1. fetching URLs that we want to scrape
To fetch URLs that we scrape later run:
```bash
$  python main.py fetch
```

2. Scraping those URLs
To scrape the URLs that have been saved for scraping run:
```bash
$  python main.py scrape
```

query_local_db.py to query the local sqlite
For the moment it is set to drop the properties table
and reset scrape_yet column in the URLs table.
(DO NOT RUN THIS FILE WITHOUT VERIFYING.)


## Setting up venv
```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```
## ToDo:


- Parallelise the url_scraper call so that multiple pages can be scraped at once
- Shift to using postgresDB on AWS




Extension ideas?
- Further datasets/websites to scrape and add to the dataset
- Time based data so that the same property can be scraped monthly to detect any pricing variations?
- Frontend with metrics?

- Multithread the fetcher 


## Helpful:
https://www.worthwebscraping.com/how-to-scrape-zoopla-uk-real-estate-property-listings-scraping-using-python/
https://github.com/Tawfiqh/BeautifulSoupNotebookTest/blob/master/ParseWikipedia%20(YouTube%20Version).py (last time i used bs4)


## Done:
- add a requirements.txt file (need to setup a venv for this project)✅

- Write scraper (url_finder) to find URLs that we want to scrape and add them to a queue in the DB ✅
    - Do a search and add all of the results to the URLs table ✅

- Store results in DB ✅

- Scrape other website beyond Zoopla.  ✅
    - Find website to scrape  ✅
    - Extend url_finder to also find properties from new-website and add them to the URL queue ✅
    - Extend url_scraper to have a ZooplaRentScraper and a "PrimeLocationScraper" ✅

- url_scraper should pick records from the queue and scrape them with the right scraper either zoopla or PrimeLocationScraper ✅

- Write scraper (url_scraper) for individual zoopla-rented properties ✅

- url-fetcher should check the DB first, to check if the URL is already in the dataset before saving it. ✅

- Write scraper (url_scraper) for individual zoopla properties ✅

- Setup url_scraper to read from the queue and scrape that property ✅
    - Mark scraped property as NULL ==> SCRAPING ==> SCRAPED + date_scraped ✅

- write PrimeLocationScraper to scrape PrimeLocation for properties ✅

- Multithread the scraper ✅

- Scrape images and put in s3 bucket ✅
## Extensibility
To add new scrapers need to add a url-finder that fetches URLs of individual properties to scrape. Along with the type of scraper to use to scrape those individual properties. e.g: url_finders/zoopla_url_finder.py-ZooplaUrlFinder   

Then need to add a scraper that takes one of those URLs and scrapes it for property details and saves a Property object to the database. e.g: url_scrapers/zoopla_scraper.py-ZooplaScraper


## Helpful SQL:
```SQL
-- if you end a run in the middle of scraping, some results will still be marked as 'CURRENTLY_SCRAPING'
-- cleanup with the following:
UPDATE urls_to_scrape SET scraped_yet = 0 WHERE scraped_yet = 'CURRENTLY_SCRAPING';
UPDATE urls_to_scrape SET scraped_yet = 0 WHERE scraped_yet = 'FAILED';

select distinct scraped_yet from urls_to_scrape limit 5;

select count(distinct urls) from urls_to_scrape;
select count(distinct *) from urls_to_scrape; -- should be the same number as the line above

select count(distinct url) from properties; -- number of distinct properties scraped (some may have accidentally been scraped twice)

-- How many not scraped
 select count(url) from urls_to_scrape
 where url not in (select distinct url from properties);


-- clean data
delete from properties where price_per_month_gbp is NULL;
delete from properties where description is NULL;

UPDATE urls_to_scrape SET scraped_yet = 0 WHERE url not in (select distinct url from properties);

-- Distinct roots of URLs to be scraped
select distinct substr(url,0,42) as url_root, count(*) from urls_to_scrape group by url_root limit 25;

-- Distinct websites that properties were scraped from
select distinct substr(url,0,42) as url_root, count(*) from properties group by url_root limit 25;
```

## MacOS multi-threading Issue
If multi-threading is enabled you may run into an issue on newer versions of macOS
```
[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.
```
Details and fix here: 
https://stackoverflow.com/questions/50168647/multiprocessing-causes-python-to-crash-and-gives-an-error-may-have-been-in-progr

In Bash:
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

In Fish:
set -x OBJC_DISABLE_INITIALIZE_FORK_SAFETY YES



postgres