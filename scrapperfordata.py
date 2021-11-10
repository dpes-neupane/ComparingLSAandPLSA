import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from selenium import webdriver
import re
import time
import os


def scrapperForRatopati(URL = "https://ratopati.com/", category = "literature", save_in="Literature"):

    page = requests.get(URL +"category/" + category)

    soup  = BeautifulSoup(page.content, "html.parser")

    total_pages_raw_text = soup.find("div", class_="page-numbers disabled") #finds the tatal pages element
    total_pages = total_pages_raw_text.text.split()[-1]
    print(total_pages)
    if not os.path.isdir(".\\16NepaliNews\\16719\\raw\\" + save_in):
        os.makedirs(".\\16NepaliNews\\16719\\raw\\" + save_in)
    for i in range(1, int(total_pages)):# go to each page 
        next_page_link = soup.find("a", class_="next page-numbers", href=True)
        print(next_page_link['href'])
        page = requests.get(URL +"category/"+ category + next_page_link['href']) #goes to next page
        soup  = BeautifulSoup(page.content, "html.parser")
        all_news_stories_link = soup.find_all("div", class_="item-content") #finds all links with class "item-content"
        for news in all_news_stories_link: #goes to each link in each page of the category
            print(news.find("a", href=True)['href'])
            news_page = requests.get(URL +  news.find("a", href=True)['href'] )
            news_soup = BeautifulSoup(news_page.content, "html.parser")
            main_ = news_soup.find("div", class_="ratopati-table-border-layout") #gets the text which is in div with class "ratopati-border-layout"
            now = datetime.now()
            filename = now.strftime("%d_%m_%y_%H_%M_%S") + news.find("a", href=True)['href'].split("/") [-1] + 'ratopati'
            with open(".\\16NepaliNews\\16719\\raw\\" + save_in + "\\" + filename + ".txt", 'w', encoding='utf-8') as wp: # --not a good way but it works
                wp.write(main_.text)
            time.sleep(1)#sleep to give way for same filename to be different -- can be changed to a better solution

    
def scrapperForOnlineKhabar(URL = "https://www.onlinekhabar.com/", category = "literature", save_in="Literature"):
    page = requests.get(URL +"content/" + category) #can have different urls for different categories, so change as per need

    soup  = BeautifulSoup(page.content, "html.parser")
    # print(page.content)
    next_page_link = soup.find("a", class_="next page-numbers") #find link to next page
    print(next_page_link['href'])
    i = 0
    if not os.path.isdir(".\\16NepaliNews\\16719\\raw\\" + save_in):
        os.makedirs(".\\16NepaliNews\\16719\\raw\\" + save_in)
    while next_page_link is not None and i != 30: #get only 20 pages of links
        all_link_stories = soup.select(".span-4 > .ok-news-post > a")
        for link in all_link_stories:
            print(link['href'])
            news_page = requests.get(link['href'])
            news_soup = BeautifulSoup(news_page.content, 'html.parser')
            news_text = news_soup.find("div", class_=re.compile("ok18-single-post-content-wrap")) #the divs with news text all belong to this class but also have others classes assigned to them
            # print(news_text.text)
            now = datetime.now()
            filename = now.strftime("%d_%m_%y_%H_%M_%S") + link['href'][-6:] + "onlnkhbr"
            with open(".\\16NepaliNews\\16719\\raw\\" + save_in + "\\" + filename + ".txt", 'w', encoding='utf-8') as wp: #saving 
                wp.write(news_text.text)

        next_page = requests.get(next_page_link['href']) #go to next page
        soup = BeautifulSoup(next_page.content, 'html.parser')
        next_page_link = soup.find("a", class_ = "next page-numbers")
        all_link_stories = []
        print(next_page_link['href'])
        i += 1
    

def scrapperForEkantipur(URL="https://ekantipur.com/", category="literature", save_in="Literature"):
    if not os.path.isdir(".\\16NepaliNews\\16719\\raw\\" + save_in):
        os.makedirs(".\\16NepaliNews\\16719\\raw\\" + save_in)
    options = webdriver.ChromeOptions() 
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options, service=Service("C:\\chromedriver.exe"))
    driver.get(URL + category)
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(last_height)
    i = 1
    while  i < 40: #change this to true if you need to go to the end of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(new_height)
        if new_height == last_height:
            break 
        last_height = new_height 
        i+=1
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    main_tag = soup.select_one("main > section.listLayout")
    links_parent = main_tag.find_all("h2")
    for link_ in links_parent:
        link = link_.find("a")['href']
        if link[0] == "/":
            link = "https://ekantipur.com" + link
        print(link)
        news_page = requests.get(link) 
        news_soup = BeautifulSoup(news_page.content, 'html.parser')
        news_text_parent = news_soup.select_one("main>article")
        news_text_list = news_text_parent.find_all("p")
        now = datetime.now()
        filename = now.strftime("%d_%m_%y_%H_%M_%S") + "kantipur" + link.split('/')[-1].split('.')[0] 
        with open(".\\16NepaliNews\\16719\\raw\\" + save_in + "\\" + filename + ".txt", 'w', encoding='utf-8') as wp: #saving 
            for para in news_text_list:
                wp.write(para.text)
            
        
       

