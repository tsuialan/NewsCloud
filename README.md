# NewsCloud
### News Centralized and Simplified 
by [@tsuialan](https://github.com/tsuialan) and [@gakwong](https://github.com/gakwong) and [@anchen31](https://github.com/anchen31)

## To-Do Checklist
### Bugs
- html tags are not refined, incorrectly assigned some url to headlines
- cannot localize css files for some reason

### In Progress
- Flask
  - write new interface for the word cloud
  - clean up html/css formatting
  - make site looks nicer
- NewScrape
  - script can prob be rewritten for efficiency
  - need to specify html classes
  - add more newspaper sites
- NewsCloud
  - javascript implementation of word cloud
    - add categories
    - clickable keywords to headlines/urls
    - take out common words
    - combine all newspaper to one word cloud option  


## Setting Up
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
## Run
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
#### To run a command line version of the program, run inside src/ folder:
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
