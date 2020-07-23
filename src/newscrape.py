# Filename: newscrape.py
# Author: Alan Tsui
# Description: scrapes popular newspaper website
#       for headlines and selects high frequency keywords

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlsplit, urljoin
import json

""" OBJECT DIAGRAM

News Object
    |-> string paper (string name of paper)
    |-> Keyword [] keywords (list of keywords objects)
    |-> Headline [] headlines (list of headlines objects)
    |-> Dictionary wordbank ( dictionary of keywords/freqs )

Keywords Object
    |-> string word (string keyword)
    |-> Headline [] headlines (list of headlines object)
    |-> int freq (int frequency of keywords)

Headlines Object
    |-> string headline (string headline)
    |-> string url (string url of headline)

"""


""" CLASS OBJECTS """

# NEWS OBJECT


class News:
    # default constructor
    def __init__(self, paper):
        self.paper = paper
        self.keywords = []
        self.headlines = []
        self.wordbank = {}

    # adds Keyword object to keword list
    def addKeyword(self, keyword):
        self.keywords.append(keyword)

    # adds Headline object to headline list
    def addHeadline(self, headline):
        self.headlines.append(headline)

    # find and return Keyword object (string keyword)
    def findKeyword(self, word):
        for kw in self.keywords:
            if (kw.word.lower() == word.lower()):
                return kw

    # generates 'keywords' from headline
    def genKeywords(self, headline, url):
        # creates a wordbank sorted by frequency
        wordbank = self.wordbank
        # recombines the headline into a sentence
        hl = ""
        for word in headline:
            hl += word + " "
        # for each individual word in the headline
        for word in headline:
            # removes punctuation
            word = word.replace(",", "").replace(
                ".", "").replace("?", "").replace("!", "")
            word = word.replace("'", "").replace(
                '"', "").replace("’", "").replace("‘", "")
            word = word.lower()
            # check if word is in the word bank
            # if it is not
            if word not in wordbank.keys():
                # add word to worbank, creates new keyword object
                wordbank[word] = 1
                k = Keyword(word, 1)
                # recombines headline into a string
                h = Headline(hl, url)
                k.addHeadline(h)
                # add keyword object to news object
                self.addKeyword(k)
            # else
            else:
                # increase frequency of word by one
                wordbank[word] = wordbank.get(word) + 1
                k = self.findKeyword(word)
                k.setFrequency(k.freq + 1)
                h = Headline(hl, url)
                k.addHeadline(h)

    # sorts the dictionary either alphabetically or by frequency
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

    def writejson(self):
        d = []
        # go through each keyword in news object
        for keyword in self.keywords:
            # creates a list object out of the data
            l = {}
            l["x"] = keyword.word
            l["value"] = keyword.freq
            """         URL IMPLEMENTATION FOR LATER
            H = []
            for headline in keyword.headlines:
                h = []
                h.append(headline.headline)
                h.append(headline.url)
                H.append(h)
            l.append(H)
            """
            d.append(l)
        # creates a json object out of the list
        data = json.dumps(d)
        # dump json to local file
        paper = self.paper.replace(" ", "").lower()
        fname = './data/data_' + str(paper) + '.json'
        with open(fname, 'w') as f:
            json.dump(data, f)
        # returns json object
        return data

# KEYWORD OBJECT


class Keyword:
    # default constuctor
    def __init__(self, keyword, frequency):
        self.word = keyword
        self.headlines = []
        self.freq = frequency

    # set keyword's frequency
    def setFrequency(self, f):
        self.freq = f

    # add Headline object to headline list
    def addHeadline(self, headline):
        self.headlines.append(headline)

# HEADLINE OBJECT       // contains headline (str) and url


class Headline:
    # default constructor
    def __init__(self, h, u):
        self.headline = h
        self.url = u


""" WEBSCRAPING FUNCTIONS """

# scrapes new york times


def nytscrape():
    # scrapes new york times
    r1 = requests.get('https://www.nytimes.com/')
    nyt = r1.content
    bs1 = BeautifulSoup(nyt, 'lxml')
    bs_nyt = bs1.find_all('a')

    # creates headline object for nyt
    nyt = News("New York Times")

    # writes headlines into local txt file
    tfile = "./data/newyorktimes.txt"
    f = open(tfile, "w+")

    for headline in bs_nyt:
        # split headline into individual words
        h_split = headline.getText().split()
        # if less than 3 words, ignore headline
        if (len(h_split) <= 3):
            continue
        # get url from headline's href if exists
        if headline.has_attr('href'):
            hurl = headline['href']
        else:
            continue
        # if no url, ignore headlinen
        if ('/' not in hurl):
            continue
        # completes incomplete url
        if ('https://' not in hurl):
            base = 'https://www.nytimes.com/'
            hurl = urljoin(base, hurl)
        # get texts from html headline
        headline = ""
        for word in h_split:
            headline += word + " "
        # creates headline object
        H = Headline(headline, hurl)
        # adds it to news object
        nyt.addHeadline(H)
        # get keywords from headline
        nyt.genKeywords(h_split, hurl)
        # writes to local file
        f.write(str(headline) + '\t' + hurl + '\n')
    f.write('\n')
    f.close()

    # sort dictionary
    nyt.sortDictionary(tfile)
    # returns news object
    return nyt

# scrapes sf chroncile


def sfcscrape():
    # scrapes sf chronicle
    r1 = requests.get('https://www.sfchronicle.com/')
    sfc = r1.content
    bs1 = BeautifulSoup(sfc, 'lxml')
    bs_sfc = bs1.find_all("a", {"class": "hdn-analytics"})

    # creates news object
    sfc = News("SF Chronicle")

    # writes headlines into local txt file
    tfile = "./data/sfchronicle.txt"
    f = open(tfile, "w+")

    for headline in bs_sfc:
        # split headline into individual words
        h_split = headline.getText().split()
        # if less than 3 words, ignore headline
        if (len(h_split) <= 3):
            continue
        # get url from headline's href
        if headline.has_attr('href'):
            hurl = headline['href']
        else:
            continue
        # if no url, ignore headlinen
        if ('/' not in hurl):
            continue
        # completes incomplete url
        if ('https://' not in hurl):
            base = 'https://www.sfchronicle.com/'
            hurl = urljoin(base, hurl)
        # get texts from html headline
        headline = ""
        for word in h_split:
            headline += word + " "
        # creates headline object
        H = Headline(headline, hurl)
        # adds it to news object
        sfc.addHeadline(H)
        # get keywords from headline
        sfc.genKeywords(h_split, hurl)
        # writes to local file
        f.write(str(headline) + '\t' + hurl + '\n')
    f.write('\n')
    f.close()

    # sort dictionary
    sfc.sortDictionary(tfile)
    # returns news object
    return sfc


""" MAIN FUNCTION """


def main():
    # calling webscraping functions
    print("[*] Starting New York Times ... ")
    nyt = nytscrape()
    print("[*] Starting SF Chronicle ... ")
    sfc = sfcscrape()

    nyt.writejson()
    print(sfc.writejson())

    # append objects into list, return list
    newslist = []
    newslist.append(nyt)
    newslist.append(sfc)
    # returns list
    return newslist


# main name thing
if __name__ == '__main__':
    main()
