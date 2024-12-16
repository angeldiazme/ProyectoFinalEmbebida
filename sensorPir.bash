#!/bin/bash

# Configurar GPIO 7 como entrada
gpio -g mode 7 in

num=0
status0=0
status1=0

while true; do
    status0=$(gpio -g read 7)
    if [ "$status0" = 1 ] && [ "$status1" = 0 ]; then
        num=$((num + 1))
        echo "Atención, se ha detectado movimiento $num"
        status1=1
        /home/grupo2/on.sh
    elif [ "$status0" = 0 ] && [ "$status1" = 1 ]; then
        echo "¡Listo para comenzar!"
        status1=0
    fi
    sleep 0.01  # Dormir por 10 ms
done