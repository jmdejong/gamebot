#!/bin/bash
cd "`dirname "$0"`"
./startgamebot.py 2>> gamebot.stderr.log >>gamebot.stdout.log &
