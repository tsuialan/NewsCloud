# Filename: main-flask.py
# Author: Alan Tsui
# Description: a flask app for newscloud

from flask import Flask, render_template, request, redirect, url_for
import json
import newscrape as ns

app = Flask(__name__)

newslist = ns.main()


@app.route('/', methods=('GET', 'POST'))
def main():
    global newslist
    # defaults to nyt wordcloud
    page = 'wordcloud'
    nyt = newslist[0]
    data = nyt.writejson()
    paper = nyt.paper
    papers = get_papers(newslist)
    abbrv = ['nyt', 'sfchron', 'usat', 'tg', 'nyp', 'all']
    all_info = zip(papers, abbrv)
    print(all_info)
    if request.method == 'POST':
        select_news = request.form['news']
        if select_news == "nyt":
            nyt = newslist[0]
            data = nyt.writejson()
            paper = nyt.paper
        elif select_news == "sfchron":
            sfc = newslist[1]
            data = sfc.writejson()
            paper = sfc.paper
        elif select_news == "usat":
            usat = newslist[2]
            data = usat.writejson()
            paper = usat.paper
        elif select_news == "tg":
            tg = newslist[3]
            data = tg.writejson()
            paper = tg.paper
        elif select_news == "nyp":
            nyp = newslist[4]
            data = nyp.writejson()
            paper = nyp.paper
        elif select_news == "all":
            allnews = newslist[5]
            data = allnews.writejson()
            paper = allnews.paper
        else:
            nyt = ns.nytscrape()
            data = nyt.writejson()
            paper = nyt.paper
    else:
        print("booted or really bad news")
    return render_template('index.html', page=page, data=data, paper=paper, all_news=all_info)


@app.route('/headline', methods=('GET', 'POST'))
def headline():
    global newslist
    page = 'headline'
    news = ''
    papers = get_papers(newslist)
    abbrv = ['nyt', 'sfchron', 'usat', 'tg', 'nyp', 'all']
    all_info = zip(papers, abbrv)
    paper = "None"
    if request.method == 'POST':
        select_news = request.form['news']
        if select_news == "nyt":
            head_url = get_head_url(newslist[0].headlines)
            paper = newslist[0].paper
        elif select_news == "sfchron":
            head_url = get_head_url(newslist[1].headlines)
            paper = newslist[1].paper
        elif select_news == "usat":
            head_url = get_head_url(newslist[2].headlines)
            paper = newslist[2].paper
        elif select_news == "tg":
            head_url = get_head_url(newslist[3].headlines)
            paper = newslist[3].paper
        elif select_news == "nyp":
            head_url = get_head_url(newslist[4].headlines)
            paper = newslist[4].paper
        elif select_news == "all":
            head_url = get_head_url(newslist[5].headlines)
            paper = newslist[5].paper
        else:
            head_url = zip(["Not a supported news site"], ['/'])
        return render_template('headline.html', page=page, list=head_url, all_news=all_info, paper=paper)
    else:
        paper = newslist[0].paper
        head_url = get_head_url(newslist[0].headlines)
        all_info = zip(papers, abbrv)
        print("booted or really bad news")
    return render_template('headline.html', page=page, list=head_url, all_news=all_info, paper=paper)


@app.route('/word', methods=('GET', 'POST'))
def word():
    global newslist
    page = 'headline'
    word = "default"
    word = request.args['word'].lower()
    paper = request.args['paper']
    for news in newslist:
        print(news.paper)
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
    papers = get_papers(newslist)
    return render_template('word.html', page=page, word=word, paper=paper, list=headurl, links=links, all_news=papers)


"""
Helper function to zip the headline and url together
"""


@app.route('/fupdate', methods=('GET', 'POST'))
def fupdate():
    global newslist
    newslist = ns.main()
    return main()


@app.route('/about')
def about():
    return render_template('about.html', page="about")


def get_head_url(headlines):
    head = []
    urls = []
    for headline in headlines:
        head.append(headline.headline)
        urls.append(headline.url)
    # print(head)
    return zip(head, urls)


def get_papers(newslist):
    papers = []
    for news in newslist:
        if news.paper not in papers:
            papers.append(news.paper)
    return papers


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
