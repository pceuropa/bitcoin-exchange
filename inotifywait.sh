#!/bin/sh

while inotifywait -r -e modify .
  do
    clear
    python3 -m cProfile -o stats $1 $2
    python3 read_stats.py
  done
