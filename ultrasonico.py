import RPi.GPIO as GPIO
import time
import os
import subprocess
import time

# Configuración de pines
TRIG = 23  # Cambiar al pin correcto
ECHO = 24  # Cambiar al pin correcto

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def medir_distancia():
    # Enviar señal de disparo
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    inicio_pulso = None
    fin_pulso = None

    # Esperar el inicio del pulso
    while GPIO.input(ECHO) == 0:
        inicio_pulso = time.time()

    # Esperar el final del pulso
    while GPIO.input(ECHO) == 1:
        fin_pulso = time.time()

    # Validar si las variables se establecieron
    if inicio_pulso is None or fin_pulso is None:
        raise RuntimeError("No se pudo medir la distancia correctamente. Revise las conexiones del sensor.")
    
    # Calcular duración del pulso
    duracion_pulso = fin_pulso - inicio_pulso
    # Calcular distancia
    distancia = duracion_pulso * 17150  # Constante para convertir tiempo en distancia
    return round(distancia, 2)

try:
    print("Listo para comenzar...")
    while True:
        distancia = medir_distancia()
        
        # Decisión de color según la distancia
        if 20 <= distancia <= 30:
            os.system("sudo /./home/grupo2/on17.sh")
            os.system("sudo /./home/grupo2/off21.sh")
            os.system("sudo /./home/grupo2/off27.sh")
            
        elif 10 < distancia < 20:
            os.system("sudo /./home/grupo2/on21.sh")
            os.system("sudo /./home/grupo2/off17.sh")
            os.system("sudo /./home/grupo2/off27.sh")
            
        elif distancia <= 10:
            os.system("sudo /./home/grupo2/on27.sh")
            os.system("sudo /./home/grupo2/off21.sh")
            os.system("sudo /./home/grupo2/off17.sh")
        else:
            os.system("sudo /./home/grupo2/off27.sh")
            os.system("sudo /./home/grupo2/off21.sh")
            os.system("sudo /./home/grupo2/off17.sh")
            
                   
            
        print(f"Distancia: {distancia} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nTerminando programa.")
finally:
    GPIO.cleanup()
