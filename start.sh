#!/usr/bin/env bash

export PATH=${PwD}webdriver:$PATH
cd src/main

python3 rym_adder.py $@

#os.environ['PATH'] = os.environ['PWD'] + 'webdriver:' + os.environ['PATH']
#os.chdir('src/main')
#import src.main.rym_adder
