#include <gpiod.h>#include <stdio.h>#include <unistd.h>#include <time.h>#define CHIP_NAME "/dev/gpiochip0"  // Nombre del chip GPIO#define TRIG_PIN 23                  // GPIO 23#define ECHO_PIN 24                  // GPIO 24// Función para obtener la hora actual en microsegundoslong get_microseconds() {    struct timespec ts;    clock_gettime(CLOCK_MONOTONIC, &ts);    return ts.tv_sec * 1000000 + ts.tv_nsec / 1000;}// Función para medir la distanciafloat medir_distancia(struct gpiod_line *trig_line, struct gpiod_line *echo_line) {    long inicio_pulso, fin_pulso;    float distancia;    // Generar un pulso en TRIG    gpiod_line_set_value(trig_line, 1);    usleep(10);  // 10 microsegundos    gpiod_line_set_value(trig_line, 0);    // Esperar el inicio del pulso en ECHO    while (gpiod_line_get_value(echo_line) == 0) {        inicio_pulso = get_microseconds();    }    // Esperar el final del pulso en ECHO    while (gpiod_line_get_value(echo_line) == 1) {        fin_pulso = get_microseconds();    }    // Calcular duración del pulso    long duracion_pulso = fin_pulso - inicio_pulso;    // Calcular distancia (en cm)    distancia = duracion_pulso * 0.034 / 2;  // Constante para convertir tiempo en distancia    return distancia;}int main() {    struct gpiod_chip *chip;    struct gpiod_line *trig_line, *echo_line;    // Abrir el chip GPIO    chip = gpiod_chip_open(CHIP_NAME);    if (!chip) {        perror("Error al abrir el chip GPIO");        return 1;    }    // Configurar la línea TRIG    trig_line = gpiod_chip_get_line(chip, TRIG_PIN);    if (!trig_line || gpiod_line_request_output(trig_line, "ultrasonico", 0) < 0) {        perror("Error al configurar el pin TRIG");        gpiod_chip_close(chip);        return 1;    }    // Configurar la línea ECHO    echo_line = gpiod_chip_get_line(chip, ECHO_PIN);    if (!echo_line || gpiod_line_request_input(echo_line, "ultrasonico") < 0) {        perror("Error al configurar el pin ECHO");        gpiod_chip_close(chip);        return 1;    }    printf("Esperando al sensor...");    usleep(1000000);  // Esperar 1 segundo    while (1) {        float distancia = medir_distancia(trig_line, echo_line);        if (distancia >= 20 && distancia <= 30) {            system("sudo /./home/grupo2/on17.sh");            system("sudo /./home/grupo2/off21.sh");            system("sudo /./home/grupo2/off27.sh");        } else if (distancia > 10 && distancia < 20) {            system("sudo /./home/grupo2/on21.sh");            system("sudo /./home/grupo2/off17.sh");            system("sudo /./home/grupo2/off27.sh");        } else if (distancia <= 10) {            system("sudo /./home/grupo2/on27.sh");            system("sudo /./home/grupo2/off21.sh");            system("sudo /./home/grupo2/off17.sh");        } else {            system("sudo /./home/grupo2/off27.sh");            system("sudo /./home/grupo2/off21.sh");            system("sudo /./home/grupo2/off17.sh");        }        printf("Distancia medida: %.2f cm\n", distancia);        sleep(1);  // Medir cada segundo    }    // Liberar recursos    gpiod_line_release(trig_line);    gpiod_line_release(echo_line);    gpiod_chip_close(chip);    return 0;}