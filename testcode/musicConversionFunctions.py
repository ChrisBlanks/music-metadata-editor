#!/usr/bin/env python3
"""
Programmer: Chris Blanks
Date: Early July, 2019
Purpose: This script defines backend functions for the
metadata editor GUI demo (a.k.a metaDataEditorDemo.py).

Notes:
> The following CLI programs are needed:
    > soundconverter
    > sox
    > ffmpeg
> This script file operates on copies of the original files
that are fed in as input.
> The supported file types are `.wav`, `.ogg` ,and `.mp3`
> CLI format: ./exec_name "file_path.extension"
"""

import os
import os.path
from os.path import sep, expanduser

import sys
import subprocess
import shutil


def makeCopyOf(orig_file):
    """Makes a copy of a file in the Music directory within the Home directory."""
    music_dir_path = expanduser('~')+sep+"Music"+sep
    file_copy_path = "{}{}".format(music_dir_path,os.path.basename(orig_file))

    shutil.copyfile(orig_file,file_copy_path) #copy original file to ~/Music 
    return file_copy_path


def convertMP3ToFlac(mp3_file):
    """Converts a mp3 file to the flac format."""
    absolute_path = os.path.abspath(mp3_file)
    print(absolute_path)
    #verify that ogg file exists before operation
    assert os.path.exists(absolute_path) ,"Could not locate `MP3` copy of original file."
    
    basename = os.path.splitext(absolute_path)[0]
    shell_cmd = "ffmpeg -i \'{}\' \'{}.flac\'".format(absolute_path,basename)
    subprocess.call(shell_cmd,shell=True)


def convertOggToMP3(ogg_file):
    """Converts an ogg file to the mp3 format."""
    absolute_path = os.path.abspath(ogg_file)

    #verify that ogg file exists before operation
    assert os.path.exists(absolute_path) ,"Could not locate `Ogg` copy of original file."
    
    shell_cmd = "soundconverter -b -m audio/mpeg -s .mp3 \'{}\'".format(absolute_path)
    subprocess.call(shell_cmd,shell=True)


def convertWavToFlac(wav_file):
    """Converts a wav file to the flac format."""
    absolute_path = os.path.abspath(wav_file)

    #verify that ogg file exists before operation
    assert os.path.exists(absolute_path) ,"Could not locate `Wav` copy of original file."
    
    basename = os.path.splitext(absolute_path)[0]
    shell_cmd = "sox \'{}\' \'{}.flac\'".format(absolute_path,basename)
    subprocess.call(shell_cmd,shell=True)


def convertFileToFlac(file):
    """Determines the file type and converts `file` to a Flac file."""
    absolute_path = os.path.abspath(file)
    assert os.path.exists(absolute_path),"Input file doesn't exist: {}".format(absolute_path)
    
    new_file_path = makeCopyOf(absolute_path)
    basename , extension = os.path.splitext(new_file_path)
 
    if ".wav" in extension:
        print("Input is `Wav` file type")
        convertWavToFlac(new_file_path)
        os.remove(new_file_path) #remove copy

    elif ".ogg" in extension:
        print("Input is `Ogg` file type")
        convertOggToMP3(new_file_path)
        os.remove(new_file_path)
        mp3_file_name = "{}.mp3".format(basename) #file should be of mp3 type at this point
        convertMP3ToFlac(mp3_file_name)
        os.remove(mp3_file_name)

    elif ".mp3" in extension:
        print("Input is `MP3` file type")
        mp3_file_name = "{}.mp3".format(basename) #file should be of mp3 type at this point
        convertMP3ToFlac(mp3_file_name)
        os.remove(mp3_file_name)

    else:
        assert False, "Unsupported type of file supplied as input: {}".format(new_file_path)
        return None

    return "{}.flac".format(basename)


def expandHomeDirectoryPath(file):
    """Changes the `~` for the actual home directory path of a user."""
    if "~" in file:
        file = file.replace("~", expanduser("~") )
    return file


if __name__ == "__main__":
    if len(sys.argv) < 2 :
        file= "Track 1.wav"
    else:
        file= sys.argv[1] # 2nd CLI will be used for the input file
    
    #change abbreviation to path to home of user
    file= expandHomeDirectoryPath(file)
    print(convertFileToFlac(file))
