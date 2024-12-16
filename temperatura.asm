; Programa ensamblador para manejar el DHT11 con libgpiod
; Activar scripts según temperatura y humedad

.global _start
.section .data

TEMP_30:     .word 20   ; Umbral de temperatura para Crítico 1
TEMP_40:     .word 30   ; Umbral de temperatura para Crítico 2
TEMP_50:     .word 40   ; Umbral de temperatura para Crítico 3
GPIO_PATH:   .asciz "/dev/gpiochip0"
ON17:        .asciz "/home/grupo2/on17.sh"
ON21:        .asciz "/home/grupo2/on21.sh"
ON27:        .asciz "/home/grupo2/on27.sh"
OFF17:       .asciz "/home/grupo2/off17.sh"
OFF21:       .asciz "/home/grupo2/off21.sh"
OFF27:       .asciz "/home/grupo2/off27.sh"
ERROR_MSG:   .asciz "Error al leer el sensor\n"

.section .bss
.lcomm temp, 4          ; Almacena la temperatura leída
.lcomm humedad, 4       ; Almacena la humedad leída

.section .text
_start:
    ; Configurar interrupción para Ctrl+C (SIGINT)
    LDR R0, =sigint_handler
    BL signal

main_loop:
    ; Leer datos del DHT11
    LDR R0, =GPIO_PATH
    BL dht_read_data
    CMP R0, #0
    BEQ read_error

    ; Mostrar datos leídos
    LDR R0, =temp
    LDR R1, =humedad
    BL print_data

    ; Evaluar estados
    ; Estado Crítico 3
    LDR R0, temp
    LDR R1, =TEMP_50
    CMP R0, R1
    BGT critical_3

    ; Estado Crítico 2
    LDR R1, =TEMP_40
    CMP R0, R1
    BLE critical_2

    ; Estado Crítico 1
    LDR R1, =TEMP_30
    CMP R0, R1
    BLE critical_1

    ; Estado normal
    BL apagar_todos
    B main_loop

critical_3:
    LDR R0, =ON27
    BL ejecutar_script
    BL apagar_moderado
    B main_loop

critical_2:
    LDR R0, =ON21
    BL ejecutar_script
    BL apagar_normal
    B main_loop

critical_1:
    LDR R0, =ON17
    BL ejecutar_script
    BL apagar_critico
    B main_loop

read_error:
    LDR R0, =ERROR_MSG
    BL print_message
    B main_loop

; Subrutinas
print_data:
    ; Imprime temperatura y humedad
    ; Implementa tu propia lógica para mostrar datos
    BX LR

print_message:
    ; Imprime un mensaje en consola
    ; Implementa tu propia lógica para salida
    BX LR

ejecutar_script:
    ; Ejecuta un script usando system()
    ; R0 contiene la ruta al script
    MOV R1, R0
    LDR R0, ="sh "
    BL strcat
    BL system
    BX LR

apagar_todos:
    ; Apaga todos los scripts
    LDR R0, =OFF17
    BL ejecutar_script
    LDR R0, =OFF21
    BL ejecutar_script
    LDR R0, =OFF27
    BL ejecutar_script
    BX LR

apagar_moderado:
    ; Apaga los scripts menos el de Crítico 3
    LDR R0, =OFF21
    BL ejecutar_script
    LDR R0, =OFF17
    BL ejecutar_script
    BX LR

apagar_normal:
    ; Apaga los scripts menos el de Crítico 2
    LDR R0, =OFF17
    BL ejecutar_script
    LDR R0, =OFF27
    BL ejecutar_script
    BX LR

apagar_critico:
    ; Apaga los scripts menos el de Crítico 1
    LDR R0, =OFF21
    BL ejecutar_script
    LDR R0, =OFF27
    BL ejecutar_script
    BX LR

sigint_handler:
    ; Manejar interrupción SIGINT
    MOV R0, #0
    BL exit
    BX LR

.align
