# CSGO-Rank-Finder
[![](https://img.shields.io/github/v/release/Porvil/CSGO-Rank-Finder?color=green)](https://github.com/Porvil/CSGO-Rank-Finder/releases/tag/v1.0)
[![](https://img.shields.io/tokei/lines/github/Porvil/CSGO-Rank-Finder?color=green)]()
[![](https://img.shields.io/github/downloads/Porvil/CSGO-Rank-Finder/total?color=green)]()
\
[![](https://img.shields.io/github/repo-size/Porvil/CSGO-Rank-Finder)]()
[![](https://img.shields.io/github/languages/code-size/Porvil/CSGO-Rank-Finder)]()

CSGO Rank Finder is a Python GUI application based on PyQT-5.\
The application can search rank of CSGO players.

# Installation

- Download the latest single executable or zip from [Releases](https://github.com/Porvil/CSGO-Rank-Finder/releases).
- If using single executable -> simply open the file and use the application.
- If using single zip -> extract the zip, open the folder "CSGO Rank Finder" and run the "start.bat" file. It will open the application.

# Features

- Searches players ranks(current and best), show their No. of wins, KD, and HS%.
- Can exclude your friends and yourself from the search.
- Auto find ranks based on data copied to clipboard, before running the application.
- Auto copy ranks data in a table form to clipboard after a search is complete.

# Usage

1. Open CSGO console(`) and type "status".
2. Copy the result of above command.
3. Run "CSGO Rank Finder" [[See installation](https://github.com/Porvil/CSGO-Rank-Finder#installation)].
4. Paste the output using "Paste input" button and click "Search Ranks".[if using "Auto find ranks on start up" feature, you can skip this step]
5. Wait for the application to find ranks, it will automatically show ranks in application.
6. Click "Copy ranks to clipboard" to copy ranks in a table form and share it with friends.[if using "Auto copy result to clipboard" feature, you can skip this step]

# Add Friends to blacklist

- Enter friends steamID/steam64ID's to input box.
- Click "Add friends to blacklist" button.
- It will append the entered ID's to blacklist file("friends.txt").
- Don't forget to enable "Exclude friends from search" to exclude friends while searching ranks.

# Note

- The application will create "settings.cfg" file which saves user preferences.
- Do not overuse the application as it uses "csgostats.gg" website to scrape data, so your IP address might get banned if you overuse it.
- Tested on Windows 10 64bit and Python 3.9.5, executable made using auto-py-to-exe v2.13.

# Mentions

- [csgo_rank_finder](https://github.com/PankajzYadav/csgo_rank_finder) by [Pankaj Yadav](https://github.com/PankajzYadav): Used for backend of the GUI.
