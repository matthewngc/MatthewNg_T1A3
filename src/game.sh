#!/bin/bash
if [[ -x "$(command -v python3)" ]]
then
    pyv="$(python3 -V 2>&1)"
    if [[ $pyv == "Python 3"* ]]
    then
        python3 ./src/main.py
    else
        echo "Your version of python is not up to date, please update and try again." >&2
    fi
else
    echo "You don't have python installed! Go to https://installpython3.com/ to install python!" >&2
fi
