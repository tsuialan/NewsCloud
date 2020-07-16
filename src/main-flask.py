# Filename: main-flask.py
# Author: Alan Tsui
# Description: a flask app for newscloud

from flask import Flask, render_template, request, redirect, url_for
import newscloud as nc
import newscrape as ns

app = Flask(__name__, instance_relative_config=True, static_folder='static', static_url_path='/static')

@app.route('/', methods=('GET','POST'))
def main():
    news = ''
    #nc.main()
    all_news = ns.main()
    if request.method == 'POST':
        if request.form['news'] == "nyt":
            news = 'nyt'
        else:
            news = 'sfchron'

        if news == 'nyt':
            list = all_news[0].getWords()
            #list = ["test", "words"]
        elif news == "sfchron":
            list = all_news[1].getWords()
            #list = ['test', "words", "chron"]
        else:
            list = ["Not", "a", "supported", "news"]
        print(news)
        return render_template('index.html', list=list)
    print("bad news")
    return render_template('index.html', list=[])

if __name__ == "__main__":
     app.run(host='127.0.0.1', port=4000, debug=True)
