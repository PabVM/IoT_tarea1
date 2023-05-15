from struct import unpack, pack
import json
import sqlite3 as sql
import traceback

createDatos = '''CREATE TABLE Datos (
    ID_device INTEGER PRIMARY KEY,
    MAC TEXT NOT NULL,
    Val INTEGER,
    Batt_level FLOAT,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Temp INTEGER,
    Press FLOAT,
    Hum INTEGER,
    Co FLOAT,
    RMS FLOAT,
    Amp_x FLOAT,
    Frec_x FLOAT,
    Amp_y FLOAT,
    Frec_y FLOAT,
    Amp_z FLOAT,
    Frec_z FLOAT,
    Acc_x FLOAT ARRAY,
    Acc_y FLOAT ARRAY,
    Acc_z FLOAT ARRAY
)'''

createLogs = '''CREATE TABLE Logs (
    ID_device INTEGER PRIMARY KEY,
    Status INTEGER,
    Protocol INTEGER,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)'''

createConfig = '''CREATE TABLE Config (
    Protocol INTEGER PRIMARY KEY DEFAULT 0,
    Status INTEGER DEFAULT 1
)'''

createLoss = '''CREATE TABLE Loss (
    Latency FLOAT,
    Packet_loss INT
)'''


def dataCreate():
    con = sql.connect("DB.sqlite")
    cur = con.cursor()
    cur.execute(createDatos)
    cur.execute(createLogs)
    cur.execute(createConfig)
    cur.execute(createLoss)
    con.close()

# funcion para guardar los headers del mensaje recibido
def dataSave(header,data):
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        saveDatos = '''INSERT INTO Datos (ID_device, MAC, Val, Batt_level, Timestamp, Temp, Press, Hum, Co, RMS, Amp_x, Frec_x, Amp_y, Frec_y, Amp_z, Frec_z, Acc_x, Acc_y, Acc_z) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cur.execute(saveDatos, (header["ID_device"], header["MAC"],json.dumps(data)))

def getConfig():
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        get_tlayer = '''SELECT Status, Protocol from Config'''
        status, protocol = cur.execute(get_tlayer)
        return status, protocol

def logSave(id_device, timestamp):
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        saveLogs = '''INSERT INTO Logs (ID_device, Status, Protocol, Timestamp) VALUES (?, ?, ?, ?)'''
        status, protocol = getConfig()
        cur.execute(saveLogs,(id_device, status, protocol, timestamp))

def configSave(status,protocol):
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        saveConfig = '''UPDATE Config SET (Status, Protocol) VALUES (?, ?)'''
        cur.execute(saveConfig,status,protocol)

def saveLoss(t_diff, p_loss):
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        lossSave = '''INSERT INTO Loss (Latency, Packet_loss) VALUES (?, ?)'''
        cur.execute(lossSave,(t_diff, p_loss))

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
    if dataD is not None:
        dataSave(header,dataD)
    return None if dataD is None else {**header, **dataD}