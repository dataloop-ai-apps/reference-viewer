#!/bin/bash

rm -r ./dist ./panels
npm i
npm run build
mkdir -p ./panels/referenceViewer
cp -r ./dist/. ./panels/referenceViewer
rm -r ./dist