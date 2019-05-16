#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import numpy as np
import pandas as pd
import re
import datetime as dt
import time
import datetime
from dateutil.relativedelta import relativedelta
from pprint import pprint


mars_info_dict=dict()

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)

    executable_path = {'executable_path': 'chromedriver.exe'}
    #executable_path = {'executable_path': 'C:\ChromeSafe\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

def mars_scrape():

    #def scrape_info():

    browser = init_browser()

    # Visit NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    #print(soup.prettify())

    # Get the News
    news_titles = soup.find('div', class_='content_title').get_text()
    news_body = soup.find('div', class_="article_teaser_body").get_text()

    mars_info_dict['Mars_news_title'] = news_titles
    mars_info_dict['Mars_news_body'] = news_body

    # JPL Mars space Images
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    full_image_elem = browser.find_by_id("full_image")
    full_image_elem.click()
    browser.is_element_present_by_text("more info",wait_time = 1)
    more_info_elem = browser.find_link_by_partial_text("more info")
    more_info_elem.click()
        
    featured_image_url = soup.select_one("figure.lede a img").get("src")
    image_url = f'https://www.jpl.nasa.gov{featured_image_url}'
        
    featured_image_url=image_url

    # Append featured image url to the Mars dictionary.

    mars_info_dict["Mars_featured_image_url"] = featured_image_url

    # Mars Weather
    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page.
    # Save the tweet text for the weather report as a variable called mars_weather.

    browser = init_browser()
    # Visit NASA Mars News Site
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    
    mars_weather= soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text

    #Add weather tweet to the mars_info dict.
    mars_info_dict["Mars_tweet_weather"] = mars_weather
    # pprint(mars_info_dict)


    url4 = "http://space-facts.com/mars/"
    df_Mars_all_Facts = pd.read_html(url4)
    df_marsfacts = df_Mars_all_Facts[0]


    # Rename columns of the dataframe. 
    df_marsfacts.columns = ['Mars_Facts', 'Values']
    df_marsfacts

    #convert DataFrame to html
    df_marsfacts.to_html("mars_facts.html", index=False)

    #Add index to Dataframe for better retrieval. 
    df_marsfacts.set_index("Mars_Facts")

    #html version of the Mars facts tables.
    mars_facts_html = df_marsfacts.to_html(classes="mars_facts table table-striped")
    mars_info_dict["Mars_facts_table"] = mars_facts_html

    # pprint(mars_info_dict)

    url5 =  "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/"
    browser.visit(url5)
    time.sleep(10)
    html5 = browser.html
    soup5 = bs(html5, "html.parser")

    class_collap_results = soup5.find('div', class_="collapsible results")
    hemis_items = class_collap_results.find_all('div',class_='item')



    #loop thru to find tile and the image urls to append to lists. 
    hemis_img_urls_list=list()
    img_urls_list = list()
    title_list = list()
    for h in hemis_items:
        #save title
        h_title = h.h3.get_text()
        title_list.append(h_title)
        
        # find the href link.
        h_href  = "https://astrogeology.usgs.gov" + h.find('a',class_='itemLink product-item')['href']
        
        #print(h_title,h_href)
        
        #browse the link from each page
        browser.visit(h_href)
        time.sleep(5)
        #Retrieve the  image links and store in a list. 
        html5   = browser.html
        soup_img = bs(html5, 'html.parser')
        h_img_url = soup_img.find('div', class_='downloads').find('li').a['href']
        
        img_urls_list.append(h_img_url)
                
        # create a dictionary with  each image and title and append to a list. 
        hemispheres_dict = dict()
        hemispheres_dict['title'] = h_title
        hemispheres_dict['img_url'] = h_img_url
        
        hemis_img_urls_list.append(hemispheres_dict)
        

    #Add hemispheres list  to the mars_info dictionary.
    mars_info_dict["Hemisphere_image_urls"] = hemis_img_urls_list



    #Generate date time and store in the dictionary.
    cur_datetime = datetime.datetime.utcnow()
    mars_info_dict["Date_time"] = cur_datetime

    pprint(mars_info_dict)

    mars_return_dict =  {
        "News_Title": mars_info_dict["Mars_news_title"],
        "News_Summary" :mars_info_dict["Mars_news_body"],
        "Featured_Image" : mars_info_dict["Mars_featured_image_url"],
        "Weather_Tweet" : mars_info_dict["Mars_tweet_weather"],
        "Facts" : mars_facts_html,
        "Hemisphere_Image_urls": hemis_img_urls_list,
        "Date" : mars_info_dict["Date_time"],
    }
    return mars_return_dict


