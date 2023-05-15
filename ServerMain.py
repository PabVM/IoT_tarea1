import socket
import Desempaquetamiento as dpack
import sqlite3 as sql
from datetime import datetime as dt

# Primero vamo a crear la base de datos
dpack.dataCreate()
print("Base de datos creada")

def timestamp_diff(t):
    current_time = dt.now()
    td = t - current_time.timestamp()
    return td

def bytes_loss(data_len, packet):
    data = packet[12:]
    return data_len - len(data)

def save_log(packet):
    header = packet[:12]
    header_dict = dpack.headerDict(header)
    dpack.logSave(header_dict["ID"],dt.now())

def save_loss(pack_dict, packet):
    timestamp = pack_dict["header"]["Timestamp"]
    t_diff = timestamp_diff(timestamp)

    data_length = pack_dict["header"]["msg_len"]
    loss = bytes_loss(data_length, packet)
    dpack.saveLoss(t_diff, loss)

# Recibe un socket
def TCP_frag_recv(conn):
    doc = b''
    while True:
        try:
            conn.settimeout(5)
            data = conn.recv(1024)
            if data == b'\0':
                break
            else:
                doc += data
        except TimeoutError:
            conn.send(b'\0')
            raise
        except Exception:
            conn.send(b'\0')
            raise
        conn.send(b'\1')
    return doc

def UDP_frag_recv(s):
    doc = b''
    addr = None
    while True:
        try:
            data, addr = s.recvfrom(1024)
            if data == b'\0':
                break
            else:
                doc += data
        except TimeoutError:
            raise
        except Exception:
            raise
    return (doc,addr)
    

HOST = "192.168.28.1"
PORT = 5010

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)
print(f'Listening in {HOST}:{PORT}')

"""
Lo que hay que hacer es:

- Recibir la consulta de la ESP32 por el tipo de conexión
- Establecer la conexión que se indique desde la base de datos 
- Recibir los datos desde esa conexión (habría que crear un socket nuevo)
- Guardar los datos en la BBDD

-> se pueden hacer funciones auxiliares para la creación de los sockets UDP y TCP(?)

"""
while True:
    # Esta debería ser la primera conexion con la ESP32
    # asi que solo deberia enviarle los datos del tipo de conexion
    conn, addr = s.accept()
    print(f'Conexion establecida con ({addr[0]}:{addr[1]})')
    while True:
        try:
            msg = conn.recv(1024)
            if msg == b'':
                break;
            # Hay que guardar el log. Para eso extraemos el header del mensaje
            save_log(msg)
        except ConnectionResetError:
            break
        print(f'Recibido {msg}')
        # aqui debo obtener Status y Protocol de la base de datos y enviarlos
        status, protocol = dpack.getConfig()
        response = dpack.response(status=status,protocol=protocol)
        conn.send(response,addr)
    # Aca tengo que revisar el dato de status
    if status == 0: # la conexion es UDP
        UDP_IP = '192.168.5.177'
        UDP_PORT = 5010
        sUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sUDP.bind((UDP_IP, UDP_PORT))
        print(f'Esperando datagramas UDP en {UDP_IP}:{UDP_PORT}')
        while True:
            payload, client_address = UDP_frag_recv(sUDP)
            # Se guarda el log
            save_log(payload)
            # Aqui tengo que ir guardando la data en la base de datos
            # Primero parseamos
            msg_dict = dpack.parseData(payload)
            print(f'Datos recibidos: {msg_dict}')
            # Registramos por si hay perdida
            save_loss(msg_dict, msg)
            current_status = msg_dict["header"]["Status"]
            # Vemos si se cambia el status para hacer el update y cerrar la conexion
            if current_status != status:
                current_protocol = msg_dict["header"]["Protocol"]
                dpack.configSave(current_status, current_protocol)
                break
    else:
        data = TCP_frag_recv(conn)
        data_dict = dpack.parseData(data)
        # Registramos por si hay perdida
        save_loss(data_dict,data)
        print(f'Datos recibidos: {data_dict}')
    conn.close()
