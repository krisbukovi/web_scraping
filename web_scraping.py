# filename: web_scraping.py
# author: kris bukovi
# last modified: July 13, 2018
# purpose: to scrape data using BeautifulSoup 

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import time
from user_agent import generate_user_agent
import math
import numpy as np
import pandas as pd

# class definition for news 
class News:

    def __init__(self, proxies):

        # intializing instance variables 
        self.highlights = []
        self.proxies = proxies
        
        
    # getter method to return highlights      
    def get_highlights(self):
        return self.highlights

    # setters to modify highlights
    def set_highlights(self, s):
        self.highlights = s

    # display highlights
    def display_highlights(self):
        cols = ["Time", "Headline", "Link"]
        rows = ["0", "1", "2", "3", "4"]
        print(pd.DataFrame(self.highlights.T, columns=cols, index=rows))
    
    # method to scrape web to get CSPAN highlights 
    def scrape_highlights(self):

        # url array
        url = []
        url.append("https://www.c-span.org/")

        for i in url:

            # GET request to URL
            # returns None is request fails
            def simple_get(url):
                try:
                    with closing(get(url, stream=True)) as resp:
                        if is_good_response(resp):
                            return resp.content
                        else:
                            return None

                except RequestException as e:
                    log_error('Error during requests to {0} : {1}'.format(url, str(e)))
                    return None


            def is_good_response(resp):
                content_type = resp.headers['Content-Type'].lower()
                return (resp.status_code == 200 
                        and content_type is not None 
                        and content_type.find('html') > -1)


            def log_error(e):
                print(e)

            headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

            raw_html = get(i, proxies=self.proxies, headers=headers, timeout=7)

            # time.sleep(0.5)

            # if raw_html != None:
            if raw_html.status_code == 200:

                # html = BeautifulSoup(raw_html, 'html.parser')
                html = BeautifulSoup(raw_html.text, 'html.parser')
                
                # print(html.prettify())

                if i == url[0]:

                    links = []
                    text = []
                    times = []

                    # html_section = (html.find_all('ul', class_='schedule')[0].getText())
                    # print(html_section)
                    
                    # html_list_items = (html.find_all('span', class_='time highlights'))
                    

                    # text = html_section.split("\n\n")
                    # print(text)

                    html_section = html.find_all('span', class_='time highlights')

                    i = 0

                    for h in html_section:

                        # get links
                        a = h.find('a').attrs['href']
                        links.append(a[2:])

                        # get titles
                        b = h.find('span').getText()
                        text.append(b)

                        # get times
                        c = html_section[i].getText()
                        temp_times, x = c.split(" EDT")
                        times.append(temp_times)

                        i+=1

                    '''
                    print("\nlinks")
                    print("\n".join(links))

                    print("\ntext")
                    print("\n".join(text))

                    print("\ntimes:")
                    print("\n".join(times))
                    '''


                    highlights = np.array([times, text, links])
                    self.set_highlights(highlights)
                            
              
                #elif i == url[1]:
                #elif i == url[2]:

            else:
                print(raw_html.status_code)

def main():

    proxies = [{'http' : '109.111.83.67:53281',  'https': '81.217.94.83:8080'}, 
        {'http' : '95.143.108.195:41258',  'https': '80.97.64.58:8080'}, 
        {'http' : '168.232.197.194:6666',  'https': '212.47.252.91:8118'}, 
        {'http' : '190.186.59.22:52335',  'https': '61.247.189.22:8080'}, 
        {'http' : '181.129.183.19:53281',  'https': '119.110.69.130:65103'}, 
        {'http' : '212.47.239.33:80',  'https': '93.179.66.57:8080'}, 
        {'http' : '36.66.169.18:8080',  'https': '62.249.156.13:53281'},
        {'http' : '181.52.238.94:53281',  'https': '180.249.4.60:80'}, 
        {'http' : '45.70.238.21:53281',  'https': '185.158.65.115:41258'}, 
        {'http' : '41.73.251.98:8080',  'https': '94.232.34.121:41258'}, 
        {'http' : '97.105.19.61:53281',  'https': '108.178.64.170:8080'}, 
        {'http' : '212.47.239.33:80',  'https': '93.179.66.57:8080'}, 
        {'http' : '173.212.202.65:443',  'https': '62.249.156.13:53281'},
        {'http' : '181.52.238.94:53281',  'https': '180.249.4.60:80'}, 
        {'http' : '45.70.238.21:53281',  'https': '185.158.65.115:41258'}, 
        {'http' : '41.73.251.98:8080',  'https': '94.232.34.121:41258'}, 
        {'http' : '97.105.19.61:53281',  'https': '108.178.64.170:8080'}, 
        {'http' : '212.47.239.33:80',  'https': '93.179.66.57:8080'}, 
        {'http' : '103.73.166.158:53281',  'https': '62.249.156.13:53281'},
        {'http' : '181.52.238.94:53281',  'https': '180.249.4.60:80'}, 
        {'http' : '95.78.121.173:8080',  'https': '185.158.65.115:41258'}, 
        {'http' : '41.73.251.98:8080',  'https': '94.232.34.121:41258'}, 
        {'http' : '97.105.19.61:53281',  'https': '108.178.64.170:8080'}, 
        {'http' : '212.47.239.33:80',  'https': '93.179.66.57:8080'}, 
        {'http' : '36.66.169.18:8080',  'https': '62.249.156.13:53281'}]

    index = 0

    # index = math.floor(k/10)

    news_0 = News(proxies[index])
    news_0.scrape_highlights()
    news_0.display_highlights()

main()