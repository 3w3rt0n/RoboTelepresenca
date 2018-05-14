import socket
import sys
import cv2
import pickle
import numpy as np
import struct
#Tela
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os

# Definicoes

HOST = '127.0.0.1'
PORT = 8083


#Classe da tela
class Tela:
    
    def __init__(self):
       #Conecao de rede 
       self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       print('[INFO] Cliente iniciado!')

       self.cliente.connect((HOST, PORT))
       print('[INFO] Cliente conectado.')
       print('[INFO] Endereco do servidor: ' + HOST + ':' + str(PORT) + '.')

       self.data = b''
       self.payload_size = struct.calcsize("L")
       
       #Inicializacao do tkinter
       self.frame = None
       self.thread = None
       self.stopEvent = None

	   # initialize the root window and image panel
       self.root = tki.Tk()       
       self.root.resizable(width=False, height=False)
       self.root.geometry('800x600')
       #self.root.resizable(0, 0)
       self.panel = None
       
       # Formulario para conexão
       

	   # create a button, that when pressed, will take the current
	   # frame and save it to file
       btn = tki.Button(self.root, text="Conectar...", command=self.conectar)
       btn.pack(side="right", fill="both", expand="yes", padx=10,pady=10)

	   # start a thread that constantly pools the video sensor for
	   # the most recently read frame
       self.stopEvent = threading.Event()
       self.thread = threading.Thread(target=self.videoLoop, args=())
       self.thread.start()

       # set a callback to handle when the window is closed
       self.root.wm_title("Robo de teçepresenca - v1.0.0")       
       self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
   
    def videoLoop(self):
      # DISCLAIMER:
	  # I'm not a GUI developer, nor do I even pretend to be. This
	  # try/except statement is a pretty ugly hack to get around
	  # a RunTime error that Tkinter throws due to threading
      try:
		# keep looping over frames until we are instructed to stop
          while not self.stopEvent.is_set():
      
             while True:
               while len(self.data) < self.payload_size:
                   self.data += self.cliente.recv(4096)
                    
               self.packed_msg_size = self.data[:self.payload_size]
            
               self.data = self.data[self.payload_size:]
               self.msg_size = struct.unpack("L", self.packed_msg_size)[0]
            
               while len(self.data) < self.msg_size:
                   self.data += self.cliente.recv(4096)
                    
               self.frame_data = self.data[:self.msg_size]
               self.data = self.data[self.msg_size:]
            
               self.frame=pickle.loads(self.frame_data)
               print('[INFO] Resolucao: ' + str(self.frame.size) + 'px.')
               
		       # grab the frame from the video stream and resize it to
	      	   # have a maximum width of 300 pixels
               self.frame = imutils.resize(self.frame, width=300)
		
			   # OpenCV represents images in BGR order; however PIL
			   # represents images in RGB order, so we need to swap
			   # the channels, then convert to PIL and ImageTk format
               image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
               image = Image.fromarray(image)
               image = ImageTk.PhotoImage(image)
		
			   # if the panel is not None, we need to initialize it
               if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)
		
			   # otherwise, simply update the panel
               else:
                    self.panel.configure(image=image)
                    self.panel.image = image

      except RuntimeError as e:
          print("[INFO] caught a RuntimeError")
          
    def conectar(self):
       # grab the current timestamp and use it to construct the
	   # output path
       ts = datetime.datetime.now()
       filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
       p = os.path.sep.join((self.outputPath, filename))

       # save the file
       cv2.imwrite(p, self.frame.copy())
       print("[INFO] saved {}".format(filename))

    def onClose(self):
       # set the stop event, cleanup the camera, and allow the rest of
	   # the quit process to continue
       print("[INFO] closing...")
       self.stopEvent.set()
       self.root.quit()
       self.cliente.close()
         
         
# start the app
print("[INFO] starting...")
pba = Tela()
pba.root.mainloop()
       






