# Filename: newscloud.py
# Author: Alan Tsui
# Description: compiliation of python methods 
#       and scripts needed for newscloud

from bs4 import BeautifulSoup
import requests

class News:
    def __init__(self, paper, headlines):
        self.paper = paper
        self.headlines = headlines
        self.keywords = []
        
    def addKeywords(self, keywords):
        self.keywords = keywords

def newscrape():
    # scrapes new york times
    r1 = requests.get('https://www.nytimes.com/')
    nyt = r1.content
    bs1 = BeautifulSoup(nyt, 'lxml')
    bs_nyt = bs1.find_all('h2')

    # writes headline into file
    nyt_hl = []
    f = open("nytheadlines.txt", "w")
    for headline in bs_nyt:
        nyt_hl.append(headline.getText())
        f.write(headline.getText() + '\n')
    f.write('\n')
    f.close()

    # creates an object, calls analysis
    nyt = News('New York Times', nyt_hl)
    newsAnalysis(nyt)

def newsAnalysis(news):
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

    # alphabetized dictionary
    lst = wordbank.items()
    lst = sorted(lst, key = lambda x : x[0])
    f = open("nytheadlines.txt", "a")
    for index in lst:
        f.write(index[0] + " : " + str(index[1]) + '\n')
    f.close()

    # finds most frequent keywords
    mostFrequent(wordbank)

def mostFrequent(words):
    lst = words.items()
    lst = sorted(lst, key = lambda x : x[1], reverse = True)
    print(lst)

if __name__ == '__main__':
    newscrape()