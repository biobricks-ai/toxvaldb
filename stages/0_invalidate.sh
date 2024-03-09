#!/usr/bin/env bash
mkdir -p download
url="https://gaftp.epa.gov/Comptox/Staff/rjudson/datasets/ToxValDB/"
curl -k $url > download/toxvaldb.html

