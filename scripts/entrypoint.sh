#!/bin/bash

echo "check: $INPUT_CHECK"

if [ $INPUT_CHECK == "all" ]
then
    python grammar_checker/main.py $(find . -name '*.md')
elif [ $INPUT_CHECK == "updated" ]
then
    # find updated files
else
    echo "Invalid check value: $INPUT_CHECK"
    exit 1
fi