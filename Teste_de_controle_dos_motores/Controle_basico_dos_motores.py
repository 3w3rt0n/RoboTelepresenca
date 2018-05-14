#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Interface básica para controle dos motores
Desenvolvedor: Ewerton L. de Sousa
"""

import serial,sys, glob

from ttk import Frame, Label, Combobox
from Tkinter import *


class Frame1(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
        
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
        
        self.lbox = Listbox(self, height = 10, width = 55)
        sbar = Scrollbar(self, command=self.lbox.yview)
        sbar.place(x=360, y=240)
        self.lbox.config(yscrollcommand=sbar.set)
        self.lbox.place(x=10, y=240)

        self.lbox.insert('end',  "Interface Básica de Controle dos Motores - v1.0")
        self.lbox.insert('end', "S.O. (%s)"  % (sys.platform))
      
        self.parent.title("Interface básica para controle dos motores - v1.0")
        self.pack(fill=BOTH, expand=1)

        self.opts = ""
        self.cbox = Combobox(self, textvariable=self.opts, state='readonly')
        for n,s in scan():
            self.opts += "%s " % (s)
              
        self.cbox['values'] = self.opts
        if(self.opts != ""):
            self.cbox.current(0)
        self.cbox.place(x=10, y=10)
        "self.cbox.bind('<<ComboboxSelected>>', self.conectar)"

        btConectar = Button(self, text="Conectar", width=10)
        btConectar.bind("<Button-1>", self.conectar)
        btConectar.place(x=200, y=10)
        
        btFrente = Button(self, text="/\\", width=5)
        btFrente.bind("<Button-1>", self.comandoF)
        btFrente.place(x=160, y=100)
        btTraz = Button(self, text="\/", width=5)
        btTraz.bind("<Button-1>", self.comandoT)
        btTraz.place(x=160, y=130)

        btEsqFrente = Button(self, text="/\\", width=5)
        btEsqFrente.place(x=50, y=70)
        btEsqFrente.bind("<Button-1>", self.comandoEF)
        btEsqTraz = Button(self, text="\/", width=5)
        btEsqTraz.place(x=50, y=150)
        btEsqTraz.bind("<Button-1>", self.comandoET)

        btDirFrente = Button(self, text="/\\", width=5)
        btDirFrente.place(x=260, y=70)
        btDirFrente.bind("<Button-1>", self.comandoDF)
        btDirTraz = Button(self, text="\/", width=5)
        btDirTraz.place(x=260, y=150)
        btDirTraz.bind("<Button-1>", self.comandoDT)

        btGiraEsq = Button(self, text=">>", width=5)
        btGiraEsq.place(x=90, y=200)
        btGiraEsq.bind("<Button-1>", self.comandoGE)
        btParar = Button(self, text="-x-", width=5)
        btParar.place(x=160, y=200)
        btParar.bind("<Button-1>", self.comandoP)
        btGiraDir = Button(self, text="<<", width=5)
        btGiraDir.place(x=230, y=200)
        btGiraDir.bind("<Button-1>", self.comandoGD)  
        

    def conectar(self, event):
        self.lbox.insert('end', "conectando...")
        self.lbox.insert('end', "Porta:", self.cbox.get())
        self.lbox.insert('end', "Baund: 9600")

        self.arduino = None   

        try:
            self.arduino = serial.Serial(self.cbox.get(), 9600);
            self.lbox.insert('end', "Conectado! \n")
        
            try:
               self.lbox.insert('end', self.arduino.readline() )
               self.lbox.insert('end', self.arduino.readline())
               self.lbox.insert('end', self.arduino.readline())
               self.lbox.insert('end', self.arduino.readline())
                   
            except serial.serialutil.SerialException:
               pass
        except:
            pass
        finally:
            if self.arduino:
                "self.arduino.close()"
                pass
            
    def comandoP(self, event):
        self.lbox.insert('0', "Comando 3000")
        try:
            self.arduino.write("3000\n")
            self.lbox.insert('0', self.arduino.readline() )
        except:
            pass
        
    def comandoF(self, event):
        self.lbox.insert('0', "Comando 3300")
        try:
            self.arduino.write("3300\n")
            self.lbox.insert('0', self.arduino.readline() )
        except:
            pass

    def comandoT(self, event):
        self.lbox.insert('0', "Comando 3700")
        try:
            self.arduino.write("3700\n")
            self.lbox.insert('0', self.arduino.readline() )
        except:
            pass

    def comandoEF(self, event):
        self.lbox.insert('0', "Comando 2300")
        try:
            self.arduino.write("2300\n")
            self.lbox.insert('0', self.arduino.readline())
        except:
            pass

    def comandoET(self, event):
        self.lbox.insert('0', "Comando 2700")
        try:
            self.arduino.write("2700\n")
            self.lbox.insert('0',  self.arduino.readline())
        except:
            pass

    def comandoDF(self, event):
        self.lbox.insert('0',  "Comando 1300")
        try:
            self.arduino.write("1300\n")
            self.lbox.insert('0',  self.arduino.readline())
        except:
            pass

    def comandoDT(self, event):
        self.lbox.insert('0',  "Comando 1700")
        try:
            self.arduino.write("1700\n")
            self.lbox.insert('0',  self.arduino.readline())
        except:
            pass

    def comandoGE(self, event):
        self.lbox.insert('0',  "Comando 4300")
        try:
            self.arduino.write("4300\n")
            self.lbox.insert('0',  self.arduino.readline() )
        except:
            pass

    def comandoGD(self, event):
        self.lbox.insert('0',  "Comando 4700")
        try:
            self.arduino.write("4700\n")
            self.lbox.insert('0',  self.arduino.readline() )
        except:
            pass


        
def scan():
    """scan for available ports. return a list of tuples (num, name)"""
    available = []
    
    if sys.platform.startswith('linux'): 
        available.append((0, glob.glob('/dev/ttyS*')[0] ))
        available.append((1, glob.glob('/dev/ttyUSB*')[0]))
        """available.append((2, glob.glob('/dev/ttyACM*')[0]))"""
        available.append((3, glob.glob('/dev/serial/by-id/*')[0]))
        return available
    
    elif sys.platform.startswith('win'): 
        
        for i in range(256):
           try:
                s = serial.Serial(i)
                available.append((i, s.portstr))
                s.close()   # explicit close 'cause of delayed GC in java
           except serial.SerialException:
                pass
        return available
    else: self.lbox.insert('end',  "S.O. não suportado!")
    
    return None    


def main():
    
    def teclado(event):
        app.lbox.insert('end',  "Tecla: %d" % event.keycode)

        if event.keycode == 39:
            app.lbox.insert('0',  "Direita")
            app.arduino.write("4700\n")            
            app.lbox.insert('0',  app.arduino.readline())
        elif event.keycode == 40:
            app.lbox.insert('0',  "Tras")
            app.arduino.write("3700\n")            
            app.lbox.insert('0',  app.arduino.readline() )
        elif event.keycode == 38:
            app.lbox.insert('0',  "Frente")
            app.arduino.write("3300\n")            
            app.lbox.insert('0',  app.arduino.readline() )
        elif event.keycode == 37:
            app.lbox.insert('0',  "Esquerda")
            app.arduino.write("4300\n")            
            app.lbox.insert('0',  app.arduino.readline())
        elif event.keycode == 32:
            app.lbox.insert('0',  "Parado")
            app.arduino.write("3000\n")            
            app.lbox.insert('0',  app.arduino.readline())
            
    root = Tk()
    root.geometry("400x420")
    app = Frame1(root)
    app.bind_all("<KeyPress>", teclado)
    root.mainloop()  


if __name__ == '__main__':
    main()

