#!/bin/bash
python3 -m nuitka --onefile --standalone  main.py --enable-plugin=pyside6 --follow-imports --include-data-files="key.txt"="key.txt"
rm -r main.dist
rm -r main.build
rm -r main.onefile-build