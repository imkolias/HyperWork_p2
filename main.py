# This is my second project on HyperSkill, WebScrapper
# it should parse Nature.com and select user selected topics
# then it should download it and save topics texts and save in
# files (each page in different directory)

import os
import requests
import bs4
import string

web_page_data = ""

user_page_count = int(input())
article_type = input()


def download_content(url):
    """Function that download page with article list and put in web_page_data if ok, else return False"""
    global web_page_data
    web_page_data = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if web_page_data:
        return True
    else:
        print("The URL returned", web_page_data.status_code)


# we start our path thought pages from first(1) to page number that user input in the beginning
for page_number in range(1, user_page_count+1):

    # Create directory for page number. That part code here, because the task
    # checks whether there is a folder, regardless of the presence of news in it.
    if not os.access(f"./page_{page_number}", os.R_OK):
        os.mkdir(f"Page_{page_number}")

    # check input url and go download and process if al ok
    if download_content(f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page_number}"):
        sci_content = bs4.BeautifulSoup(web_page_data.content, "html.parser")

        # parse all articles on the page and select only chosen type of articles
        for sci_step in sci_content.find_all('article'):
            if sci_step.find('span', {'data-test': 'article.type'}).text.replace("\n", "") == article_type:

                # get Article header inside A href & replace all punctuation from punctuation list
                sci_title = sci_step.find('a').text.translate(str.maketrans('', '', string.punctuation))
                sci_title = sci_title.replace(" ", "_")

                # print Article header processed title
                print(sci_title)

                # this is url
                article_url = "https://www.nature.com"+sci_step.find('a')['href']
                print(article_url)
                article_page_data = requests.get(article_url, headers={'Accept-Language': 'en-US,en;q=0.5'})

                sci_news_content = bs4.BeautifulSoup(article_page_data.content, "html.parser")
                sci_sel_news_text = sci_news_content.find('div', attrs={'class': 'c-article-body main-content'})

                bin_data = sci_sel_news_text.text.encode("utf-8")

                # write binary Article data to file
                file = open(f"Page_{page_number}\{sci_title}.txt", "wb")
                if file.write(bin_data):
                    print("Article saved")
                file.close()
