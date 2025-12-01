# Spotify scripts - by Adrian Retamosa

So ever since Spotify started messing with user licenses earlier this year, I feared that my playlists which I spent half a decade updating would vanish on any given day. Therefore, I made these simple scripts to help both exporting the 'Favourite Songs' playlist to a .txt file and, since my Spotify account is still a thing, I also decided to be able to share my personal fav songs playlist by saving it into a different one that **can** be shared, unlike the default one.

## Overview

The repo contains the following scripts:

- **fav-songs-to-playlist.py**: this detects your default 'Favourite Songs' playlist and makes a copy of it.
- **update-fav-songs.py**: this updates the second playlist with any new song that was added to the default fav songs list.
- **export-fav-songs.py**: this creates a text file with every song added to the default 'Favourite Songs' playlist, in case you also fear that your Spotify account might just disappear one day (can't blame you for that) or if you want to use a different music service (can't blame you for this either).

## How to use

Minimal setup is needed, provided that you are a software developer (so having a programming IDE, Python installed in your machine, some of the most common libraries also downloaded...), you only need to setup a *credentials.py* file with the following values:

- **CLIENT_ID**
- **CLIENT_SECRET**
- **REDIRECT_URL**='http://localhost:8888/callback'

The first two values can be found by creating a **[SPOTIFY FOR DEVELOPERS](https://developer.spotify.com/)** account. Make sure to keep them secret! If you decide to clone this repo, the file *credentials.py* will never be uploaded to the repo as it is present in the **.gitignore** file.

To run each independent script, just open any IDE of your choice (the terminal / command line should also work) and run it! 

*Note: this project was developed on a **Windows** machine, so any error that could happen in a Linux or MacOS is unknown to me.*

To finish this document, just let you know that, even though this following sentence is forbidden to us developers, *this works in my machine*, which means there is a solid chance I might have forgotten to explain something. And perhaps something else might not work in your machine. Sorry in advance!

If you are reading this, thank you so much for having a look at my small project. Have a nice one! And enjoy the music 😎.