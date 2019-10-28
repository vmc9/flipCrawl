import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup

# Dictionary of Magazines
magazines = {
    # magazine name : magazine url
}

# Iteration over all Magazines
for name, magazine in magazines.items():

    # Format for csv file name
    fileName = "{}.csv".format(name)

    # Chromedriver is required for Selenium to manipulate the browser
    # https://chromedriver.chromium.org/downloads
    # Chromedriver must match Chrome Browser version
    browser = webdriver.Chrome('./chromedriver')
    browser.get(magazine)

    # Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.
    # It will continue to do this until the page stops loading new data.
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var "
                                       "lenOfPage=document.body.scrollHeight;return lenOfPage;")
    print(lenOfPage)

    # Selenium command to find the "Load More" button and continue loading infinite scroll
    if lenOfPage > 7000:
        loadButton = browser.find_element_by_xpath("//div[@class='load-more']/button")
        loadButton.click()

    # Loop to reach bottom of the page
    match = False
    while not match:
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var "
                                           "lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

    # Soup parsing
    loaded_page = browser.page_source
    soup = BeautifulSoup(loaded_page, "html.parser")

    # Finding posts
    posts = soup.find_all('div', attrs={"class": "post__body"})

    # Extracting information and writing to csv
    with open(fileName, encoding='utf-8', mode='w') as pageFile:
        writer = csv.writer(pageFile, delimiter=',')
        for post in posts:

            # Article title
            postTitle = post.find(class_='post__title')

            # Protect against broken posts
            if postTitle is not None:
                titleText = postTitle.find('a').contents[0]

                # Protect against broken titles
                if titleText is not None:
                    # Article publisher
                    postPublisher = post.find(class_='post-attribution__source')

                    # Protect against broken publisher links
                    if postPublisher is not None:
                        publisherInfo = postPublisher.find('a').contents

                        # Offset in case publisher div includes an icon
                        if len(publisherInfo) > 1:
                            publisherText = publisherInfo[1]
                        else:
                            publisherText = publisherInfo[0]

                        # Article link
                        postLink = postPublisher.find('a').get('href')

                        # Writing  extracted data to csv
                        print(titleText, "\n", publisherText, "\n", postLink, "\n")
                        writer.writerow([titleText, publisherText, postLink])
    pageFile.close()
