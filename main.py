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
cur.executemany("INSERT INTO Location VALUES (?, ?)", locations)


#need this stoof to actually update the database, this should be at the end of every insertion or update jazz

con.commit()

con.close()