#!/bin/bash

echo "check: $INPUT_CHECK"
INPUT_BASE_BRANCH="$2"

if [ $INPUT_CHECK == "all" ]; then
    python grammar_checker/main.py $(find . -name '*.md')
elif [ $INPUT_CHECK == "updated" ]; then
    echo "base branch: $INPUT_BASE_BRANCH"

    git fetch origin "${INPUT_BASE_BRANCH}" --depth=1

    git log

    python grammar_checker/main.py $(git diff --name-only origin/${INPUT_BASE_BRANCH} | grep '**/*.md')
else
    echo "Invalid check value: $INPUT_CHECK"
    exit 1
fi