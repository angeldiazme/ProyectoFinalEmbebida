#!/bin/bash
while true
do
    valor1=$(python3 reademail.py | grep "ON17" | cut -d " " -f3 | cut -b 24-27)
    valor2=$(python3 reademail.py | grep "OFF17" | cut -d " " -f3 | cut -b 24-28)
    valor3=$(python3 reademail.py | grep "ON21" | cut -d " " -f3 | cut -b 24-27)
    valor4=$(python3 reademail.py | grep "OFF21" | cut -d " " -f3 | cut -b 24-28)
    valor5=$(python3 reademail.py | grep "ON27" | cut -d " " -f3 | cut -b 24-27)
    valor6=$(python3 reademail.py | grep "OFF27" | cut -d " " -f3 | cut -b 24-28)

    if [ "$valor1" = "ON17" ]; then
        echo "$valor1"
        sudo /./home/grupo2/on17.sh
    elif [ "$valor2" = "OFF17" ]; then
        echo "$valor2"
        sudo /./home/grupo2/off17.sh
    elif [ "$valor3" = "ON21" ]; then
        echo "$valor3"
        sudo /./home/grupo2/on21.sh
    elif [ "$valor4" = "OFF21" ]; then
        echo "$valor4"
        sudo /./home/grupo2/off21.sh
    elif [ "$valor5" = "ON27" ]; then
        echo "$valor5"
        sudo /./home/grupo2/on27.sh
    elif [ "$valor6" = "OFF27" ]; then
        echo "$valor6"
        sudo /./home/grupo2/off27.sh
    fi

    sleep 1
done

