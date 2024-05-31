#Imports Server
import os
import socket
import struct
import sys
import threading
import time
import urllib
#Imports UI
import tkinter as tk
import customtkinter
from tkinter import simpledialog, filedialog, messagebox
from CTkTable import *

try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import TCPServer
    from urllib import quote

except ImportError:
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer
    from urllib.parse import quote

#Extenciones soportadas y puertodefault
fileExtension = [('Archivos 3DS Compatibles (.cia .tik .cetk .3dsx)','.cia .tik .cetk .3dsx')]
hostPort = 8080

def UIWindow():
    #Tema CTkinter
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("green")

    #InicializarCtk
    app = customtkinter.CTk()
    app.geometry("400x500")
    app.title("GaySex")
    app.grid_anchor("center")

    #Titulo
    tiTXT = "3DS Cia Sender"
    titulo= customtkinter.CTkLabel(app, text=tiTXT, width=60, height=80, fg_color='transparent')
    titulo.grid(column=0,row=0,columnspan=2)

    app.grid_rowconfigure(3,pad=10)
    app.grid_rowconfigure(4,pad=10)
    app.grid_rowconfigure(5,pad=20)
    app.grid_rowconfigure(5,pad=20)
    app.grid_rowconfigure(7,pad=20)

    #FileInput 
    fileinput = customtkinter.CTkLabel(app,width=20,height=40, text="Seleccionar Archivo : ")
    fileinput.grid(column=0,row=2)
    filelist = []
    filelook = customtkinter.CTkButton(app,text="Buscar Archivo",command=lambda: filePicker(alert,filelist,filetable))
    filelook.grid(column=1,row=2)
    

    #3DS IP
    iplabel = customtkinter.CTkLabel(app, text='IP Consola 3DS : ', width=40, height=28, fg_color='transparent')
    iplabel.grid(column=0,row=3)
    ipclient = customtkinter.CTkEntry(app,width=140,height=28, placeholder_text="192.168.0.15")
    ipclient.grid(column=1,row=3)

    #3DS Puerto
    hostlabel = customtkinter.CTkLabel(app, text='IP Host(o dejar en blanco para detectar IP) : ', width=40, height=28, fg_color='transparent')
    hostlabel.grid(column=0 ,row=4)
    hostip = customtkinter.CTkEntry(app, placeholder_text='5000', width=140, height=28)
    hostip.grid(column=1, row=4)

    #Subir
    enviar = customtkinter.CTkButton(app, text='Enviar', width=140, height=28,command=lambda:Send(ipclient,hostip,filelist,alert,progresoTarea,porcentaje,cola))
    enviar.grid(column=0, row=5, columnspan=2)

    #Alerta
    alert = customtkinter.CTkLabel(app, text='', width=40, height=28, fg_color='transparent')
    alert.grid(column=0 ,row=6, columnspan=2)

    #Progressbar
    progresoTarea = customtkinter.CTkProgressBar(app, orientation='horizontal',mode="determinate",determinate_speed=1,progress_color="#2fa572",width=200)
    progresoTarea.set(-1)
    progresoTarea.grid(column=0, row=8,columnspan=2, pady=10)
    cola = customtkinter.CTkLabel(app, text='', width=40, height=28, fg_color='transparent')
    cola.grid(column=0 ,row=7)
    porcentaje = customtkinter.CTkLabel(app, text='', width=40, height=28, fg_color='transparent')
    porcentaje.grid(column=1 ,row=7)

    #Frame
    frame = customtkinter.CTkFrame(app, width=350, height=200)
    frame.grid(column=0, row=9, columnspan = 2)

    #Table
    filetable = CTkTable(master=frame,column=2,header_color="#2fa572")
    filetable.grid(column=0, row=9, columnspan = 2, sticky="ew" ,padx=20,pady=20)
    filetable.insert(row=0,column=0, value="Directorio")
    filetable.insert(row=0,column=1, value="Archivo")
    filetable.delete_row(1)

    def filePicker(alert,filelist,filetable):
        
        files = customtkinter.filedialog.askopenfiles(title="Seleccionar Archivo o Carpeta",filetypes=(fileExtension))#Seleccionar Archivos
        alert.configure(text="",text_color="white") #Limpiar Alertas
        filelist.clear() #Limpiar Lista de archivos

        #Limpiar Tabla
        while filetable.rows > 1:
            a = filetable.rows
            filetable.delete_row(a)

        #Si la lista no esta vacia llenar la tabla y crear la lista de archivos
        if files:
            for index, file in enumerate(files):
                file_path = file.name
                directory, filename = os.path.split(file_path)
                filelist.append(directory+"/"+filename) # Agrega el archivo a filelist
                filetable.add_row(values=["",""])
                filetable.insert(row=index+1, column=0, value=directory)  # Inserta el directorio en la tabla
                filetable.insert(row=index+1, column=1, value=filename)

        else:
            alert.configure(text="Ningun Archivo Seleccionado",text_color="red")

        
        return filelist

    #RunCTk
    app.mainloop()

def StartServer(hostIp, hostPort,alert):
    try:
        server = TCPServer((hostIp, hostPort), SimpleHTTPRequestHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()       
        return server
    
    except Exception as e:
        print("Error starting server:", e)
        return None

def PrepareSend(filelist,hostIP,hostPort,alert):

    alert.configure(text="Preparando Envio... ",text_color="white")
    #crear path y url
    baseUrl = hostIP+":"+str(hostPort)+"/"
    fileurl = ''
    filepath = ''
    for file in filelist:
        filepath = file.strip()
        fileurl += baseUrl+quote(os.path.basename(filepath))+'\n'

    #inicializar lista de bytes
    filelistbytes = fileurl.encode("ascii")
    #Cambiar directorio para servir archivos
    directory = os.path.dirname(filepath)
    os.chdir(directory)

    return filelistbytes

def Send(ipclient,hostip,filelist,alert,progresoTarea,porcentaje,cola):
    
    #Obtener datos
    clientIp = ipclient.get()
    hostIp = hostip.get()

    if not clientIp:
        alert.configure(text="IP 3DS No puede quedar en blanco",text_color="red")
        
    
    if not hostIp:
        hostIp = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
                    [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

    server = StartServer(hostIp,8080,alert)

    filebytes = PrepareSend(filelist,hostIp,hostPort,alert)
    DataThread(clientIp,filebytes,alert,progresoTarea,porcentaje,cola)

    server.shutdown()

def DataTransfer(clientIp,filebytes,alert,progresoTarea,porcentaje,cola):

    #Iniciar Transferencia
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((clientIp,5000))
        sock.sendall(struct.pack('!L',len(filebytes))+filebytes)
        while len(sock.recv(1)) < 1:
            time.sleep(0.05)
        alert.configure(text="Envio Exitoso", text_color="#2fa572")

    except Exception as e:
        alert.configure(text="Envio Fallido", text_color="red")
        print('An error occurred: ' + str(e))
        return False
    
    finally:
        sock.close()

def DataThread(clientIp,filebytes,alert,progresoTarea,porcentaje,cola):
    transferthread = threading.Thread(target=DataTransfer,args=(clientIp,filebytes,alert,progresoTarea,porcentaje,cola))
    transferthread.start()

def main():
    event = threading.Event()
    ui_thread = threading.Thread(target=UIWindow)
    ui_thread.start()
    event.wait()

if __name__ == "__main__":
    main()
