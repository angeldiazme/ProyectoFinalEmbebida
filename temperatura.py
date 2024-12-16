import time
import board
import adafruit_dht
import subprocess

# Configura el sensor DHT en el GPIO25
dht_device = adafruit_dht.DHT11(board.D26)  # Cambia a GPIO25

# Definir los umbrales para temperatura y humedad
TEMP_30 = 20  # Temperatura mayor a 30°C
TEMP_40 = 25  # Temperatura mayor a 40°C
TEMP_50 = 30  # Temperatura mayor a 50°C

HUMEDAD_NORMAL = 50  # Humedad normal máxima
HUMEDAD_MODERADO = 70  # Humedad moderada máxima

while True:
    try:
        # Leer temperatura y humedad
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        # Verificar los valores y activar los scripts
        if temperature is not None and humidity is not None:
            print(f"Temperatura: {temperature:.1f}°C    Humedad: {humidity:.1f}%")
            
            # Estado crítico 3: Temperatura mayor a 40°C
            if temperature > TEMP_50:
                print("Estado: Crítico 3 - Activando on27.sh")
                subprocess.call("sh /home/grupo2/on27.sh", shell=True)
                subprocess.call("sh /home/grupo2/off21.sh", shell=True)
                subprocess.call("sh /home/grupo2/off17.sh", shell=True)

            # Estado crítico 2: Temperatura entre 30°C y 40°C
            elif TEMP_40 < temperature <= TEMP_50:
                print("Estado: Crítico 2 - Activando on21.sh")
                subprocess.call("sh /home/grupo2/on21.sh", shell=True)
                subprocess.call("sh /home/grupo2/off17.sh", shell=True)
                subprocess.call("sh /home/grupo2/off27.sh", shell=True)

            # Estado crítico 1: Temperatura entre 20°C y 30°C
            elif TEMP_30 < temperature <= TEMP_40:
                print("Estado: Crítico 1 - Activando on17.sh")
                subprocess.call("sh /home/grupo2/on17.sh", shell=True)
                subprocess.call("sh /home/grupo2/off21.sh", shell=True)
                subprocess.call("sh /home/grupo2/off27.sh", shell=True)

            # Condición fuera de rango
            else:
                print("Estado: Normal - Apagando todos los scripts")
                subprocess.call("sh /home/grupo2/off17.sh", shell=True)
                subprocess.call("sh /home/grupo2/off21.sh", shell=True)
                subprocess.call("sh /home/grupo2/off27.sh", shell=True)

        else:
            print("Fallo en la lectura del sensor.")
    except RuntimeError as error:
        # Manejar errores comunes como fallos temporales de lectura
        print(f"Error al leer el sensor: {error.args[0]}")
    except Exception as error:
        dht_device.exit()
        raise error

    # Esperar 2 segundos antes de la siguiente lectura
    time.sleep(2.0)
