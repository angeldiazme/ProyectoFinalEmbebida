.global _start

.equ GPIO_BASE, 0x3F200000  // Dirección base del GPIO en Raspberry Pi 3,4,5
.equ GPIO_SET_OFFSET, 0x1C
.equ GPIO_CLR_OFFSET, 0x28
.equ GPIO_LEV_OFFSET, 0x34
.equ GPIO_PIR, 7

.section .data
script_path:
    .asciz "/home/pi/on.sh"

.section .bss
    .align 4
buffer:
    .skip 1024

.section .text

_start:
    // Configurar GPIO
    ldr r0, =GPIO_BASE
    ldr r1, [r0, #0x04]     // Leer registro GPFSEL0
    bic r1, r1, #(7 << (GPIO_PIR * 3))  // Limpiar los bits para GPIO_PIR
    orr r1, r1, #(1 << (GPIO_PIR * 3))  // Establecer GPIO_PIR como entrada
    str r1, [r0, #0x04]     // Escribir de vuelta a GPFSEL0

    ldr r2, =script_path     // Cargar la dirección del script

main_loop:
    // Leer estado del sensor PIR
    ldr r1, [r0, #GPIO_LEV_OFFSET]
    tst r1, #(1 << GPIO_PIR)
    beq no_motion

    // Movimiento detectado
    bl motion_detected

no_motion:
    // Sin movimiento, bucle
    b main_loop

motion_detected:
    // Llamar al script utilizando execve
    mov r0, r2              // script_path en r0
    ldr r1, =buffer         // Cargar buffer en r1
    str r2, [r1]            // Guardar script_path en buffer
    add r1, r1, #4
    mov r2, #0              // NULL en r2

    // execve(const char *filename, const char *const argv[], const char *const envp[])
    mov r7, #11             // syscall number for execve
    svc #0                  // Llamada al sistema

    // Si execve falla, regresar al bucle principal
    b main_loop

// Limpiar y salir
cleanup:
    mov r7, #1     // syscall: exit
    svc #0

//(as -o sensor.o sensor.s
//gcc -o sensor sensor.o -lwiringPi
