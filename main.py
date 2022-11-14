# This is my second project on HyperSkill, WebScrapper
# it should parsing Nature.com and select user selected topics
# then it should download it and save topics texts and save in
# files

import os
import requests
import bs4
import string

user_page_count = int(input())
article_type = input()


def download_content(url):
    """Function that download page and put in web_data if ok, else return False"""
    global web_data
    web_data = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if web_data:
        return True
    else:
        print("The URL returned", web_data.status_code)


for page_number in range(1, user_page_count+1):
    if not os.access(f"./page_{page_number}", os.R_OK):
        os.mkdir(f"Page_{page_number}")

    url = f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page_number}"

    # check input url and go download and process if al ok
    if download_content(url):
        sci_content = bs4.BeautifulSoup(web_data.content, "html.parser")

        # parse all articles on the page and select only chosen type of articles
        for sci_step in sci_content.find_all('article'):
            if sci_step.find('span', {'data-test': 'article.type'}).text.replace("\n", "") == article_type:

                # get Article header inside A href & replace all puncuation from punctuation list
                sci_title = sci_step.find('a').text.translate(str.maketrans('', '', string.punctuation))
                sci_title = sci_title.replace(" ", "_")
                # print Article header processed  title
                print(sci_title)

                # this is url
                url = "https://www.nature.com"+sci_step.find('a')['href']

                web_data_art = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
                print(url)
                sci_news_content = bs4.BeautifulSoup(web_data_art.content, "html.parser")
                sci_sel_news_text = sci_news_content.find('div', attrs={'class': 'c-article-body main-content'})

                bin_text = sci_sel_news_text.text.encode("utf-8")
                # if not os.access(f"./page_{page_number}", os.R_OK):
                #     os.mkdir(f"Page_{page_number}")
                file = open(f"Page_{page_number}\{sci_title}.txt", "wb")
                if file.write(bin_text):
                    print("article saved")
                file.close()
