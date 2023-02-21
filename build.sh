#!/bin/bash

if test -d ./dist; then rm -r ./dist; fi
if test -d ./panels/referenceViewer; then rm -r ./panels/referenceViewer; fi
npm i
npm run build
cp -r ./dist ./panels/referenceViewer
python3 ./build.py
rm -r ./dist