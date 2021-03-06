# Filename: newscrape.py
# Author: Alan Tsui
# Description: scrapes popular newspaper website
#       for headlines and selects high frequency keywords

from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlsplit, urljoin
import json
import sys
import copy

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

    # webscraping function
    def webscrape(self, bs_data, paperUrl):
        # writes headlines into local txt file
        #tfile = "./data/" + self.paper.replace(" ", "").lower() + ".txt"
        #f = open(tfile, "w+")
        for headline in bs_data:
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
            # if no url, ignore headline
            if ('/' not in hurl):
                continue
            # completes incomplete url
            if ('https://' not in hurl):
                base = paperUrl
                hurl = urljoin(base, hurl)
            # get texts from html headline
            headline = ""
            for word in h_split:
                headline += word + " "
            # creates headline object
            H = Headline(headline, hurl)
            # check duplicates
            dup = False
            for hl in self.headlines:
                if hl.headline == headline:
                    dup = True
                    break
            if dup == False:
                # adds it to news object
                self.addHeadline(H)
                # get keywords from headline
                self.genKeywords(h_split, hurl)
                # writes to local file
                #f.write(str(headline) + '\t' + hurl + '\n')
        # f.write('\n')
        # f.close()
        # sort dictionary
        self.sortDictionary()
        self.sortKeywords()
        # returns news object

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
                ".", "").replace("?", "").replace("!", "").replace("(", "").replace(")", "")
            word = word.replace("'", "").replace(
                '"', "").replace("’", "").replace("‘", "").replace(";", "")
            word = word.lower()
            # check if word is in the word bank
            # if it is not
            if word not in wordbank.keys():
                # add word to worbank, creates new keyword object
                wordbank[word] = 1
                k = Keyword(word, 1)
                # recombines headline into a string
                H = Headline(hl, url)
                k.addHeadline(H)
                # add keyword object to news object
                self.addKeyword(k)
            # else
            else:
                # increase frequency of word by one
                k = self.findKeyword(word)
                k.setFrequency(k.freq + 1)
                wordbank[word] = wordbank.get(word) + 1
                # ignonre duplicates in hl
                dup = False
                for h in k.headlines:
                    if (h.headline == hl):
                        dup = True
                if (dup):
                    continue
                H = Headline(hl, url)
                k.addHeadline(H)

    # quick sorts the list of keywords in news object
    def sortKeywords(self):
        kw_l = self.keywords
        length = len(kw_l)
        quickSort(kw_l, 0, length-1)
        self.keywords = kw_l

    # sorts the dictionary either alphabetically or by frequency
    def sortDictionary(self):
        # sort by frequency keywords
        keywords = self.wordbank.items()
        l_wb = sorted(keywords, key=lambda x: x[1], reverse=True)
        """ ALPHABETIZED
        keywords = words.items()
        keywords = sorted(keywords, key = lambda x : x[0])
        """
        """ WRITE FREQS
        # write to txt file
        tfile = "./data/" + self.paper.replace(" ", "").lower() + ".txt"
        f = open(tfile, "a")
        for index in l_wb:
            f.write(index[0] + " : " + str(index[1]) + '\n')
        f.close()
        """
        # convert from sorted list back to dictionary
        wb = {}
        for t in l_wb:
            key, value = t
            wb[key] = value
        self.wordbank = wb

    def writejson(self):
        # ignore common words
        fcommon = './common.txt'
        # read each line into list
        with open(fcommon) as fc:
            common = fc.readlines()
        common = [x.lower().strip() for x in common]

        d = []
        counter = 0
        # go through each keyword in news object
        for keyword in self.keywords:
            # limit words
            if (counter >= 20):
                break
            if (keyword.word in common):
                continue
            # creates a list object out of the data
            l = {}
            l["x"] = keyword.word
            l["value"] = keyword.freq
            d.append(l)
            counter += 1
        # creates a json object out of the list
        data = json.dumps(d)
        # dump json to local file
        paper = self.paper.replace(" ", "").lower()
        #fname = './data/data_' + str(paper) + '.json'
        # with open(fname, 'w') as f:
        #    json.dump(data, f)
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


""" HELPER METHODS """


def quickSort(arr, low, high):
    if (low < high):
        pindex = partition(arr, low, high)
        quickSort(arr, low, pindex-1)
        quickSort(arr, pindex+1, high)


def partition(arr, low, high):
    index = (low-1)
    pivot = arr[high]
    for j in range(low, high):
        if (arr[j].freq >= pivot.freq):
            index += 1
            arr[index], arr[j] = arr[j], arr[index]
    arr[index+1], arr[high] = arr[high], arr[index+1]
    return index+1


