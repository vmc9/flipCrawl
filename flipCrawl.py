import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup

# Dictionary of Magazines
magazines = {
    "startups": "https://flipboard.com/@sconnexions/startups-6q42rjd9z",
    "IoT": "https://flipboard.com/@sconnexions/internet-of-things-(iot)-08aq40osz",
    "scienceEnvironment": "https://flipboard.com/@sconnexions/sciences-connexions---environnement-48cqponqz",
    "blockchain": "https://flipboard.com/@sconnexions/blockchain-74gnm8gbz",
    "ux": "https://flipboard.com/@sconnexions/ux-(user-experience)-pehj9g0hz",
    "digitalTransformation": "https://flipboard.com/@sconnexions/digital-transformation-818s5iv1z",
    "digitalContinuous": "https://flipboard.com/@sconnexions/digital-continuous-improvement-m1rikuphz",
    "aeroMTL": "https://flipboard.com/@sconnexions/montreal%27s-aero-digital-ecosystem-126lovekz",
    "wearables": "https://flipboard.com/@sconnexions/wearables-kabn6beqz",
    "exoskeletons": "https://flipboard.com/@sconnexions/exoskeletons-bd6nr3nkz",
    "additiveManufacturing": "https://flipboard.com/@sconnexions/additive-manufacturing-j9ustp35z",
    "cybersecurity": "https://flipboard.com/@sconnexions/cybersecurity-lg789ov9z",
    "ar": "https://flipboard.com/@sconnexions/augmented-reality-usv9e6vmz",
    "plm": "https://flipboard.com/@sconnexions/product-lifecycle-management-(plm)-jdf1p3tvz",
    "cloudComputing": "https://flipboard.com/@sconnexions/cloud-computing-obne0gjnz",
    "data&analytics": "https://flipboard.com/@sconnexions/data-and-analytics-l4v7vm0jz",
    "agile": "https://flipboard.com/@sconnexions/agile-ruld40jhz",
    "web": "https://flipboard.com/@sconnexions/web-development-qcg9fmjdz",
    "digitalTech": "https://flipboard.com/@sconnexions/digital-technology-watch-r7i52qs0z",
    "ai": "https://flipboard.com/@sconnexions/artificial-intelligence-r7pcqfuqz",
    "quantum": "https://flipboard.com/@sconnexions/quantum-computing-3g0n38msz",
    "aeroTechnology": "https://flipboard.com/@sconnexions/aerospace-technology-watch-70m3do2dz",
    "science": "https://flipboard.com/@sconnexions/sciences-connexions-pl0h8r52z",
    "candidates": "https://flipboard.com/@sconnexions/candidates-for-digital-technology-watch-oe3lr4kaz"
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
