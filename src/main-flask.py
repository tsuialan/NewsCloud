# Filename: main-flask.py
# Author: Alan Tsui
# Description: a flask app for newscloud

from flask import Flask, render_template, request, redirect, url_for
import newscloud as nc
import newscrape as ns

app = Flask(__name__, instance_relative_config=True,
            static_folder='static', static_url_path='/static')


@app.route('/', methods=('GET', 'POST'))
def main():
    news = ''
    all_news = ns.main()
    if request.method == 'POST':
        if request.form['news'] == "nyt":
            news = 'nyt'
        else:
            news = 'sfchron'

        if news == 'nyt':
            # get list of keywords
            l = []
            u = []
            temp = []
            nyt = all_news[0]
            #print(nyt.keywords)
            """
            keyword --> keyword object
            """
            for keyword in nyt.keywords:
                if temp != keyword.urls:
                    l.append(keyword.headlines)
                    print(keyword.urls, 15)
                    u.append(keyword.urls)
            list = zip(l, u)
            print(list)
            #print(list)
            #for a in list:
            #    print(a)

            #list = ["test", "words"]
        elif news == "sfchron":
            # get list of keywords
            l = []
            u = []
            temp=[]
            sfc = all_news[1]
            for keyword in sfc.keywords:
                if temp != keyword.urls:
                    l.append(keyword.headlines)
                    print(keyword.urls, 15)
                    u.append(keyword.urls)

            list = zip(l, u)
            print(list)
        else:
            list = ["Not", "a", "supported", "news"]
            u = ['www.google.com']
        print(news)
        return render_template('index.html', list=list, url=u)
    else:
        print("bad news")
    return render_template('index.html', list=[], url=[])

def getheadurl(news):

    return list

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
