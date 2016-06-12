#!/bin/bash

. /etc/environment

if [[ ! -z $1 ]] ; then 
    TERM=$1 
fi

if [[ -z $SCOTUSBOT_TIMEOUT ]] ; then
    SCOTUSBOT_TIMEOUT=60
fi

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

    if [ -f /tmp/scotusbot_timeout.sh ]; then
        . /tmp/scotusbot_timeout.sh
    fi

    pre
    get_new_opinions
    run_bot
    post

    sleep $ELEX_LOADER_TIMEOUT

done