# Filename: newscrape.py
# Author: Alan Tsui
# Description: scrapes popular newspaper website
#       for headlines and selects high frequency keywords

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlsplit, urljoin
import newscloud as nc

"""

NEWS (object)   
    |-> newspaper (identifier)
    |-> LIST OF KEYWORDS (objects)  |-> keyword (object's identifier)
                                        |-> original headline
                                        |-> headlines' url
                                        |-> frequency of keyword

"""

""" CLASS FUNCTIONS AND DEFINITIONS """
# news headline objects


class News:
    def __init__(self, paper):
        self.paper = paper
        self.keywords = []
        self.headlines = []
        self.wordbank = {}

    def addKeyword(self, keyword):
        self.keywords.append(keyword)

    def addHeadline(self, headline):
        self.headlines.append(headline)

    def findKeyword(self, word):
        for kw in self.keywords:
            if (kw.word.lower() == word.lower()):
                return kw

    # find keywords and creates corrresponding objects
    def genkeywords(self, headlines, url):
        wordbank = self.wordbank
        # hl is reformatted 'headlines'
        hl = ""
        for word in headlines:
            hl += word + " "
        # split each headline to a series of words, and the count them
        for word in headlines:
            word = word.replace(",", "").replace(
                ".", "").replace("?", "").replace("!", "")
            word = word.replace("'", "").replace(
                '"', "").replace("’", "").replace("‘", "")
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
                self.addKeyword(k)
            else:
                wordbank[word] = wordbank.get(word) + 1
                for kw in self.keywords:
                    if (kw.word == word):
                        # update headline object values
                        kw.setfrequency(kw.freq + 1)
                        kw.addheadline(hl)
                        kw.addurl(url)
                        break

    # sorts dictionary by frequency of keyword
    def sortDictionary(self, tfile):
        # sort by frequency keywords
        keywords = self.wordbank.items()
        self.wordbank = sorted(keywords, key=lambda x: x[1], reverse=True)

        """ ALPHABETIZED
        keywords = words.items()
        keywords = sorted(keywords, key = lambda x : x[0])
        """

        # write to txt file
        f = open(tfile, "a")
        for index in self.wordbank:
            f.write(index[0] + " : " + str(index[1]) + '\n')
        f.close()

# keyword object
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

# headline object
class Headline:
    def __init__(self, h, u):
        self.headline = h
        self.url = u

""" WEBSCRAPING FUNCTIONS """
# https://www.sfchronicle.com/


def sfscrape():
    # scrapes sf chronicle
    r1 = requests.get('https://www.sfchronicle.com/')
    sfc = r1.content
    bs1 = BeautifulSoup(sfc, 'lxml')
    bs_sf = bs1.find_all("a", {"class": "hdn-analytics"})

    # creates news object
    sfc = News("SF Chronicle")

    # writes headline into txt file
    tfile = "./headlines/sfchronicle.txt"         # local text file
    f = open(tfile, "w+")
    for headlines in bs_sf:
        # get href url from headlien
        hurl = headlines['href']
        # completes incomplete urls
        if ('https://' not in hurl):
            base = 'https://www.sfchronicle.com/'
            hurl = urljoin(base, hurl)
        # removes excess spaces
        headlines = headlines.getText().split()
        hl = ""
        for word in headlines:
            hl += word + " "
        H = Headline(hl, hurl)
        sfc.addHeadline(H)
        # skip single word 'headlines'
        if (len(headlines) <= 3):
            continue
        # get keywords
        sfc.genkeywords(headlines, hurl)
        # reformats headline text
        hl = ""
        for word in headlines:
            hl += word + " "
        # writes to local file
        f.write(str(hl) + "\t" + hurl + '\n')
    f.write('\n')
    f.close()

    # sort dictionary
    sfc.sortDictionary(tfile)
    return sfc

# https://www.nytimes.com/


def nytscrape():
    # scrapes new york times
    r1 = requests.get('https://www.nytimes.com/')
    nyt = r1.content
    bs1 = BeautifulSoup(nyt, 'lxml')
    bs_nyt = bs1.find_all('a')

    # creates headline object for nyt
    nyt = News("New York Times")

    # writes headlines into local txt file
    tfile = "./headlines/newyorktimes.txt"
    f = open(tfile, "w+")

    # goes through each 'headline' scraped

    for headlines in bs_nyt:
        # reformats the headline, take out spaces
        headline = headlines.getText().split()
        # ignore 'headlines' if too short, takes out dumb things
        if (len(headline) <= 3):
            continue
        # get url correspondingn to headline
        hurl = headlines['href']
        # ignore 'headlines' with no url
        if ('/' not in hurl):
            continue
        # completes incomplete urls
        if ('https://' not in hurl):
            base = 'https://www.nytimes.com/'
            hurl = urljoin(base, hurl)
        # create headline object for news object
        hl = ""
        for word in headline:
            hl += word + " "
        H = Headline(hl, hurl)
        print("{EENINASDKNLJALDKSJKLSPENINS")
        print(H.headline)
        print(H.url)
        nyt.addHeadline(H)
        # get keywords
        nyt.genkeywords(headline, hurl)
        # reformats hl text
        hl = ""
        for word in headline:
            hl += word + " "
        # writes to local file
        f.write(str(hl) + "\t" + hurl + '\n')
    f.write('\n')
    f.close()

    # sort dictionary
    nyt.sortDictionary(tfile)
    return nyt


""" MAIN FUNCTION """


def main():
    # calling webscraping scripts
    print("[*] Starting New York Times ... ")
    nyt = nytscrape()
    print("[*] Starting SF Chronicle ... ")
    sfc = sfscrape()
    # list holding the news objects
    news = []
    news.append(nyt)
    news.append(sfc)
    return news


if __name__ == '__main__':
    main()
