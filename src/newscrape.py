# Filename: newscrape.py
# Author: Alan Tsui
# Description: scrapes popular newspaper website
#       for headlines and selects high frequency keywords

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlsplit, urljoin
import newscloud as nc

"""

NEWS (object) |-> newspaper (identifier)
                    |-> HEADLINES (object) |-> keyword (identifier)
                                                    |-> original headline
                                                    |-> headline's url
                                                    |-> frequency of keyword

"""

# news headline objects
class News:
    def __init__(self, paper):
        self.paper = paper
        self.keywords = []
        self.wordbank = {}
    def addKeyword(self, keyword):
        self.keywords.append(keyword)
        
class Keyword:
    def __init__(self, keyword):
        self.word = keyword
        self.headlines = []
        self.urls = []
        self.freq = 0
    def setfrequency(self, freq):
        self.freq = freq
    def addheadline(self, headline):
        self.headlines.append(headline)
    def addurl(self, url):
        self.urls.append(url)

def main():
    # calling webscraping scripts
    nyt = nytscrape()
    sf = sfscrape()

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
    for headlines in bs_sf:
        # get href url from headlien
        hurl = headlines['href']
        # completes incomplete urls
        if ('https://' not in hurl):
            base = 'https://www.sfchronicle.com/'
            hurl = urljoin(base, hurl)
        # removes excess spaces
        headlines = headlines.getText().split()
        # skip single word 'headlines'
        if (len(headlines) <= 3):
            continue
        # get keywords
        sf = genkeywords(sf, headlines, hurl)
        # reformats headline text
        hl = ""
        for word in headlines:
            hl += word + " "
        # writes to local file
        f.write(str(hl) + "\t" + hurl + '\n')
    f.write('\n')
    f.close()

    # sort dictionary 
    sortDictionary(sf, tfile)
    return sf

# https://www.nytimes.com/
def nytscrape():
    # scrapes new york times
    r1 = requests.get('https://www.nytimes.com/')
    nyt = r1.content
    bs1 = BeautifulSoup(nyt, 'lxml')
    bs_nyt = bs1.find_all('a')

    # creates headline object for nyt
    nyt = News("newyorktimes")
    
    # writes headlines into local txt file
    tfile = "./headlines/newyorktimes.txt"
    f = open(tfile, "w")
    # goes through each 'headline' scraped 
    for headlines in bs_nyt:
        # reformats the headline, take out spaces
        headline = headlines.getText().split()
        # ignore 'headlines' if too short, takes out dumb things
        if (len(headline) <= 3):
            continue
        hurl = headlines['href']
        # ignore 'headlies' with no url
        if ('/' not in hurl):
            continue
        # completes incomplete urls
        if ('https://' not in hurl):
            base = 'https://www.nytimes.com/'
            hurl = urljoin(base, hurl)
        # get keywords
        nyt = genkeywords(nyt, headline, hurl)
        # reformats hl text
        hl = ""
        for word in headline:
            hl += word + " "
        # writes to local file
        f.write(str(hl) + "\t" + hurl + '\n')
    f.write('\n')
    f.close()

    # sort dictionary 
    sortDictionary(nyt, tfile)
    return nyt

def genkeywords(news, headlines, url):
    wordbank = news.wordbank
    # hl is reformatted 'headlines'
    hl = ""
    for word in headlines:
        hl += word + " "
    # split each headline to a series of words, and the count them
    for word in headlines:
        word = word.replace(",", "").replace(".", "").replace("?", "").replace("!", "")
        word = word.replace("'", "").replace('"', "").replace("’", "").replace("‘", "")
        word = word.lower()
        if word not in wordbank.keys():
            wordbank[word] = 1
            # creating headline object
            k = Keyword(word)
            # add headline, url, freq to headline object
            k.addheadline(hl)
            k.addurl(url)
            k.setfrequency(1)
            # add the headline object into of news object
            news.addKeyword(k)
        else:
            wordbank[word] = wordbank.get(word) + 1
            for kw in news.keywords:
                if (kw.word == word):
                    # update headline object values
                    kw.setfrequency(kw.freq + 1)
                    kw.addheadline(hl)
                    kw.addurl(url)
                    break
    return news

# sorts dictionary by frequency of keyword
def sortDictionary(news, tfile):
    # sort by frequency keywords
    keywords = news.wordbank.items()
    news.wordbank = sorted(keywords, key = lambda x : x[1], reverse = True)

    """ ALPHABETIZED
    keywords = words.items()
    keywords = sorted(keywords, key = lambda x : x[0])
    """

    # write to txt file
    f = open(tfile, "a")
    for index in news.wordbank:
        f.write(index[0] + " : " + str(index[1]) + '\n')
    f.close()

def printObject(obj):
    print(obj.paper)
    for hl in obj.headlines:
        print(hl.keyword + " : " + str(hl.freq))
        print(hl.headlines)

if __name__ == '__main__':
    main()