def allnews(newslist):
    print("Starting All ...")
    allnews = News("All")
    for news in newslist:
        # check if keyword exists in all
        for kw in news.keywords:
            for akw in allnews.keywords:
                # if it does, append head/url
                if kw.word == akw.word:
                    akw.headlines += kw.headlines
                    akw.freq += kw.freq
                    break
            nkw = copy.deepcopy(kw)
            allnews.keywords.append(nkw)
        # check if headline exists in all
        for hl in news.headlines:
            for ahl in allnews.headlines:
                # ignore, else append
                if hl.headline == ahl.headline:
                    break
            nhl = copy.deepcopy(hl)
            allnews.headlines.append(nhl)
        # wordbankn update
        for key, value in news.wordbank.items():
            if key not in allnews.wordbank:
                allnews.wordbank[key] = value
            else:
                allnews.wordbank[key] += value
    # increase recursion depth
    sys.setrecursionlimit(2000)
    allnews.sortKeywords()
    allnews.sortDictionary()
    return allnews


""" WEBSCRAPING FUNCTIONS """

# scrapes new york times


def nytscrape():
    print("Begin New York Times ... ")
    # scrapes new york times
    nyt_url = 'https://www.nytimes.com/'
    r1 = requests.get(nyt_url)
    nyt = r1.content
    bs1 = BeautifulSoup(nyt, 'lxml')
    bs_nyt = bs1.find_all('a')

    # creates headline object for nyt
    nyt = News("New York Times")
    # call webscrape algorithm
    nyt.webscrape(bs_nyt, nyt_url)
    # return object
    return nyt

# scrapes sf chroncile


def sfcscrape():
    print("Begin San Francisco Chronicle ... ")
    # scrapes sf chronicle
    sfc_url = 'https://www.sfchronicle.com/'
    r1 = requests.get(sfc_url)
    sfc = r1.content
    bs1 = BeautifulSoup(sfc, 'lxml')
    bs_sfc = bs1.find_all("a", {"class": "hdn-analytics"})

    # creates news object
    sfc = News("SF Chronicle")
    # call webscrape algorithm
    sfc.webscrape(bs_sfc, sfc_url)
    # return object
    return sfc


# scrapes usatoday

def usatodayscrape():
    print("Begin USA Today ...")
    # scrapes usatoday chronicle
    usat_url = 'https://www.usatoday.com/'
    r1 = requests.get(usat_url)
    usat = r1.content
    bs1 = BeautifulSoup(usat, 'lxml')
    bs_usat = bs1.find_all("a")

    # creates news object
    usat = News("USA Today")
    # call webscrape algorithm
    usat.webscrape(bs_usat, usat_url)
    # return object
    return usat

# scrapes tg


def tgscrape():
    print("Begin The Guardian ...")
    # scrapes usatoday chronicle
    tg_url = 'https://www.theguardian.com/us'
    r1 = requests.get(tg_url)
    tg = r1.content
    bs1 = BeautifulSoup(tg, 'lxml')
    bs_tg = bs1.find_all("a")

    # creates news object
    tg = News("The Guardian")
    # call webscrape algorithm
    tg.webscrape(bs_tg, tg_url)
    # return object
    return tg

# scrapes nyp


def nypscrape():
    print("Begin New York Post ...")
    # scrapes usatoday chronicle
    nyp_url = 'https://www.nypost.com/'
    r1 = requests.get(nyp_url)
    nyp = r1.content
    bs1 = BeautifulSoup(nyp, 'lxml')
    bs_nyp = bs1.find_all("a")

    # creates news object
    nyp = News("New York Post")
    # call webscrape algorithm
    nyp.webscrape(bs_nyp, nyp_url)
    # return object
    return nyp


""" MAIN FUNCTION """


def main():
    print("[*] +++ NEWSCRAPE MAIN +++")
    # calling webscraping functions
    print("[*] Starting New York Times ... ")
    nyt = nytscrape()
    print("[*] Starting SF Chronicle ... ")
    sfc = sfcscrape()
    print("[*] Starting USA Today ... ")
    usat = usatodayscrape()
    print("[*] Starting The Guardian... ")
    tg = tgscrape()
    print("[*] Starting New York Post... ")
    nyp = nypscrape()

    # create json file just in case
    # nyt.writejson()
    # sfc.writejson()
    # usat.writejson()
    # tg.writejson()
    # nyp.writejson()

    # append objects into list, return list
    newslist = []
    newslist.append(nyt)
    newslist.append(sfc)
    newslist.append(usat)
    newslist.append(tg)
    newslist.append(nyp)

    print("[*] Combining All ...")
    a = allnews(newslist)
    # a.writejson()
    newslist.append(a)

    print("[*] DONE")
    # returns list
    return newslist


# main name thing
if __name__ == '__main__':
    main()
