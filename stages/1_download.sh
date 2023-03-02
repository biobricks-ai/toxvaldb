#!/usr/bin/env bash
mkdir -p download/toxvaldb
cd ./download/toxvaldb
echo $(pwd)
ncftpget -R -v -u anonymous -p '' -T \
  ftp://newftp.epa.gov/COMPTOX/STAFF/rjudson/datasets/ToxValDB/
cd ../../