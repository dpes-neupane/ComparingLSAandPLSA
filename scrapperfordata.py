import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re



def scrapperForRatopati(URL = "https://ratopati.com/", category = "literature", save_in="Literature"):

    page = requests.get(URL +"category/" + category)

    soup  = BeautifulSoup(page.content, "html.parser")

    total_pages_raw_text = soup.find("div", class_="page-numbers disabled") #finds the tatal pages element
    total_pages = total_pages_raw_text.text.split()[-1]
    print(total_pages)
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
            filename = now.strftime("%d_%m_%y_%H_%M_%S") + news.find("a", href=True)['href'].split("/") [-1]
            with open(".\\16NepaliNews\\16719\\raw\\" + save_in + "\\" + filename + ".txt", 'w', encoding='utf-8') as wp: # --not a good way but it works
                wp.write(main_.text)


    
def scrapperForOnlineKhabar(URL = "https://www.onlinekhabar.com/", category = "literature", save_in="Literature"):
    page = requests.get(URL +"content/" + category) #can have different urls for different categories, so change as per need

    soup  = BeautifulSoup(page.content, "html.parser")
    # print(page.content)
    next_page_link = soup.find("a", class_="next page-numbers") #find link to next page
    print(next_page_link['href'])
    i = 0
    while next_page_link is not None and i != 30: #get only 20 pages of links
        all_link_stories = soup.select(".span-4 > .ok-news-post > a")
        for link in all_link_stories:
            print(link['href'])
            news_page = requests.get(link['href'])
            news_soup = BeautifulSoup(news_page.content, 'html.parser')
            news_text = news_soup.find("div", class_=re.compile("ok18-single-post-content-wrap")) #the divs with news text all belong to this class but also have others classes assigned to them
            # print(news_text.text)
            now = datetime.now()
            filename = now.strftime("%d_%m_%y_%H_%M_%S") + link['href'][-6:]
            with open(".\\16NepaliNews\\16719\\raw\\" + save_in + "\\" + filename + ".txt", 'w', encoding='utf-8') as wp: #saving 
                wp.write(news_text.text)

        next_page = requests.get(next_page_link['href']) #go to next page
        soup = BeautifulSoup(next_page.content, 'html.parser')
        next_page_link = soup.find("a", class_ = "next page-numbers")
        all_link_stories = []
        print(next_page_link['href'])
        i += 1
    

        
    

# scrapperForRatopati()
# scrapperForOnlineKhabar()