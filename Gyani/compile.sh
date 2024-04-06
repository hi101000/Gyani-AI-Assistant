#!/bin/bash
python -m nuitka --onefile --standalone  main.py --enable-plugin=pyside6 --follow-imports