import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import time

HOST = ''
PORT = 8083

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Servidor criado!')

try:
    server.bind((HOST, PORT))
except socket.error as msg:
	print('Falha ao iniciar o servico. Codigo do erro: ' + str(msg[0]) + ': ' + msg[1])
	sys.exit()
	
print('Servidor iniciado!')

server.listen(1)
print('Servidor aguardando conexao!')

conn, addr = server.accept()
print('Cliente conectado ' + addr[0] + ':' + str(addr[1]) + '.')

cap = cv2.VideoCapture('drop.avi')
time.sleep(1)

while True:
    ret,frame = cap.read()
    data = pickle.dumps(frame)
    conn.sendall(struct.pack("L", len(data)) + data)
    print('Video sendo transmitido!')
    
server.close()
