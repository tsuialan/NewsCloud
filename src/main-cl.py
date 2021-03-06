# Filename: main-cl.py
# Author: Alan Tsui
# Description: a cl version for easier debugging

import webbrowser
import newscrape as ns


def main():
    print("[*] +++++++++ NEWSCLOUD +++++++++")
    print("[*] News Simplified and Centralized")
    input("[*] Press enter to begin newscraping ...")
    newslist = ns.main()
    print("[*] Done newscraping ")
    sindex = "0"
    while (1):
        # "home menu" formatting
        print("[*] +++ NewsCloud +++")
        counter = 1
        for news in newslist:
            print("[*] " + str(counter) + ": " + news.paper)
            counter += 1
        # inputs
        sindex = input(
            "[*] Please enter a number corresponding to the paper \n")
        # q to quit program
        if (sindex == "q"):
            break
        if (sindex == "Q"):
            return 0
        # calculates index
        sindex = int(sindex) - 1
        # prints out existing newspaper
        counter = 1
        for keyword in newslist[sindex].keywords:
            print("[*] " + str(counter) + ": " + keyword.word)
            counter += 1
        # second "menu"
        kindex = "0"
        while (1):
            # formatting for list of keywords
            kindex = input(
                "[*] Please enter a number corresponding to the keyword \n")
            if (kindex == "q"):
                break
            if (kindex == "Q"):
                return 0
            # calculates index
            kindex = int(kindex) - 1
            kcounter = 1
            # get headline
            keyword = newslist[sindex].keywords[kindex]
            for headline in keyword.headlines:
                print("[*] " + str(kcounter) + ": " + headline.headline)
                kcounter += 1
            uindex = "0"
            while (1):
                # formatting for list of headlines
                uindex = input(
                    "[*] Please enter a number corresponding to the headline \n")
                if (uindex == "q"):
                    break
                if (uindex == "Q"):
                    return 0
                uindex = int(uindex) - 1
                url = keyword.headlines[uindex].url
                # open selected headline in broweser
                webbrowser.open(url)


if __name__ == "__main__":
    main()
