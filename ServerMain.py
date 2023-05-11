import socket

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

HOST = "192.168.100.31"
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)
print(f'Listening in {HOST}:{PORT}')

"""
Lo que hay que hacer es:

- Recibir la consulta de la ESP32 por el tipo de conexión
- Establecer la conexión que se indique desde la base de datos
AQUI SE SUPONE QUE LA ESP32 ES LA QUE SABE QUÉ TIPO DE CONEXIÓN HAY QUE ESTABLECER  
- Recibir los datos desde esa conexión (habría que crear un socket nuevo)
- Guardar los datos en la BBDD

-> se pueden hacer funciones auxiliares para la creación de los sockets UDP y TCP(?)

"""
while True:
    # Esta debería ser la primera conexion con la ESP32
    # asi que solo deberia enviarle los datos del tipo de conexion
    conn, addr = s.accept()
    print(f'Conexion establecida con ({addr[0]}:{addr[1]})')
    

