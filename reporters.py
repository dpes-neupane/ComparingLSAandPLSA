import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re



##def scrapperForRatopati(URL = "https://ratopati.com/", category = "interview", save_in="interview"):
##
##    page = requests.get(URL +"category/" + category)
##
##    soup  = BeautifulSoup(page.content, "html.parser")
##
##    total_pages_raw_text = soup.find("div", class_="page-numbers disabled") #finds the tatal pages element
##    total_pages = total_pages_raw_text.text.split()[-1]
##    print(total_pages)
##    for i in range(1, int(total_pages)):# go to each page 
##        next_page_link = soup.find("a", class_="next page-numbers", href=True)
##        print(next_page_link['href'])
##        page = requests.get(URL +"category/"+ category + next_page_link['href']) #goes to next page
##        soup  = BeautifulSoup(page.content, "html.parser")
##        all_news_stories_link = soup.find_all("div", class_="item-content") #finds all links with class "item-content"
##        for news in all_news_stories_link: #goes to each link in each page of the category
##            print(news.find("a", href=True)['href'])
##            news_page = requests.get(URL+news.find("a", href=True)['href'] )
##            news_soup = BeautifulSoup(news_page.content, "html.parser")
##            main_ = news_soup.find("div", class_="ratopati-table-border-layout") #gets the text which is in div with class "ratopati-border-layout"
##            now = datetime.now()
##            filename = now.strftime("%d_%m_%y_%H_%M_%S")
##            with open(".\\scrapped\\raw\\" + save_in + "\\" + filename + ".txt", 'w', encoding='utf-8') as wp:
##                wp.write(main_.text)
##
##scrapperForRatopati()
    
def forReporters(URL = "https://www.reportersnepal.com/", category = "interview", save_in="interview"):
    page = requests.get(URL +"category/" + category) #can have different urls for different categories, so change as per need

    soup  = BeautifulSoup(page.content, "html.parser")
    # print(page.content)
    next_page_link = soup.select_one("ul.pagination.pagination-sm > li.page-item > i.page-link > a")
    print(next_page_link['href'])
    i = 0
    while next_page_link is not None and i != 100: #get only 20 pages of links
        all_link_stories = soup.select("div.container > div.row.category > div.col-md-8.text-justify > a.post-list.d-flex")
        for link in all_link_stories:
            print(link['href'])
            news_page = requests.get(link['href'])
            news_soup = BeautifulSoup(news_page.content, 'html.parser')
            news_text = news_soup.find("article", class_=re.compile("post-entry")) #the divs with news text all belong to this class but also have others classes assigned to them
##            print(news_text.text)
            now = datetime.now()
            filename = now.strftime("%d_%m_%y_%H_%M_%S") + link['href'][-6:]
            with open(".\\" + save_in + "\\" + filename + ".txt", 'w', encoding='utf-8') as wp: #saving 
                wp.write(news_text.text)
        
        next_page = requests.get(next_page_link['href']) #go to next page
        soup = BeautifulSoup(next_page.content, 'html.parser')
        next_page_link= soup.select("ul.pagination.pagination-sm > li.page-item > i.page-link > a")[-1]
        all_link_stories = []
        print(next_page_link['href'])
        i += 1

forReporters()    
