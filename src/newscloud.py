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

    print(nyt.paper)
    print(nyt.headlines)

def newsAnalysis():
    print("Hello World")

if __name__ == '__main__':
    newscrape()
    newsAnalysis()