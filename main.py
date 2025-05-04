import sqlite3

#DONT TOUCH DIS

con = sqlite3.connect("DataBaseFinalProj.db")

cur = con.cursor()

# read the airline.sql DDL file 
with open("DatabaseSetupScript.sql", "r") as f:
    ddl = f.read()

# execute the DDL file
# executescript can run multiple SQL statements at once
cur.executescript(ddl)

#TIL HERE NOTHING SHOULD HAVE BEEN TOCUHED :)

comments = [
    ('1', '1', '1', 'I can see the test post')
]
cur.executemany("INSERT OR IGNORE INTO Comment VALUES (?, ?, ?, ?)", comments)

locations = [
    ('1', 'Schoenecker Hall'),
    ('2', 'Ireland'),
    ('3', 'Dowling'),
    ('4', 'Frey Hall'),
    ('5', 'Flynn Hall'),
    ('6', 'Morrison Hall'),
    ('7', 'Brady Hall'),
    ('8', 'OEC'),
    ('9', 'AARC'),
    ('10', 'ASC'),
    ('11', 'JRC'),
    ('12', 'Library'),
    ('13', 'MHC'),
    ('14', 'OSS'),
    ('15', 'Brady Education Center'),
    ('16', 'FDC'),
    ('17', 'SCC'),
    ('18', 'OPUS'),
    ('19', 'Center of Well Being'),
    ('20', 'Grace Hall'),
    ('21', 'OWS')
]
cur.executemany("INSERT OR IGNORE INTO Location VALUES (?, ?)", locations)

status = [
    ('1', 'Lost'),
    ('2', 'Found'),
    ('3', 'Donated'),
]
cur.executemany("INSERT OR IGNORE INTO Status VALUES (?, ?)", status)

itemType = [
    ('1', 'Clothing/Shoes'),
    ('2', 'Electronics'),
    ('3', 'St. Thomas ID'),
    ('4', 'Wallet'),
    ('5', 'Purse'),
    ('6', 'Backpack'),
    ('7', 'Water Bottle'),
    ('8', 'Keys'),
    ('9', 'Other')
]
cur.executemany("INSERT OR IGNORE INTO ItemType VALUES (?, ?)", itemType)

users = [
    ('1', 'Harrison@gmail.com'),
    ('2', 'Porter@gmail.com'),
    ('3', 'Josh@gmail.com')
]
cur.executemany("INSERT OR IGNORE INTO User VALUES (?, ?)", users)

Items = [
    ('1', '1', 'NULL', 'This is the Test Item', '2', '1', '9', '2025-05-04')
]
cur.executemany("INSERT OR IGNORE INTO Item VALUES (?, ?, ?, ?, ?, ?, ?, ?)", Items)

# need this stoof to actually update the database, this should be at the end of every insertion or update jazz
con.commit()
con.close()
