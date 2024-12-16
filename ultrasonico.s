.data
TRIG_PIN:       .word 23               @ Pin TRIG (GPIO 23)
ECHO_PIN:       .word 24               @ Pin ECHO (GPIO 24)
CLOCK_FREQ:     .word 1000000          @ Frecuencia del reloj (1 MHz para microsegundos)
PULSE_DELAY:    .word 10               @ Duración del pulso TRIG (10 microsegundos)

    .text
    .global _start

_start:
    BL init_gpio                        @ Inicializar GPIO
    BL medir_distancia                  @ Llamar a la función de medición de distancia

    B _start                            @ Volver a iniciar (bucle infinito)

@ -------------------------------
@ Configurar GPIO
@ -------------------------------
init_gpio:
    LDR R0, =TRIG_PIN                   @ Cargar el pin TRIG
    MOV R1, #1                          @ Configurar como salida
    BL config_gpio                      @ Llamar a config_gpio(TRIG, OUT)

    LDR R0, =ECHO_PIN                   @ Cargar el pin ECHO
    MOV R1, #0                          @ Configurar como entrada
    BL config_gpio                      @ Llamar a config_gpio(ECHO, IN)
    BX LR

config_gpio:                            @ Función para configurar GPIO
    PUSH {R1, LR}                       @ Guardar registros
    @ Aquí deberás escribir el código específico de acceso GPIO
    POP {R1, LR}                        @ Restaurar registros
    BX LR

@ -------------------------------
@ Medir distancia
@ -------------------------------
medir_distancia:
    @ Enviar pulso TRIG
    BL set_pin_high                     @ Subir TRIG
    BL delay_us                         @ Esperar 10 microsegundos
    BL set_pin_low                      @ Bajar TRIG

    @ Esperar señal de inicio (ECHO == 1)
wait_echo_high:
    BL read_pin                         @ Leer el pin ECHO
    CMP R0, #0                          @ Comparar con 0
    BEQ wait_echo_high                  @ Si sigue en 0, esperar

    @ Medir tiempo de inicio
    BL get_timer                        @ Leer el tiempo de inicio
    MOV R1, R0                          @ Guardar tiempo de inicio en R1

    @ Esperar señal de fin (ECHO == 0)
wait_echo_low:
    BL read_pin                         @ Leer el pin ECHO
    CMP R0, #1                          @ Comparar con 1
    BEQ wait_echo_low                   @ Si sigue en 1, esperar

    @ Medir tiempo de fin
    BL get_timer                        @ Leer el tiempo de fin
    MOV R2, R0                          @ Guardar tiempo de fin en R2

    @ Calcular duración (R2 - R1)
    SUB R3, R2, R1                      @ Duración del pulso (en microsegundos)

    @ Calcular distancia: duration * 34300 / 2
    MOV R4, #34300                      @ Velocidad del sonido en cm/s
    MOV R5, R3                          @ Usar un registro temporal para evitar conflicto
    MUL R6, R5, R4                      @ Multiplicar duración por velocidad
    LSR R6, R6, #1                      @ Dividir entre 2 (equivale a distancia = duration * 34300 / 2)

    @ Imprimir distancia (R6 contiene la distancia)
    BL print_distance

    BX LR

@ -------------------------------
@ Utilidades
@ -------------------------------
set_pin_high:
    @ Escribe un 1 en el pin TRIG (GPIO)
    @ Código específico de escritura GPIO aquí
    BX LR

set_pin_low:
    @ Escribe un 0 en el pin TRIG (GPIO)
    @ Código específico de escritura GPIO aquí
    BX LR

read_pin:
    @ Leer el valor del pin ECHO
    @ Código específico de lectura GPIO aquí
    @ Devuelve el valor en R0
    MOV R0, #0   @ Simulación de lectura
    BX LR

get_timer:
    @ Leer el timer del sistema
    @ Devuelve el valor del timer en R0
    MOV R0, #12345   @ Simulación de timer
    BX LR

delay_us:
    @ Delay de R0 microsegundos (simulación)
    MOV R1, R0        @ Copiar valor
delay_loop:
    SUBS R1, R1, #1   @ Restar 1
    BNE delay_loop    @ Repetir hasta que llegue a 0
    BX LR

print_distance:
    @ Llamar a una función de impresión para mostrar la distancia
    @ No implementada aquí
    BX LR
