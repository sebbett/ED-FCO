import sqlite3

def RegisterCarrier(id, name, owner, cmdr):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM carriers WHERE id=\"{id}\";")
    id_rows = len(cursor.fetchall())
    cursor.execute(f"SELECT * FROM carriers WHERE owner=\"{owner}\";")
    owner_rows = len(cursor.fetchall())
    
    if id_rows == 0:
        if owner_rows == 0:
            cursor.execute(f"INSERT INTO carriers (id, name, owner, cmdr) VALUES (\"{id}\",\"{name}\",\"{owner}\",\"{cmdr.upper()}\");")
            conn.commit()
            cursor.close()
            conn.close()
            return 200
        else:
            conn.commit()
            cursor.close()
            conn.close()
            return 401
    else:
        conn.commit()
        cursor.close()
        conn.close()
        return 402

def UnregisterCarrier(id, owner):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM carriers WHERE id=\"{id}\" AND owner=\"{owner}\";")
    rows = len(cursor.fetchall())
    if rows > 0:
        cursor.execute(f"DELETE FROM carriers WHERE id=\"{id}\" AND owner=\"{owner}\";")
        conn.commit()
        cursor.close()
        conn.close()
        return 200 #Succesfully unregistered
    else:
        cursor.close()
        conn.close()
        return 401 #Carrier not registered or not registered to user

def Subscribe(id, channel):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM subscriptions WHERE channel=\"{channel}\" LIMIT 1000;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        if row[1] == id:
            return 401 #Subscription between id and channel exists

    cursor.execute(f"INSERT INTO subscriptions (id, channel) VALUES (\"{id}\",\"{channel}\");")
    conn.commit()
    cursor.close()
    conn.close()
    return 200

def Unsubscribe(id, channel):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM subscriptions WHERE id=\"{id}\" AND channel=\"{channel}\";")
    conn.commit()
    cursor.close()
    conn.close()
    return 200

def UnsubscribeAll(channel):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM subscriptions WHERE channel=\"{channel}\";")
    conn.commit()
    cursor.close()
    conn.close()
    return 200

def GetCarrier(owner):
    id = ""
    name = ""
    cmdr = ""
    subs = list()
    
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM carriers WHERE owner=\"{owner}\";")
    rows = cursor.fetchall()
    if len(rows) > 0:
        
        data = rows[0]
        id = data[1]
        name = data[2]
        owner = data[3]
        cmdr = data[4]

        cursor.execute(f"SELECT * FROM subscriptions WHERE id=\"{id}\" LIMIT 1000;")
        subs_data = cursor.fetchall()
        cursor.close()
        conn.close()
        for s in subs_data:
            subs.append(s[2])
        return CarrierInfo.createData(id, name, owner, cmdr, subs)
    else:
        return 

def GetSubscriptions(channel):
    subs = list()
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM subscriptions WHERE channel=\"{channel}\";")
    rows = cursor.fetchall()

    for r in rows:
        id = r[1]
        cursor.execute(f"SELECT * FROM carriers WHERE id=\"{id}\";")
        name = cursor.fetchone()[2]
        subs.append(SubInfo.createData(id, name))


    return subs

def GetCarrierName(id):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM carriers WHERE id=\"{id}\" LIMIT 1;")
    response = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(response) > 0:
        return response[0][0]
    else:
        return None

def GetCarrierID(owner):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM carriers WHERE owner=\"{owner}\" LIMIT 1;")
    response = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(response) > 0:
        return response[0][0]
    else:
        return None

def GetCarrierName(owner):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM carriers WHERE owner=\"{owner}\" LIMIT 1;")
    response = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(response) > 0:
        return response[0][0]
    else:
        return None

def GetCarrierServices(id):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM services WHERE id=\"{id}\" LIMIT 1;")
    response = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(response) > 0:
        r = response[0]
        flags = list()
        for i in r:
            flags.append(i)

        return flags
    else:
        return None

def SetCarrierStatus(id, loc, obj, res):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM status_updates WHERE id=\"{id}\" LIMIT 1;")
    response = cursor.fetchall()
    if len(response) > 0:
        cursor.execute(f"UPDATE status_updates SET location=\"{loc}\", objective=\"{obj}\", reserves=\"{res}\" WHERE id=\"{id}\";")
        cursor.close()
        conn.commit()
        conn.close()
    else:
        cursor.execute(f"INSERT INTO status_updates (id, location, objective, reserves) VALUES (\"{id}\",\"{loc}\",\"{obj}\",\"{res}\");")
        cursor.close()
        conn.commit()
        conn.close()

class CarrierInfo:
    def __init__(self, id, name, owner, cmdr, subs):
        self.id = id
        self.name = name
        self.owner = owner
        self.cmdr = cmdr
        self.subs = subs
    
    @classmethod
    def createData(cls, id, name, owner, cmdr, subs):
        return cls(id, name, owner, cmdr, subs)

class SubInfo:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def createData(cls, id, name):
        return cls(id, name)
    

        