#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Date: Early July 2019
Purpose: This script provides the backend functions for changing metadata
on flac files.

Notes:
>The CLI program `metaflac` is required in order to run this script successfully.
> Potential tags: ALBUM, ARTIST, TITLE, TRACKNUMBER,DATE, GENRE, COMMENTS

"""

import os
import os.path
from os.path import expanduser
import subprocess


def setCoverArt(image_path,music_file):
    """Sets the cover art image of the `music_file` with the given `image_path`."""
    shell_cmd= "metaflac --import-picture-from=\'{}\' \'{}\'".format(image_path,music_file)
    subprocess.call(shell_cmd,shell=True)


def changeTagValue(tag,new_val,music_file):
    """Updates the `tag` value of the `music_file` to `new_value`."""
    shell_cmd = "metaflac --remove-tag={0} \'--set-tag={0}={1}\' \'{2}\'".format(tag,new_val,music_file)
    print(shell_cmd)
    subprocess.call(shell_cmd,shell=True)

    if tag == "TITLE" and new_val != os.path.basename(os.path.splitext(music_file)[0]):
        changeNameOfMusicFile(music_file,new_val)


def changeNameOfMusicFile(music_file,title):
    """Updates the name of the music file to match the value of the Title tag."""
    new_file_name = "{}/Music/{}.flac".format( expanduser("~"), title)
    os.rename(music_file,new_file_name)


if __name__ == "__main__":
    setCoverArt("/home/chrisblanks/Pictures/ADDS.png","/home/chrisblanks/Music/japanese_song.flac")

    changeTagValue("ALBUM","stupid","/home/chrisblanks/Music/japanese_song.flac")
    changeTagValue("ARTIST","lucie","/home/chrisblanks/Music/japanese_song.flac")
    #title should be changed last because it will change the name of the song file
    changeTagValue("TITLE","new_song","/home/chrisblanks/Music/japanese_song.flac")

