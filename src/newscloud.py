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
    Words = []
    freq = []


    for Tuple in News[0].wordbank:
        (wrd, frq) = Tuple
        Words.append(wrd)
        freq.append(frq)
    
        
   #df = pd.DataFrame()

   #get unique values of the freq and assign font sizes based off it

    

if __name__ == '__main__':
    setFont()
