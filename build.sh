#!/bin/bash

rm -r ./dist ./panels
npm run build
python3 ./build.py
rm -r ./dist