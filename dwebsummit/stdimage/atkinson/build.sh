#!/bin/bash
python setup.py build
cp build/lib.*/atk.so ./
rm -r build
