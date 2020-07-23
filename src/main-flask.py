# Filename: main-flask.py
# Author: Alan Tsui
# Description: a flask app for newscloud

from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import mpld3
import json
import newscrape as ns

app = Flask(__name__, instance_relative_config=True,
            static_folder='static', static_url_path='/static')


@app.route('/', methods=('GET', 'POST'))
def main():
    news = ''

    if request.method == 'POST':
        all_news = ns.main()
        if request.form['news'] == "nyt":
            head_url = get_head_url(all_news[0].headlines)
        elif request.form['news'] == "sfchron":
            head_url = get_head_url(all_news[1].headlines)
        else:
            head_url = zip(["Not a supported news site"], ['www.google.com'])

        return render_template('index.html', list=head_url)
    else:
        print("bad news")
    return render_template('index.html', list=[], url=[])


@app.route('/wordcloud')
def wordcloud():
    # get json object
    l = ns.main()
    d = l[0].writejson()
    p = l[0].paper
    return render_template('wordcloud.html', data=d, paper=p)


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
