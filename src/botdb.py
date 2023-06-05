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

def GetCarrierByID(id):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM carriers WHERE id=\"{id}\" LIMIT 1;")
    r = cursor.fetchall()
    if len(r) > 0:
        name = r[0][2]
        owner = r[0][3]
        cmdr = r[0][4]
        subs = GetSubscriptionsToCarrier(id)
        status = GetCarrierStatus(id)
        vanity = r[0][5]

        cursor.execute
        r = cursor.fetchall()
        return CarrierInfo.createData(id, name, owner, cmdr, subs, status, vanity)
    else:
        return None

def GetCarrierByDiscord(discord):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM carriers WHERE owner=\"{discord}\" LIMIT 1;")
    r = cursor.fetchall()
    if len(r) > 0:
        id = r[0][1]
        name = r[0][2]
        owner = r[0][3]
        cmdr = r[0][4]
        subs = GetSubscriptionsToCarrier(id)
        status = GetCarrierStatus(id)
        vanity = r[0][5]

        cursor.execute
        r = cursor.fetchall()
        return CarrierInfo.createData(id, name, owner, cmdr, subs, status, vanity)
    else:
        return None

def UpdateCarrierVanity(id, url):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE carriers SET vanity=\"{url}\" WHERE id=\"{id}\";")
    conn.commit()
    cursor.close()
    conn.close()

def GetSubscriptionsToCarrier(id):
    subs = list()
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM subscriptions WHERE id=\"{id}\";")
    rows = cursor.fetchall()

    for r in rows:
        subs.append(r[2])

    return subs

def GetSubscriptionsToChannel(channel):
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

def GetCarrierStatus(id):
    conn = sqlite3.connect("carriers.db")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM status_updates WHERE id=\"{id}\" LIMIT 1;")
    response = cursor.fetchall()
    if len(response) > 0:
        return StatusInfo.createData(response[0][2], response[0][3], response[0][4])
    else:
        return None

class CarrierInfo:
    def __init__(self, id, name, owner, cmdr, subs, status, vanity):
        self.id = id
        self.name = name
        self.owner = owner
        self.cmdr = cmdr
        self.subs = subs
        self.status = status
        self.vanity = vanity
    
    @classmethod
    def createData(cls, id, name, owner, cmdr, subs, status, vanity):
        return cls(id, name, owner, cmdr, subs, status, vanity)

class SubInfo:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def createData(cls, id, name):
        return cls(id, name)

class StatusInfo:
    def __init__(self, loc, obj, res):
        self.location = loc
        self.objective = obj
        self.reserves = res
    
    @classmethod
    def createData(cls, loc, obj, res):
        return cls(loc, obj, res)

        