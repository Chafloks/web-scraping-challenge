from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import requests

def scrape():
    # Path and driver set up
    path = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(path)
    # NASA Mars News
    driver.get("https://mars.nasa.gov/news/")
    time.sleep(5)
    # Get Headers
    contents = driver.find_elements_by_class_name("content_title")
    res = []
    Headers = [] 
    for content in contents:
        text = content.text
        if text != '' :
            res.append(text)
    for i in res: 
        if i not in Headers: 
            Headers.append(i) 
    # Get description
    contents2 = driver.find_elements_by_class_name("article_teaser_body")
    res = []
    Description = [] 
    for content in contents2:
        text = content.text
        if text != '' :
            res.append(text)

    for i in res: 
        if i not in Description: 
            Description.append(i) 

    news_title = Headers[0]
    news_p = Description[0]

    # JPL Mars Space Images - Featured Image
    driver = webdriver.Chrome(path)
    driver.get("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    time.sleep(5)
    full_image = driver.find_element_by_id('full_image')
    full_image.click()
    time.sleep(5)
    image = driver.find_element_by_class_name("fancybox-image").get_attribute("src")
    time.sleep(5)
    
    # Mars Facts
    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    df = pd.DataFrame(tables[0])
    df.columns=['Mars','Data']
    mars_table = df.set_index("Mars")
    MarsTable = mars_table.to_html(classes='MarsTable')
    MarsTable = MarsTable.replace('\n', ' ')
    time.sleep(5)
    # Mars Hemispheres

    driver = webdriver.Chrome(path)
    driver.get("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    time.sleep(5)
    img1_title = driver.find_elements_by_tag_name('h3')[0].text
    img2_title = driver.find_elements_by_tag_name('h3')[1].text
    img3_title = driver.find_elements_by_tag_name('h3')[2].text
    img4_title = driver.find_elements_by_tag_name('h3')[3].text
    images = driver.find_elements_by_class_name('thumb')
    img1 = images[0]
    img1.click()
    time.sleep(2)
    img1_url =driver.find_element_by_link_text('Sample').get_attribute("href")
    driver.back()
    time.sleep(2)
    images = driver.find_elements_by_class_name('thumb')
    img2 = images[1]
    img2.click()
    time.sleep(2)
    img2_url =driver.find_element_by_link_text('Sample').get_attribute("href")
    driver.back()
    time.sleep(2)
    images = driver.find_elements_by_class_name('thumb')
    img2 = images[2]
    img2.click()
    time.sleep(2)
    img3_url =driver.find_element_by_link_text('Sample').get_attribute("href")
    driver.back()
    time.sleep(2)
    images = driver.find_elements_by_class_name('thumb')
    img2 = images[3]
    img2.click()
    time.sleep(2)
    img4_url =driver.find_element_by_link_text('Sample').get_attribute("href")
    driver.back()
    hemisphere_image_urls = [
        {"title":img1_title,"img_url":img1_url},
        {"title":img2_title,"img_url":img2_url},
        {"title":img3_title,"img_url":img3_url},
        {"title":img4_title,"img_url":img4_url}
    ]
    mars_data = {
        "Header": news_title,
        "Description": news_p,
        "FullImage": image,
        "Facts": MarsTable,
        "Hems": hemisphere_image_urls
    }
    return mars_data