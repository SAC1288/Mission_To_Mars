#!/usr/bin/env python
# coding: utf-8

#Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import lxml as lxml
import datetime as dt

def scrape_all():
    #Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in a dictionary.
    data = {
     "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()   
    }

    #Stop webdriver and reurn data
    browser.quit()
    return data

def mars_news(browser):

    #Scrape Mars News
    #Assigning URL and instructing browser to visit it
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    
    #Optional delay for loading the page.
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #COnvert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')

        #use the parent elementt to find the firstt 'a' tag and save i as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        #Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None 
    
    return news_title, news_p

def featured_image(browser):

    #Visit URL for images
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    #FIdn and click the full image button.
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #add try/except for error handling
    try:
    # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    
    return img_url

def mars_facts():
    #Add try/except for error handling
    try:

        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None
    #Assign columns and set index of data frame

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

#convert datafram to HTML format
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    #IF running as script, print scraped data
    print(scrape_all())