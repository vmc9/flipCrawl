# flipCrawl
A simple python web crawling script for flipboard magazines

# set up
## libraries required
pip install selenium

pip install beautifulsoup 4

## additional requirements
download chrome web driver from https://chromedriver.chromium.org/downloads

place webdriver in the script directory

make sure path matches line 43 of the script

make sure the driver version matches your chrome version

## spider paths
make sure the flipboard magazine names and their corresponding urls are up to date
in the dict starting at line 7 of the script

## run script
run the python file, selenium will open up the headless browser on its own and pass the
pages to bs4 for parsing and extraction

csv files will be generated or updated for each magazine in the dict automatically

