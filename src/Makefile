# Filename: Makefile
# Author: Alan Tsui
# Description: a makefile for convenience
# Run: set noexpandtab

.PHONY: run scripts install update clean

all: run

run:
			@echo "[*] [++++++++++ NewsCloud ++++++++++]"
			export FLASK_ENV=newscloud
			export FLASK_APP=main-flask.py
			python -m flask run
			#python -m flask run --host=0.0.0.0

cl:
			@echo "[*] [++++++++++ NewsCloud - CL ++++++++++]"	
			python3 main-cl.py

newscrape:
			@echo "[*] Testing newscrape.py"
			python3 newscrape.py

install:
			@echo "[*] Installing required pytho packages"
			pip3 install -r requirements.txt

update:
			@echo "[*] Updating python packages"
			pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

clean:
			@echo "[*] Cleaning files"
			-rm -rf __pycache__/

delete:
			@echo "[*] Deleting files"
			-rm -rf data/
			mkdir data/
