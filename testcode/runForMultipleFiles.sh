#!/bin/bash

#
# Programmer: Chris Blanks
# Purpose: Starts the GUI editor for all files supplied
# as CLI arguments.
# Date: Early July, 2019
#

#iterates through all supplied files
for i ; do
  python3 metadataEditorDemo.py $i
done
