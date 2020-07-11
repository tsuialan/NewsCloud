# NewsCloud
## News Centralized and Simplified 
by [@tsuialan](https://github.com/tsuialan) and [@gakwong](https://github.com/gakwong) and [@anchen31](https://github.com/anchen31)
## Setting Up
### If virtual environment is not set up, run: 
MacOs: 
``` MAC
python -m virtualenv newscloud
```
Windows: 
``` WIN
python -m virtualenv newscloud
```
### Else, to open virtual environment, run:
MacOs: 
``` MAC
source activate.sh
```
Windows: 
``` WIN
newscloud\scripts\activate.bat
```
### Install required python packages by running the makefile inside the src/ folder:
MacOs: 
``` MAC
make install
```
Windows: 
``` WIN
pip install -r requirements.txt
```
## Run
### To execute flask program, run inside src/ folder:
MacOs: 
``` MAC
make
```
Windows: 
``` WIN
set FLASK_ENV=newscloud
set FLASK_APP=main.py
python -m flask run --host=0.0.0.0
```
### To execute news-scraping script, run inside src/ folder:
MacOs:
``` MAC
make newscrape
```
Windows:
``` WIN
python newscrape.py
```
