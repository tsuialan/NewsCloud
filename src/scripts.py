# Filename: scripts.py
# Author: Alan Tsui
# Description: compiliation of python methods 
#       and scripts needed for newscloud

from bs4 import BeautifulSoup
import requests

def webscrape():
    print("hello, world!")
    r1 = requests.get('https://www.nytimes.com/')
    nyt = r1.content

    bs1 = BeautifulSoup(nyt, 'lxml')
    nyt = bs1.find_all('h2')

    nyt_hl = []
    f = open( "nytheadlines.txt", "w")
    
    for headline in nyt:
        nyt_hl.append(headline.getText())
        f.write(headline.getText() + '\n')

if __name__ == '__main__':
    webscrape()