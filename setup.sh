#!/bin/bash
file=$([ -z "$1" ] && echo ".env" || echo ".env.$1")

if [ -f $file ]; then
    echo "$file environment selected"
    export $(cat $file | xargs)
else 
    echo "Not able to find the environment"
fi
