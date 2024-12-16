#Control gpio
# Developer: Universidad
### Zona de librerias

from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import os
import subprocess
import time

# Crear Ventana
v0 = Tk()
v0.title("Raspi Control")
v0.geometry("700x500+0+0")

text3 = font.Font(family="Arial", size=80)
#Declarar varibles tipo imagen
img_on=PhotoImage(file="/home/grupo2/on.gif")
img_off=PhotoImage(file="/home/grupo2/off.gif")

#Etiquetas de gpio's
text_lenguaje = font.Font(family="Arial", weight="bold")
lb_gpi17=Label(v0, text="GPIO17").place(x=170, y=80)
lb_gpi21=Label(v0, text="GPIO21").place(x=310, y=80)
lb_gpi27=Label(v0, text="GPIO27").place(x=450, y=80)



#Declarar funciones para actualiza estado de gpio's    
def actualizaGpio17():
    os.system("gpio read 17 > estado.txt")
    global status17
    status17=StringVar()
    pf=open("/home/grupo2/estado.txt", "r")
    for linea in pf:
        campo=linea.split("\n")
        campof=campo[0]
        status17 = campo[0]
        if (campof=="0"):
            btn_img_on=Button(v0,image=img_on).place(x=150,y=100)
            v0.after(1000,actualizaGpio17)
        if (campof=="1"):
            btn_img_off=Button(v0,image=img_off).place(x=150,y=100)
            v0.after(1000,actualizaGpio17)


def actualizaGpio27():
    os.system("gpio read 27 > estado27.txt")
    global status27
    status27=StringVar()
    pf=open("/home/grupo2/estado27.txt", "r")
    for linea in pf:
        campo=linea.split("\n")
        campof=campo[0]
        status27 = campo[0]
        if (campof=="0"):
            btn_img_on=Button(v0,image=img_on).place(x=290,y=100)
            v0.after(1000,actualizaGpio27)
        if (campof=="1"):
            btn_img_off=Button(v0,image=img_off).place(x=290,y=100)
            v0.after(1000,actualizaGpio27)

            
def actualizaGpio21():
    os.system("gpio read 21 > estado21.txt")
    global status21
    status21=StringVar()
    pf=open("/home/grupo2/estado21.txt", "r")
    for linea in pf:
        campo=linea.split("\n")
        campof=campo[0]
        status22 = campo[0]
        if (campof=="0"):
            btn_img_on=Button(v0,image=img_on).place(x=430,y=100)
            v0.after(1000,actualizaGpio21)
        if (campof=="1"):
            btn_img_off=Button(v0,image=img_off).place(x=430,y=100)
            v0.after(1000,actualizaGpio21)


  
#Llamar funciones recursivas en el load del programa
actualizaGpio17()
actualizaGpio21()
actualizaGpio27()
##                          gpio 17
def encender_sh_17():
    print("Encendido sh 17...")
    os.system("sudo /./home/grupo2/on17.sh")

def apagar_sh_17():
    print("Apagado sh 17...")
    os.system("sudo /./home/grupo2/off17.sh")


def encender_sh_21():
    print("Encendido sh 21...")
    os.system("sudo /./home/grupo2/on21.sh")

def apagar_sh_21():
    print("Apagado sh 21...")
    os.system("sudo /./home/grupo2/off21.sh")


##                          gpio 27
def encender_sh_27():
    print("Encendido sh 27...")
    os.system("sudo /./home/grupo2/on27.sh")

def apagar_sh_27():
    print("Apagado sh 27...")
    os.system("sudo /./home/grupo2/off27.sh")




##funciones con los lenguajes
def encenderultraso():
    print("Ultrasonico...")
    os.system("sudo /./home/grupo2/ultraso &")
    

def encenderPir():
    print("Pir...")
    os.system("sudo /./home/grupo2/SensorC &")

def encenderTemp():
    print("Pir...")
    os.system("source mi_entorno/bin/activate")
    os.system("sudo /./home/grupo2/temp &")
    



def encenderultrasoP():
    print("Ultrasonico...")
    os.system("sudo /./home/grupo2/ultrasonico.py &")

