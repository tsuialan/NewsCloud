# Filename: main-flask.py
# Author: Alan Tsui
# Description: a flask app for newscloud

from flask import Flask, render_template, request, redirect, url_for
import json
import newscrape as ns

app = Flask(__name__, instance_relative_config=True,
            static_folder='static', static_url_path='/static')

newslist = ns.main()


@app.route('/', methods=('GET', 'POST'))
def main():
    global newslist
    # defaults to nyt wordcloud
    page = 'wordcloud'
    nyt = newslist[0]
    data = nyt.writejson()
    paper = nyt.paper
    if request.method == 'POST':
        if request.form['news'] == "nyt":
            nyt = newslist[0]
            data = nyt.writejson()
            paper = nyt.paper
        elif request.form['news'] == "sfchron":
            sfc = newslist[1]
            data = sfc.writejson()
            paper = sfc.paper
        else:
            nyt = ns.nytscrape()
            data = nyt.writejson()
            paper = "Default: NYT"
    else:
        print("booted or really bad news")
    return render_template('index.html', page=page, data=data, paper=paper)

@app.route('/fupdate')
def fupdate():
    global newslist
    newslist= ns.main()
    page = 'wordcloud'
    nyt = newslist[0]
    data = nyt.writejson()
    paper = nyt.paper
    return render_template('index.html', page=page, data=data, paper=paper)

@app.route('/headline', methods=('GET', 'POST'))
def headline():
    page = 'headline'
    news = ''
    if request.method == 'POST':
        if request.form['news'] == "nyt":
            head_url = get_head_url(ns.nytscrape().headlines)
        elif request.form['news'] == "sfchron":
            head_url = get_head_url(ns.sfcscrape().headlines)
        else:
            head_url = zip(["Not a supported news site"], ['/'])

        return render_template('headline.html', page=page, list=head_url)
    else:
        print("booted or really bad news")
    return render_template('headline.html', page=page, list=[], url=[])


@app.route('/headlines', methods=('GET', 'POST'))
def headlines():
    global newslist
    word = "default"
    word = request.args['word'].lower()
    paper = request.args['paper']
    for news in newslist:
        if (news.paper == paper):
            news_obj = news
            break
    keyword = news_obj.findKeyword(word)
    if keyword != None:
        headurl = get_head_url(keyword.headlines)
        links = True
    else:
        headurl = zip(["No headlines found, back to wordcloud?"], ['/'])
        links = False
    return render_template('word.html', word=word, paper=paper, list=headurl, links=links)


"""
Helper function to zip the headline and url together
"""


def get_head_url(headlines):
    head = []
    urls = []
    for headline in headlines:
        head.append(headline.headline)
        urls.append(headline.url)
    # print(head)
    return zip(head, urls)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
