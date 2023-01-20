import tkinter as tk
import socket
from tkinter import filedialog

window = tk.Tk()  # Invocar TK en window
#IP
iplbl = tk.Label(window, text="IP 3DS :")  # Texto
ipfield = tk.Entry(window, width=14, justify="center", bd=4)  # Campo
ipfield.insert(0, "192.168.110.56")  # Texto Temporal
iplbl.place(x=10, y=20)  # Pos Texto
ipfield.place(x=55, y=20)  # Pos Campo
#port
portlbl = tk.Label(window, text="Puerto :")
portfield = tk.Entry(window, width=6, justify="center", bd=4)  # Campo
portfield.insert(0, "5000")
portfield.place(x=210, y=20)
portlbl.place(x=160, y=20)
#Host
print('Detecting host IP...')
hostname = socket.gethostname()
hostingIp:str = socket.gethostbyname(hostname)

def explorar(): #File browser
    nombre = filedialog.askopenfilename(initialdir="/",
                                        title="Select a File",
                                        filetypes=(("Archivos .CIA",
                                                    "*.cia*"),
                                                   ("all files",
                                                    "*.*")))

    # Change label contents
    fblbl.configure(text="Archivo: " + nombre)
    fbroot.insert(0,nombre)

fblbl = tk.Label(window, text="Seleccionar Archivo Cia:")
fbroot = tk.Entry(window, bd=6)
fbroot.place(x=150, y=100)
fblbl.place(x=20, y=80)
buscar = tk.Button(window, text="Buscar Archivo", command=lambda: explorar())
buscar.place(x=40, y=100)



class data: #Objeto con los datos
    def __init__(self,ip,port,open,host):
        self.ip = ip
        self.port = port
        self.open = open
        self.hostip = host
        
console = data(ipfield.get(),portfield.get(),fbroot.get(),hostingIp)
a = console.ip
b = console.port
c = console.open
d = console.hostip
def test():
    print(a,b,c,d)
    return([a,b,c,d])

punch = tk.Button(window, text="Send", fg="green",command=lambda:test())# Boton de Prueba
punch.place(x=100, y=150)
window.title("Prueba Gay")
window.geometry("300x200")
window.mainloop()