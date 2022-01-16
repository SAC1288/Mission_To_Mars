from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import lxml as lxml

executable_path = {'executable_path': ChromeDriverManager().install()}

def scrape():
    data = {}
    browser = Browser('chrome', **executable_path, headless=False)
    title,paragraph = news(browser)
    data['title'] = title
    data['paragraph'] = paragraph
    data['image'] = image(browser)

    return data

def news(browser):
    url = 'https://redplanetscience.com'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    news_title = slide_elem.find('div', class_='content_title').get_text()
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    return news_title, news_p

def image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url


def facts():
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    return df.to_html()

def hemi(browser):


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[20]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[21]:


slide_elem.find('div', class_='content_title')


# In[22]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[23]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# In[24]:


### JPL Space Images Featured Image


# In[25]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[26]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[27]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[28]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[29]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[30]:


### Mars Facts


# In[31]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[32]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[33]:


df.to_html()


# In[34]:


# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles


# In[35]:


### Hemispheres


# In[50]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[37]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.


# In[56]:


for i in range(4):
    hemisphere = {}
    browser.find_by_css("img.thumb")[i].click()
    hemisphere['title'] = browser.find_by_tag('h2').text
    hemisphere['url'] = browser.find_by_text('Sample')['href']
    hemisphere_image_urls.append(hemisphere)
    browser.back()


# In[57]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[39]:


# 5. Quit the browser
browser.quit()

