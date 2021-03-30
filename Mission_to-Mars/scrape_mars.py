from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse 
    soup = BeautifulSoup(response.text, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list
    results = soup.find_all('div', class_='slide')
    print(type(results))

    first_news = results[0]
    first_news

    # Loop through returned results
    for result in results:
        # Error handling
        try:
            # Identify and return title of listing
            news_title = result.find('div', class_='content_title').text
            # Identify and return paragraph of listing
            news_p = result.find('div', class_='rollover_description_inner').text

            # Run only if title, price, and link are available
            if (news_title and news_p):
                # Print results
                print('-------------')
                print(news_title)
                print(news_p)

                # Dictionary to be inserted as a MongoDB document
                #post = {
                #    'Title': news_title,
                #    'Paragraph': news_p,
                #}

                #collection.insert_one(post)

        except Exception as e:
            print(e)

    img_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(img_url)
    html= browser.html
    img_soup = BeautifulSoup(html,'html.parser')
    urlb = img_soup.find('img', class_="headerimage")['src']
    featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{urlb}"

    url = "https://space-facts.com/mars/"
    facts_tables = pd.read_html(url)[0].to_html()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    hemi_soup = BeautifulSoup(html, 'html.parser')
    banners_tag = hemi_soup.find_all('h3')
    banners = [x.text for x in banners_tag]
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemispheres = []
    for i in range(len(banners)):
        hemisphere = {}
        browser.visit(url)
        browser.find_by_css('h3')[i].click()
        hemisphere["title"] = [banners[i]]
        hemisphere["img_url"] = browser.find_by_text('Sample')['href']
        
        hemispheres.append(hemisphere)
        browser.back()

    # Store data in a dictionary
    mars_data ={
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "facts_table": facts_tables,
        "hemispheres": hemispheres
    }

    browser.quit()

    return mars_data