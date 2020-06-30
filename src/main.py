# Filename: flask.py
# Author: Alan Tsui
# Description: a flask app for newscloud

from flask import Flask
from flask import render_template

app = Flask(__name__, instance_relative_config=True, static_folder='static', static_url_path='/static')

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
     app.run(host="0.0.0.0")