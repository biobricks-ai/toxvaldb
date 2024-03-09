#!/usr/bin/env bash
mkdir -p download/toxvaldb

# Extract links from the HTML file
grep -oP 'href="\K[^"]*' download/toxvaldb.html | grep -v "Parent Directory" > download/links.txt

# Download each file
cd download/toxvaldb
url="https://gaftp.epa.gov/Comptox/Staff/rjudson/datasets/ToxValDB/"
cat ../links.txt | while read line; do
    wget --no-check-certificate "${url}${line}"
done
cd ../..