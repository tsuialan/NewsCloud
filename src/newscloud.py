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

# news headline objects
class News:
    def __init__(self, paper):
        self.paper = paper
        self.headlines = []
        self.wordbank = {}
    def addHobj(self, headline):
        self.headlines.append(headline)
        
class Headline:
    def __init__(self, keyword):
        self.keyword = keyword
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
    #nytscrape()
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
    # iterate through each headline, reformats it
    for headlines in bs_sf:
        # reset format, removes excess spaces
        hurl = headlines['href']
        headlines = headlines.getText().split()
        # skip single word 'headlines'
        if (len(headlines) <= 3):
            continue
        # get keywords
        sf = genkeywords(sf, sf.wordbank, tfile, headlines, hurl)
        # writes to local file
        f.write(str(headlines) + "\t" + hurl + '\n')
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

def genkeywords(news, wordbank, tfile, headlines, url):
    # break up headlines into words 
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
            h = Headline(word)
            # add headline, url, freq to headline object
            h.addheadline(hl)
            h.addurl(url)
            h.setfrequency(1)
            # add the headline object into of news object
            news.addHobj(h)
        else:
            wordbank[word] = wordbank.get(word) + 1
            for hobj in news.headlines:
                if (hobj.keyword == word):
                    # update headline object values
                    hobj.setfrequency(hobj.freq + 1)
                    hobj.addheadline(hl)
                    hobj.addurl(url)
    return news

# sorts dictionary by frequency of keyword
def sortDictionary(news, tfile):
    # sort by frequency keywords
    keywords = news.wordbank.items()
    news.wordbank = sorted(keywords, key = lambda x : x[1], reverse = True)

    #print(keywords)

    """ ALPHABETIZED
    keywords = words.items()
    keywords = sorted(keywords, key = lambda x : x[0])
    """

    # write to txt file, create headline objects
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