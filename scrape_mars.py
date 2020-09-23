#Import dependencies
from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import os
import time



# ### NASA Mars News
# 
# - Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# - Assign the text to variables that you can reference later.
#Getting the NASA news Page and parsing the file.
def scrape():
    page = requests.get('https://mars.nasa.gov/news/')
    soup = bs(page.content, 'html.parser')
    title = soup.find_all('title')[0].text
    paragraph = soup.find_all('p')[0].text


    # ### JPL Mars Space Images - Featured Image
    # - Visit the url for JPL Featured Space Image here.
    # - Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # - Make sure to find the image url to the full size .jpg image.
    # - Make sure to save a complete url string for this image.
    #Splinter chromedriver setup

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    time.sleep(3)

    btn = browser.find_by_id('full_image')
    btn.click()

    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()

    html = browser.html
    img_soup = bs(html, 'html.parser')
    img_url_rel = img_soup.select_one('figure.lede a img').get('src')
    img_url = f'https://jpl.nasa.gov{img_url_rel}'
    

    # ### Mars Facts
    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    #Read website URL using pandas
    url = 'https://space-facts.com/mars/'
    d = pd.read_html(url)

    #Converted the table to an html file
    d[0].columns = ['Description', 'Values']
    facts = d[0].to_html()
    

    # ### Mars Hemispheres
    # - Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    # - You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # - Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    # - Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    time.sleep(3)

    links = browser.find_by_css('a.product-item h3')
    hemisphere_image_urls = []

    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css('a.product-item h3')[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
        
    browser.quit()

    mars_data = {
        'title': title,
        'paragraph': paragraph,
        'featured_img' : img_url,
        'fact_table' : facts,
        'hemi': hemisphere_image_urls
    }
    return mars_data 


