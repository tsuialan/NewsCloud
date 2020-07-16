# Filename: main-cl.py
# Author: Alan Tsui
# Description: a cl version for easier debugging

import newscrape as ns

def main():
    print("[*] +++++++++ NEWSCLOUD +++++++++")
    print("[*] News Simplified and Centralized")
    input("[*] Press any key to begin newscraping ...")
    newslist = ns.main()
    counter = 1
    for news in newslist:
        print("[*] " + str(counter) + ": " + news.paper)
        counter += 1
    sindex = "0"
    while (sindex != "-1"):
        sindex = input("[*] Please enter a number corresponding to the paper \n")
        sindex = int(sindex) - 1
        counter = 1
        for keyword in newslist[sindex].keywords:
            print("[*] " + str(counter) + ": " + keyword.word)
            counter += 1
        kindex = "0"
        while (kindex != "-1"):
            kindex = input("[*] Please enter a number corresponding to the keyword \n")
            kindex = int(kindex) - 1
            kcounter = 1
            keyword = newslist[sindex].keywords[kindex]
            for headline in keyword.headlines:
                print("[*] " + str(kcounter) + ": " + headline)
                kcounter += 1

if __name__ == "__main__":
    main()