#!/bin/bash

# Pines GPIO
TRIG=23        # Pin TRIG
ECHO=24        # Pin ECHO
CHIP=0         # Chip GPIO (generalmente 0 para Raspberry Pi)

# Configuración inicial
gpioset -m output $CHIP $TRIG=0   # Configurar TRIG como salida y ponerlo en bajo
# ECHO se usa como entrada de forma implícita al leerlo con gpioget

# Variables para control
distancia_anterior=0
num=0
status1=0

# Función para medir la distancia
function medir_distancia() {
    # Enviar pulso TRIG
    gpioset $CHIP $TRIG=1
    sleep 0.00001  # Pulso de 10 microsegundos
    gpioset $CHIP $TRIG=0

    # Leer el tiempo de inicio y fin del pulso en ECHO
    local start_time=0
    while [ "$(gpioget $CHIP $ECHO)" -eq 0 ]; do
        start_time=$(date +%s%N)
    done

    local end_time=0
    while [ "$(gpioget $CHIP $ECHO)" -eq 1 ]; do
        end_time=$(date +%s%N)
    done

    # Calcular la duración del pulso en segundos
    local duration=$(echo "($end_time - $start_time) / 1000000000" | bc -l)

    # Validar la duración para evitar ruido
    if (( $(echo "$duration > 0.05" | bc -l) )) || (( $(echo "$duration <= 0" | bc -l) )); then
        echo "Error: Duración fuera de rango (posible ruido)."
        echo "0"
        return
    fi

    # Calcular la distancia en centímetros
    local distance=$(echo "$duration * 34300 / 2" | bc -l)
    echo "$distance"
}

# Ciclo principal
echo "Iniciando monitoreo del sensor ultrasónico..."
while true; do
    # Medir la distancia actual
    distancia=$(medir_distancia)

    # Validar si la medición es válida
    if (( $(echo "$distancia > 0" | bc -l) )); then
        # Detectar cambio significativo en la distancia
        if (( $(echo "$distancia < 10" | bc -l) )) && [ "$status1" = 0 ]; then
            num=$((num + 1))
            echo "Movimiento detectado en rango cercano: $distancia cm (Evento $num)"
            status1=1
            bash /home/grupo2/on27.sh
        elif (( $(echo "$distancia >= 10 && $distancia <= 20" | bc -l) )) && [ "$status1" = 0 ]; then
            num=$((num + 1))
            echo "Movimiento detectado en rango medio: $distancia cm (Evento $num)"
            status1=1
            bash /home/grupo2/on21.sh
        elif (( $(echo "$distancia > 20 && $distancia <= 30" | bc -l) )) && [ "$status1" = 0 ]; then
            num=$((num + 1))
            echo "Movimiento detectado en rango lejano: $distancia cm (Evento $num)"
            status1=1
            bash /home/grupo2/on17.sh
        fi

        # Resetear status si no hay cambio
        if (( $(echo "$distancia > 30" | bc -l) )); then
            echo "Distancia fuera de rango: $distancia cm. Reset."
            status1=0
            bash /home/grupo2/off27.sh
            bash /home/grupo2/off21.sh
            bash /home/grupo2/off17.sh
        fi
    else
        echo "Error: Medición inválida o fuera de rango."
    fi

    # Dormir un poco para evitar lecturas continuas excesivas
    sleep 0.1
done