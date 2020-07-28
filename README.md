# NewsCloud
### News Centralized and Simplified 
by [@tsuialan](https://github.com/tsuialan) and [@gakwong](https://github.com/gakwong) and [@anchen31](https://github.com/anchen31)

NewsCloud is a python flask based web app that attempts to visualize recent headlines of contemporary popular newspaper websites into a wordcloud. It is an attempt to streamline all the popular newspaper sites into one very simple interactive user interface that is both easy to comprehend and covenient for users of any backgrounds. With NewsCloud, no longer does the modern day problems of fake news and the distrust of information that exists within many social media websites apply, for this site is built to create trust between the user and the information it presents and the consolidation of those information into one single site. 

## To-Do Checklist
### Bugs
- html tags are not refined, incorrectly assigned some url to headlines

### In Progress
- Flask
  - get template for home/headline page
  - make site looks nicer
  - add search bar in nav bar
  - add about page
  - combine home/headline page?
- NewScrape
  - script can prob be rewritten for efficiency
  - add more newspaper sites
  - add more common words to file
- NewsCloud
  - combine all newspaper to one word cloud option  
  
## Setting Up
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