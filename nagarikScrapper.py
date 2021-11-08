import requests
import os
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Edge
url="https://nagariknews.nagariknetwork.com/"
category="interview"
save_in="interview"

driver = Edge()

##options = EdgeOptions()
##options.use_chromium = True
##
##driver = Edge(options = options)

##dir = os.path.dirname(__file__)
##edge_path = dir + "\msedgedriver.exe"
##driver = webdriver.Edge(edge_path)
####driver.implicitly_wait(10)

driver.get(url+category)
driver.maximize_window()
driver.implicitly_wait(10)

Actions action = new Actions(driver);
close=action.moveToElement(driver.findElement(By.cssSelector("span.rm_ad fa fa-times"))).build().perform();
close.click()
##close=driver.find_element(By.CSS_SELECTOR, "span.rm_ad fa fa-times::before")
##close.click()

while True:
    try:
        loadmore= driver.find_element(By.ID,"loadmore")
        loadmore.click()
        driver.implicitly_wait(5)

    except NoSuchElementException:
        print("End of the page")
        break

soup= BeautifulSoup(driver.page_source, 'html.parser')

links=soup.select(".list-group-item > .image > figure > a")
print(url+links[0]['href'])
article=requests.get(url+links[0]['href'])
article_soup=BeautifulSoup(article.content, 'html.parser')
text=article_soup.find("article")
print(text.text)
##now = datetime.now()
##filename = now.strftime("%d_%m_%y_%H_%M_%S_") + links[0]['href'][-10:]
##with open(".\\"+ filename + ".txt", 'w', encoding='utf-8') as wp:
##    wp.write(text.text)


