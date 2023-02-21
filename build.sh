#!/bin/bash

if test -d ./dist; then rm -r ./dist; fi
if test -d ./panels; then rm -r ./panels; fi
npm i
npm run build
python3 ./build.py
rm -r ./dist