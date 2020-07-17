# Filename: newscloud.py
# Author: Alan Tsui
# Description: creates a word cloud from given
#   news headlines and keywords

#from wordcloud import WordCloud
import newscrape as ns
import pandas as pd

#set font size based on frequency
def setFont():
    News = ns.main()
    print(News[0].wordbank)
    numWords = 0
    for words in News[0].wordbank:
        numWords += 1 
    print(numWords)

if __name__ == '__main__':
    setFont()
