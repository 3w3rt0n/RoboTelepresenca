import socket
import sys
import cv2
import pickle
import numpy as np
import struct
from datetime import datetime

HOST = '127.0.0.1'
PORT = 8083

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Cliente iniciado!')

cliente.connect((HOST, PORT))
print('Cliente conectado.')
print('Endereco do servidor: ' + HOST + ':' + str(PORT) + '.')

data = b''
payload_size = struct.calcsize("L")

#intelx86 amd64 little
#arm bi-little
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

t5 = datetime.now()
# Registra o momento antes do teste
t0 = datetime.now()
while len(data) < payload_size:
	t9 = datetime.now()
	data += cliente.recv(8048)
	t1 = datetime.now()
	diff = t1 - t0
	print('[9] ' + str(diff.total_seconds()) + 'ms')
packed_msg_size = data[:payload_size]
# Calcula o tempo de execucao das N operacoes executadas
t1 = datetime.now()
diff = t1 - t0
print('[1]Tempo de execucao: ' + str(diff.total_seconds()) + 'ms')
print('Frame serializado: ' + str(len(data)))


# Registra o momento antes do teste
t0 = datetime.now()
data = data[payload_size:]
msg_size = struct.unpack("L", packed_msg_size)[0]
# Calcula o tempo de execucao das N operacoes executadas
t1 = datetime.now()
diff = t1 - t0
print('Tempo de execucao: ' + str(diff.total_seconds()) + 'ms')
print('Frame deserializado: ' + str(msg_size))

# Registra o momento antes do teste
t0 = datetime.now()
while len(data) < msg_size:
    data += cliente.recv(4096)
frame_data = data[:msg_size]
data = data[msg_size:]
# Calcula o tempo de execucao das N operacoes executadas
t1 = datetime.now()
diff = t1 - t0
print('Tempo de execucao: ' + str(diff.total_seconds()) + 'ms')
print('Frame msg: ' + str(len(data)))

# Registra o momento antes do teste
t0 = datetime.now()
frame=pickle.loads(frame_data)
# Calcula o tempo de execucao das N operacoes executadas
t1 = datetime.now()
diff = t1 - t0
print('Tempo de execucao: ' + str(diff.total_seconds()) + 'ms')
print('Frame opencv: ' + str(len(frame)))
#print('Resolucao: ' + str(frame.size) + 'px.')
cv2.imshow('Robo de telepresenca - v0.1', frame)
t6 = datetime.now()
diff = t6 - t5
print('Tempo total: ' + str(diff.total_seconds()) + 'ms')
cv2.waitKey(10)

cliente.close()
