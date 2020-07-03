# Filename: newscloud.py
# Author: Alan Tsui
# Description: compiliation of python methods 
#       and scripts needed for newscloud

from bs4 import BeautifulSoup
import requests

class News:
    def __init__( self, paper, headlines):
        self.paper = paper
        self.headlines = headlines

def newscrape():
    r1 = requests.get('https://www.nytimes.com/')
    nyt = r1.content

    bs1 = BeautifulSoup(nyt, 'lxml')
    bs_nyt = bs1.find_all('h2')

    nyt_hl = []
    f = open("nytheadlines.txt", "w")
    
    for headline in bs_nyt:
        nyt_hl.append(headline.getText())
        f.write(headline.getText() + '\n')

    nyt = News('New York Times', nyt_hl)

    #print(nyt.paper)
    #print(nyt.headlines)

    newsAnalysis(nyt)

def newsAnalysis(news):
    print("Hello World")

    wordbank = {}
    for headline in news.headlines:
        print(headline)
        words = headline.split()
        for word in words:
            word = word.replace(",", "").replace(".", "").replace("?", "").replace("!", "")
            word = word.replace("'", "").replace('"', "").replace("’", "").replace("‘", "")
            word = word.lower()
            print(word)
            if word not in wordbank.keys():
                wordbank[word] = 1
            else:
                wordbank[word] += 1
    #print(word_bank)

    f = open("nytheadlines.txt", "a")
    for key, value in wordbank.items():
        f.write(key + " : " + str(value) + '\n')

if __name__ == '__main__':
    newscrape()