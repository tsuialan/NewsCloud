# Filename: newscloud.py
# Author: Alan Tsui
# Description: compiliation of python methods 
#       and scripts needed for newscloud

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlsplit, urljoin

"""

NEWS (object) |-> newspaper (identifier)
                    |-> HEADLINES (object) |-> keyword (identifier)
                                                    |-> original headline
                                                    |-> headline's url
                                                    |-> frequency of keyword

"""

# news headline object
class News:
    def __init__(self, paper, headlines):
        self.paper = paper
        self.headlines = headlines
        self.keywords = {}
        
    def addKeywords(self, keywords):
        self.keywords = keywords

class Headlines:
    def __init__(self, headline, url):
        self.headline = headline
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

    # writes headline into txt file
    sf_hl = []
    sf_url = []
    tfile = "sfchronicle.txt"
    f = open(tfile, "w")
    for headlines in bs_sf:
        # reset format, removes excess spaces
        hurl = headlines['href']
        headlines = headlines.getText().split()
        headline = ""
        # skip single word 'headlines'
        if (len(headlines) <= 3):
            continue
        for word in headlines:
            headline += word + " "
        sf_hl.append(headline)
        sf_url.append(hurl)
        f.write(headline + "\t" + hurl + '\n')
    f.write('\n')
    f.close()

    # creates news object
    sf = News("sfchronicle", sf_hl)

    sf = genkeywords(sf, tfile)

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
    tfile = "newyorktimes.txt"

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

    # write to txt file
    f = open(tfile, "a")
    for index in keywords:
        f.write(index[0] + " : " + str(index[1]) + '\n')
    f.close()
    
    # add list to news object
    news.addKeywords(keywords)
    return news

if __name__ == '__main__':
    main()