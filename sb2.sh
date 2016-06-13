#!/bin/bash

. /etc/environment

TERM=2015
SCOTUSBOT_TIMEOUT=60

function pre {
    rm -rf new.csv
}

function get_new_opinions {
    docket opinions $TERM > new.csv
}

function run_bot {
    python bot.py
}

function post {
    cp new.csv old.csv
    rm -rf new.csv
}

for (( i=1; i<100000; i+=1 )); do

    pre
    get_new_opinions
    run_bot
    post

    sleep $SCOTUSBOT_TIMEOUT

done