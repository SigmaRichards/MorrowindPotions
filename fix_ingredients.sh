#!/bin/bash

PY_WRAP="python3"
FIX_SCR="scripts/rip_pages.py"
RIP_DIR="ingredients"
BUILD_DIR="web-app/build/."

$PY_WRAP $FIX_SCR

if ! [ -e $BUILD_DIR ]
then
	echo -e "Could not find build directory. Make sure to copy ripped files manually."
	exit 1
fi

if ! [ -e $RIP_DIR ] 
then
	echo -e "Could not ripped file directory. find Make sure to copy ripped files to build directory manually."
	exit 2
fi

mv $RIP_DIR $BUILD_DIR
echo -e "Ripped files moved to build directory."
exit 0