def encenderPirP():
    try:
        print("Ejecutando sensorPir.py...")
        # Ejecutar el script en segundo plano
        subprocess.Popen(["python3", "/home/grupo2/sensorPir.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("sensorPir.py iniciado correctamente.")
    except Exception as e:
        print(f"Error al ejecutar sensorPir.py: {e}")

def encenderPirB():
    try:
        print("Ejecutando sensorPir.bash...")
        # Ejecutar el script bash en segundo plano
        subprocess.Popen(["bash", "/home/grupo2/sensorPir.bash"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("sensorPir.bash iniciado correctamente.")
    except Exception as e:
        print(f"Error al ejecutar sensorPir.bash: {e}")

def encenderTempP():
    try:
        print("Ejecutando temperatura.py...")
        # Activar el entorno virtual
        activate_env = subprocess.run(["source", "mi_entorno/bin/activate"], shell=True, executable="/bin/bash")
        if activate_env.returncode == 0:  # Verificar si la activación fue exitosa
            # Ejecutar el script de temperatura con privilegios sudo
            subprocess.Popen(["sudo", "python3", "/home/grupo2/temperatura.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("temperatura.py iniciado correctamente.")
        else:
            print("No se pudo activar el entorno virtual.")
    except Exception as e:
        print(f"Error al ejecutar temperatura.py: {e}")

def detener():
    print("detener...")
    os.system("sudo /./home/grupo2/detener.sh &")
    

def EvaluarEmail():
    ckm = ckemail.get()

    if ckm == "1":
        os.system("sudo /home/grupo2/lectura.sh")
        messagebox.showinfo("save", message="Email Service --enabled--")

    elif ckm == "0":
        os.system("sudo pkill -f lectura.sh")
        messagebox.showinfo("save", message="Email Service --disabled--")

def Tiempo():
    ct=str(checkt.get())
    
    if(ct=="1"):
        def Registrar():
            print("Registrar")
            hora_inicio=str(_horaInicial.get())
            min_inicio=str(_minInicial.get())
            hora_fin=str(_horaFinal.get())
            min_fin=str(_minFinal.get())
            tab=" "
            dia="*"
            mes="*"
            anio="*"
            user="root"
            path1="/home/grupo2/on17.sh"
            path2="/home/grupo2/off17.sh"
            
            path3="/home/grupo2/on27.sh"
            path4="/home/grupo2/off27.sh"

            path5="/home/grupo2/on21.sh"
            path6="/home/grupo2/off21.sh"
            cadena1=(str(min_inicio)+''+str(tab)+''+str(hora_inicio)+''+str(tab)+''+str(dia)+''+str(tab)+''+str(mes)+''+str(tab)+''+str(anio)+''+str(tab)+''+str(user)+''+str(tab)+''+str(path1))
            cadena2=(str(min_fin)+''+str(tab)+''+str(hora_fin)+''+str(tab)+''+str(dia)+''+str(tab)+''+str(mes)+''+str(tab)+''+str(anio)+''+str(tab)+''+str(user)+''+str(tab)+''+str(path2))

            cadena3=(str(min_inicio)+''+str(tab)+''+str(hora_inicio)+''+str(tab)+''+str(dia)+''+str(tab)+''+str(mes)+''+str(tab)+''+str(anio)+''+str(tab)+''+str(user)+''+str(tab)+''+str(path3))
            cadena4=(str(min_fin)+''+str(tab)+''+str(hora_fin)+''+str(tab)+''+str(dia)+''+str(tab)+''+str(mes)+''+str(tab)+''+str(anio)+''+str(tab)+''+str(user)+''+str(tab)+''+str(path4))

            cadena5=(str(min_inicio)+''+str(tab)+''+str(hora_inicio)+''+str(tab)+''+str(dia)+''+str(tab)+''+str(mes)+''+str(tab)+''+str(anio)+''+str(tab)+''+str(user)+''+str(tab)+''+str(path5))
            cadena6=(str(min_fin)+''+str(tab)+''+str(hora_fin)+''+str(tab)+''+str(dia)+''+str(tab)+''+str(mes)+''+str(tab)+''+str(anio)+''+str(tab)+''+str(user)+''+str(tab)+''+str(path6))
            

            #permisos 777
            os.system("sudo chmod -R 777 /etc/cron.d/task1")
            os.system("sudo chmod -R 777 /etc/cron.d/task2")
            os.system("sudo chmod -R 777 /etc/cron.d/tarea1")
            os.system("sudo chmod -R 777 /etc/cron.d/tarea2")
            os.system("sudo chmod -R 777 /etc/cron.d/task1")
            os.system("sudo chmod -R 777 /etc/cron.d/task2")

            #abrir archivo en modo escritura
            pf1=open("/etc/cron.d/task1", "w")
            pf1.write(cadena1)
            pf1.write("\n")
            pf1.close()

            pf2=open("/etc/cron.d/task2", "w")
            pf2.write(cadena2)
            pf2.write("\n")
            pf2.close()

            pf3=open("/etc/cron.d/tarea1", "w")
            pf3.write(cadena3)
            pf3.write("\n")
            pf3.close()

            pf4=open("/etc/cron.d/tarea2", "w")
            pf4.write(cadena4)
            pf4.write("\n")
            pf4.close()

            pf5=open("/etc/cron.d/task1", "w")
            pf5.write(cadena5)
            pf5.write("\n")
            pf5.close()

            pf6=open("/etc/cron.d/task2", "w")
            pf6.write(cadena6)
            pf6.write("\n")
            pf6.close()

            #pause
            time.sleep(0.1)

            #reversion de permisos 755
            os.system("sudo chmod -R 755 /etc/cron.d/task1")
            os.system("sudo chmod -R 755 /etc/cron.d/task2")
            os.system("sudo chmod -R 755 /etc/cron.d/tarea1")
            os.system("sudo chmod -R 755 /etc/cron.d/tarea2")
            os.system("sudo chmod -R 755 /etc/cron.d/task1")
            os.system("sudo chmod -R 755 /etc/cron.d/task2")
            os.system("sudo /./etc/init.d/cron restart")
            
        v1=Toplevel()
        v1.title("Configuracion de Tiempo")
        v1.geometry("300x150+80+150")
        txt_v1=font.Font(family="Arial", size=12)
        #etiquetas
        lb_timei=Label(v1,text="  Tiempo Inicial en hh:mm", font=txt_v1).place(x=50,y=10)
        global _horaInicial, _minInicial, _horaFinal, _minFinal
        _horaInicial=StringVar()
        _minInicial=StringVar()
        _horaFinal=StringVar()
        _minFinal=StringVar()
        txt_horaInicial=Entry(v1, textvariable=_horaInicial, width=3).place(x=120, y=30)
        lb_1 = Label(v1, text=":").place(x=150,y=30)
        txt_minInicial=Entry(v1, textvariable=_minInicial, width=3).place(x=160, y=30)
        
        lb_timef=Label(v1,text="   Tiempo Final en hh:mm", font=txt_v1).place(x=50,y=70)
        txt_horaFinal=Entry(v1, textvariable=_horaFinal, width=3).place(x=120, y=90)
        lb_1 = Label(v1, text=":").place(x=150,y=90)
        txt_minFinal=Entry(v1, textvariable=_minFinal, width=3).place(x=160, y=90)

        btn_registrar=Button(v1, text="Registrar", fg="green", command=Registrar).place(x=100, y=120)
        v1.mainloop()
        
#Declaracion de tipo de fuente
text1 = font.Font(family="Arial", size=20)
text2 = font.Font(family="Helvetica", size=12)

#Zona de etiquetas
label_titulo = Label(v0, text="--- RASPI CONTROL---", font=text1).place(x=200, y=10)
label_A = Label(v0, text=".sh", font=text1).place(x=50, y=200)
label_A = Label(v0, text=".C", font=text1).place(x=50, y=240)
label_A = Label(v0, text=".bash", font=text1).place(x=50, y=280)
label_A = Label(v0, text=".py", font=text1).place(x=50, y=310)

#Zona de botones
btn_on_sh_17 = Button(v0, text="ON", command=encender_sh_17).place(x=200, y=200)
btn_off_sh_17 =Button(v0, text="OFF", command=apagar_sh_17).place(x=150, y=200)

btn_on_sh_27 = Button(v0, text="ON", command=encender_sh_21).place(x=340, y=200)
btn_off_sh_27 =Button(v0, text="OFF", command=apagar_sh_21).place(x=300, y=200)

btn_on_sh_21 = Button(v0, text="ON", command=encender_sh_27).place(x=480, y=200)
btn_off_sh_21 =Button(v0, text="OFF", command=apagar_sh_27).place(x=430, y=200)

btn_onU = Button(v0, text="Ultrasonico", command=encenderultraso).place(x=150, y=240)
btn_onP = Button(v0, text="Pir", command=encenderPir).place(x=300, y=240)
btn_onT = Button(v0, text="Temperatura", command=encenderTemp).place(x=430, y=240)


btnTem = Button(v0, text="Pir", command=encenderPirB).place(x=300, y=280)


btnPir1 = Button(v0, text="Ultrasonico py", command=encenderultraso).place(x=150, y=320)
btnTem1 = Button(v0, text="Pir py", command=encenderPir).place(x=300, y=320)
btnUltra1 =Button(v0, text="Temperatura py", command=encenderTemp).place(x=430, y=320)

Detener =Button(v0, text="Detener", command=detener).place(x=150, y=380)

v0.mainloop()
