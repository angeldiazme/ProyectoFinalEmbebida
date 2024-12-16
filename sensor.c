#include <stdio.h>
#include <stdlib.h>
#include <gpiod.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define GPIO_CHIP "/dev/gpiochip0" // El chip GPIO principal
#define GPIO_PIR 7                // Número del pin GPIO

int main(void) {
    struct gpiod_chip *chip;
    struct gpiod_line *line;
    int status0 = 0;
    int status1 = 0;
    int num = 0;

    // Abrir el chip GPIO
    chip = gpiod_chip_open(GPIO_CHIP);
    if (!chip) {
        perror("No se pudo abrir el chip GPIO");
        return 1;
    }

    // Solicitar la línea GPIO
    line = gpiod_chip_get_line(chip, GPIO_PIR);
    if (!line) {
        perror("No se pudo obtener la línea GPIO");
        gpiod_chip_close(chip);
        return 1;
    }

    // Configurar la línea como entrada
    if (gpiod_line_request_input(line, "pir-sensor") < 0) {
        perror("No se pudo configurar la línea como entrada");
        gpiod_chip_close(chip);
        return 1;
    }

    while (1) {
        status0 = gpiod_line_get_value(line);
        if (status0 == 1 && status1 == 0) {
            num++;
            printf("Atención, se ha detectado movimiento %d\n", num);
            status1 = 1;

            pid_t pid = fork();
            if (pid == 0) {
                // Proceso hijo
                execl("/home/grupo2/on.sh", "on.sh", NULL);
                perror("execl");
                exit(EXIT_FAILURE);
            } else if (pid < 0) {
                // Error en fork
                perror("fork");
                exit(EXIT_FAILURE);
            } else {
                // Proceso padre
                wait(NULL); // Espera a que el hijo termine
            }
        } else if (status0 == 0 && status1 == 1) {
            printf("¡Listo para comenzar!\n");
            status1 = 0;
        }
        usleep(10000); // Dormir por 10 ms
    }

    // Liberar los recursos
    gpiod_line_release(line);
    gpiod_chip_close(chip);

    return 0;
}
