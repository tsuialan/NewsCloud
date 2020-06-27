# Filename: Makefile
# Author: Alan Tsui
# Description: a makefile for convenience
# Run: set noexpandtab

.PHONY: run scripts install update clean

all: run

run:
			@echo "[*] [++++++++++ NewsCloud ++++++++++]"
			export FLASK_APP=main.py
			flask run --host=0.0.0.0

scripts:
			@echo "[*] Testing scripts.py"
			python3 scripts.py

install:
			@echo "[*] Installing required pytho packages"
			pip3 install -r requirements.txt

update:
			@echo "[*] Updating python packages"
			pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

clean:
			@echo "[*] Cleaning files"
			-rm -rf __pycache__/
