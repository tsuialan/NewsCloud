# NewsCloud
### News Centralized and Simplified 
by [@tsuialan](https://github.com/tsuialan) and [@gakwong](https://github.com/gakwong) and [@anchen31](https://github.com/anchen31)
### To-Do Checklist
#### Bugs
- refine tags for both nyt and sfc to prevent wrong headline/url and headline/excerpt 
#### In Progress
- Flask
- NewScrape
#### Need to Start
- News Cloud
### Setting Up
#### If virtual environment is not set up, run: 
MacOs: 
``` MAC
python -m virtualenv newscloud
```
Windows: 
``` WIN
python -m virtualenv newscloud
```
#### Else, to open virtual environment, run:
MacOs: 
``` MAC
source activate.sh
```
Windows: 
``` WIN
newscloud\scripts\activate.bat
```
#### Install required python packages by running the makefile inside the src/ folder:
MacOs: 
``` MAC
make install
```
Windows: 
``` WIN
pip install -r requirements.txt
```
### Run
#### To execute flask program, run inside src/ folder:
MacOs: 
``` MAC
make
```
Windows: 
``` WIN
set FLASK_ENV=newscloud
set FLASK_APP=main.py
python -m flask run
```
#### To run a command line versionn of the program, run inside src/ folder:
MacOs: 
``` MAC
make cl
```
Windows: 
``` WIN
python main-cl.py
```
#### To execute news-scraping script, run inside src/ folder:
MacOs:
``` MAC
make newscrape
```
Windows:
``` WIN
python newscrape.py
```
#### To execute news-cloud script, run inside src/ folder:
MacOs:
``` MAC
make newscloud
```
Windows:
``` WIN
python newscloud.py
```
