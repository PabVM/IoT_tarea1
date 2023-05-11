from struct import unpack, pack
import json
import sqlite3 as sql
import traceback

# funcion para guardar los headers del mensaje recibido
def dataSave(header,data):
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        cur.execute('''insert into Info (ID, MAC, Status, Protocol, Msg_len, data1) values (?,?,?,?,?,?)''', (header["ID"], header["MAC"], header["status"], header["protocol"], header["msg_len"],data))

# genera un OK para responder y da la posibilidad de cambiar el status/protocol
# el status deberia ser UDP/TCP y el protocolo al tipo de mensaje(?)
def response(change:bool=False, status:int=255, protocol:int=255):
    OK = 1
    CHANGE = 1 if change else 0
    return pack("<BBBB", OK, CHANGE, status, protocol)

# desempaqueta un byte array con los datos de un mensaje (sin el header)
def protUnpack(protocol:int, data):
    protocol_unpack = ["<B", "<B1", "<B1BfBf"]
    return unpack(protocol_unpack[protocol], data)

# transforma el byte array de datos en un diccionario con los datos del mensaje
def dataDict(protocol:int, data):
    if protocol not in [0, 1, 2, 3, 4, 5]:
        print("Error: protocol does not exist")
        return None
    def protFunc(protocol, keys):
        def p(data):
            unp = protUnpack(protocol, data)
            return {key:val for (key,val) in zip(keys, unp)}
        return p
    p0 = ["OK"]
    p1 = ["Batt_level", "Timestamp"]
    p2 = ["Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co"]
    p3 = ["Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS"]
    p4 = ["Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS", "Amp_x", "Frec_x", "Amp_y", "Frec_y", "Amp_z", "Frec_z"]
    p5 = ["Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "Acc_x", "Acc_y", "Acc_z"]

    p = [p0, p1, p2, p3, p4, p5]

    try:
        return protFunc(protocol, p[protocol])(data)
    except Exception:
        print("Data unpacking Error: ", traceback.format_exc())
        return None
    
def headerDict(data):
    ID, M1, M2, M3, M4, M5, M6, protocol, status, msg_len = unpack("<6B2BH", data)
    MAC = ".".join([hex(x)[2:] for x in [M1, M2, M3, M4, M5, M6]])
    return {"ID": ID, "MAC": MAC, "protocol": protocol, "status": status, "msg_len": msg_len}
    
def parseData(packet):
    header = packet[:12]
    data = packet[12:]
    header = headerDict(header)
    dataD = dataDict(header["protocol"],data)
    if dataD is None:
        dataSave(header,dataD)
    return None if dataD is None else {**header, **dataD}