# Filename: main-flask.py
# Author: Alan Tsui
# Description: a flask app for newscloud

from flask import Flask, render_template, request, redirect, url_for
import json
import newscrape as ns

app = Flask(__name__, instance_relative_config=True,
            static_folder='static', static_url_path='/static')


@app.route('/', methods=('GET', 'POST'))
def main():
    page = 'index'
    news = ''

    if request.method == 'POST':
        if request.form['news'] == "nyt":
            head_url = get_head_url(ns.nytscrape().headlines)
        elif request.form['news'] == "sfchron":
            head_url = get_head_url(ns.sfcscrape().headlines)
        else:
            head_url = zip(["Not a supported news site"], ['www.google.com'])

        return render_template('index.html', page=page, list=head_url)
    else:
        print("booted or really bad news")
    return render_template('index.html', page=page, list=[], url=[])


'''
https://medium.com/@AnyChart/how-to-create-javascript-word-cloud-chart-tutorial-for-web-developers-7ccf12a37513
'''


@app.route('/wordcloud', methods=('GET', 'POST'))
def wordcloud():
    # get json object
    page = 'wordcloud'
    data = None
    paper = None
    if request.method == 'POST':
        news = ns.main()
        if request.form['news'] == "nyt":
            data = news[0].writejson()
            paper = news[0].paper
        elif request.form['news'] == "sfchron":
            data = news[1].writejson()
            paper = news[1].paper
        else:
            data = news[0].writejson()
            paper = "Default: NYT"
    return render_template('wordcloud.html', page=page, data=data, paper=paper)

@app.route('/headlines', methods=('GET', 'POST'))
def headlines():
    word="default"
    word = request.args['word']
    print(word)
    return render_template('headlines.html', word=word)

"""
Helper function to zip the headline and url together
"""


def get_head_url(headlines):
    head = []
    urls = []
    for headline in headlines:
        head.append(headline.headline)
        urls.append(headline.url)
    return zip(head, urls)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
