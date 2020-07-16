# Filename: main-flask.py
# Author: Alan Tsui
# Description: a flask app for newscloud

from flask import Flask, render_template
import newscloud as nc

app = Flask(__name__, instance_relative_config=True, static_folder='static', static_url_path='/static')

@app.route('/')
def main():
    nc.main()
    return render_template('index.html')

if __name__ == "__main__":
<<<<<<< HEAD:src/main.py
     app.run(host='127.0.0.1', port=4000, debug=True)
=======
    #app.run(host="0.0.0.0")
    app.run()
>>>>>>> 7d9d485d20ec516ef4cbfa946a42165eec28febd:src/main-flask.py
