# Filename: newscloud.py
# Author: Alan Tsui
# Description: compiliation of python methods 
#       and scripts needed for newscloud

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlsplit, urljoin
from queue import PriorityQueue

"""

NEWS (object) |-> newspaper (identifier)
                    |-> HEADLINES (object) |-> keyword (identifier)
                                                    |-> original headline
                                                    |-> headline's url
                                                    |-> frequency of keyword

"""

# news headline object
class News:
    def __init__(self, paper):
        self.paper = paper
        self.headlines = PriorityQueue()
    def addheadline(self, headline):
        self.headlines.put(headline.frequency, headline)
        
class Headline:
    def __init__(self, keyword):
        self.keyword = keyword
        self.headline = NULL
        self.url = NULL
        self.freq = NULL
    def setfrequency(self, freq):
        self.freq = freq
    def setheadline(self, headline):
        self.headline = headline
    def seturl(self, url):
        self.url = url

def main():
    #nytscrape()
    sfscrape()

# https://www.sfchronicle.com/
def sfscrape():
    # scrapes sf chronicle
    r1 = requests.get('https://www.sfchronicle.com/')
    sf = r1.content
    bs1 = BeautifulSoup(sf, 'lxml')
    bs_sf = bs1.find_all("a", {"class": "hdn-analytics"})

    # creates news object
    sf = News("sfchronicle")

    # writes headline into txt file
    tfile = "./headlines/sfchronicle.txt"         # local text file
    f = open(tfile, "w")
    # iterate through each headline, reformats it
    for headlines in bs_sf:
        # reset format, removes excess spaces
        hurl = headlines['href']
        headlines = headlines.getText().split()
        headline = ""
        # skip single word 'headlines'
        if (len(headlines) <= 3):
            continue
        # headline is reformatted 'headlines'
        for word in headlines:
            headline += word + " "
        # get keywords
        #sf = genkeywords(sf, tfile)

        # adds headline to sf_hl list
        #sf_hl.append(headline)
        #sf_url.append(hurl)
        f.write(headline + "\t" + hurl + '\n')
    f.write('\n')
    f.close()

# https://www.nytimes.com/
def nytscrape():
    # scrapes new york times
    r1 = requests.get('https://www.nytimes.com/')
    nyt = r1.content
    bs1 = BeautifulSoup(nyt, 'lxml')
    bs_nyt = bs1.find_all('h2')

    # writes headline into file
    nyt_hl = []
    #parsed = urlsplit(url)
    tfile = "./headlines/newyorktimes.txt"

    f = open(tfile, "w")
    for headline in bs_nyt:
        nyt_hl.append(headline.getText())
        f.write(headline.getText() + '\n')
    f.write('\n')
    f.close()

    # creates an object
    nyt = News("newyorktimes", nyt_hl)

    nyt = genkeywords(nyt, tfile)

def genkeywords(news, tfile):
    # break up headlines into words 
    wordbank = {}
    for headline in news.headlines:
        words = headline.split()
        for word in words:
            word = word.replace(",", "").replace(".", "").replace("?", "").replace("!", "")
            word = word.replace("'", "").replace('"', "").replace("’", "").replace("‘", "")
            word = word.lower()
            if word not in wordbank.keys():
                wordbank[word] = 1
            else:
                wordbank[word] = wordbank.get(word) + 1

    # sort by frequency keywords
    keywords = wordbank.items()
    keywords = sorted(keywords, key = lambda x : x[1], reverse = True)

    """ ALPHABETIZED
    keywords = words.items()
    keywords = sorted(keywords, key = lambda x : x[0])
    """

    # write to txt file, create headline objects
    f = open(tfile, "a")
    for index in keywords:
        f.write(index[0] + " : " + str(index[1]) + '\n')
    f.close()
    
    return news

if __name__ == '__main__':
    main()