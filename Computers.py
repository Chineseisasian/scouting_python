import pymysql
import mysql.connector as mariaDB
import statistics

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

cursor.execute("SELECT * FROM team195_scouting.Computers;")

def insertComputer(id, name, typeID, connectionStatus, stationID):
    CompID = id
    CompName = name
    CompTID = typeID
    CS = connectionStatus
    SID = stationID
    sql = "INSERT INTO Computers (ComputerID, ComputerName, ComputerTypeID, ConnectionStatus, StationID) VALUES (%i, %s, %i, %b, %i)"
    iden = (CompID, CompName, CompTID, CS, SID)

    cursor.execute(sql, iden)

    conn.commit()