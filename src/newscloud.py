# Filename: newscloud.py
# Author: Alan Tsui
# Description: compiliation of python methods 
#       and scripts needed for newscloud

from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlsplit
import requests

# news headline object
class News:
    def __init__(self, paper, headlines):
        self.paper = paper
        self.headlines = headlines
        self.keywords = []
        
    def addKeywords(self, keywords):
        self.keywords = keywords

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

    sf_hl = []
    txt = "sfchronicle.txt"
    f = open(txt, "w")
    for headline in bs_sf:
        sf_hl.append(headline.getText())
        f.write(headline.getText() + '\n')
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
    txt = "newyorktimes.txt"
    f = open(txt, "w")
    for headline in bs_nyt:
        nyt_hl.append(headline.getText())
        f.write(headline.getText() + '\n')
    f.write('\n')
    f.close()

    # creates an object, calls analysis
    nyt = News("newyorktimes", nyt_hl)

    # break up headlines into words 
    wordbank = {}
    for headline in nyt.headlines:
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
    lst = words.items()
    lst = sorted(lst, key = lambda x : x[0])
    """

    # write to txt file
    f = open(txt, "a")
    for index in keywords:
        f.write(index[0] + " : " + str(index[1]) + '\n')
    f.close()
    
    # add list to news object
    nyt.addKeywords(keywords)

    return nyt

if __name__ == '__main__':
    main()