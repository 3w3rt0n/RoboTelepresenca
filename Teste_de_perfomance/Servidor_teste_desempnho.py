import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import time
from datetime import datetime

HOST = ''
PORT = 8083

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Servidor criado!')

server.bind((HOST, PORT))	
print('Servidor iniciado!')

server.listen(1)
print('Servidor aguardando conexao!')

conn, addr = server.accept()
print('Cliente conectado ' + addr[0] + ':' + str(addr[1]) + '.')

cap = cv2.VideoCapture('drop.avi')

print('Sistema (byteorder): ' + sys.byteorder)
print('Tamanho do inteiro (Byte): ' + str(sys.getsizeof(int())) + 'B')
print('Tamanhos por struct')
print('Tamanho do short (Byte): ' + str(struct.calcsize("h")) + 'B')
print('Tamanho do inteiro (Byte): ' + str(struct.calcsize("i")) + 'B')
print('Tamanho do long (Byte): ' + str(struct.calcsize("l")) + 'B')
print('Tamanho do floar (Byte): ' + str(struct.calcsize("f")) + 'B')
print('Tamanho do double (Byte): ' + str(struct.calcsize("d")) + 'B')
print('String encoding: ' + sys.getdefaultencoding())
print('Plataforma: ' + sys.platform)
print('Versao do python: ' + sys.version) 
print('Versao do C: ' + str(sys.api_version))
print('=====================================')

time.sleep(1)
t5 = datetime.now()
ret,frame = cap.read()
print('Frame arquivo: ' + str(len(frame)))


# Registra o momento antes do teste
t0 = datetime.now()
data = pickle.dumps(frame, protocol=pickle.HIGHEST_PROTOCOL)
t1 = datetime.now()
# Calcula o tempo de execucao das N operacoes executadas
diff = t1 - t0
print('Tempo de execucao: ' + str(diff.total_seconds()) + 'ms')
print('Frame serializado: ' + str(len(data)))

# Registra o momento antes do teste
t0 = datetime.now()
estrutura = struct.pack("L", len(data)) + data
print('Estrutura: ' + str(len(estrutura)))
conn.sendall(estrutura)
t1 = datetime.now()
# Calcula o tempo de execucao das N operacoes executadas
diff = t1 - t0
print('Tempo de execucao: ' + str(diff.total_seconds()) + 'ms')
print('Transmitido!')

t6 = datetime.now()
diff = t6 - t5
print('Tempo total: ' + str(diff.total_seconds()) + 'ms')
    
server.close()
