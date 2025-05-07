import sqlite3
import time

#DONT TOUCH DIS

con = sqlite3.connect("DataBaseFinalProj.db")

cur = con.cursor()

# read the airline.sql DDL file 
with open(r"C:\Users\josh4\OneDrive - University of St. Thomas\Spring 2025\CISC 450\DatabaseFinalProj\DatabaseSetupScript.sql", "r") as f:
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

def main():
    running = True
    while(running):
        print("** Welcome to the St. Thomas Lost and Found! **")
        print("To Login: 1")
        print("To Quit: 2")
        while True:
            try:
                user_input = input("Please enter a Command: ")
                # Attempt to convert the input to the desired type (e.g., integer)
                value = int(user_input)
                # If the conversion is successful, the input is valid, exit the loop
                break
            except ValueError:
                print("Please enter a valid Command.")
        # Use the validated value
        if(value == 2): running = False
        if(value == 1):
            print("Please enter your St. Thomas email.")
            while True:
                    user = input("Email: ")
                    user.strip
                    user.lower
                    if(user.endswith("stthomas.edu") == False):
                        print("Invalid input. Please enter a valid UST Email.")
                    else:
                        loggedIn = True
                        print("\nThank you: " + user + "\nWelcome to UST Lost and Found")
                        break
            while(loggedIn):
                while True:
                    try:
                        print("Would you like too:\n\tTo add a new lost item: 1\n\tUpdate lost item: 2\n\tRemove Post: 3\n\tView all posts: 4\n\tLog out: 5")
                        number = int(input("Enter a Command: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid command integer.")
                if(number == 1):
                    addLostItem()
                if(number == 2):
                    updateLostItem()
                if(number == 3):
                    removePost()
                if(number == 4):
                    viewAllPosts()
                if(number == 5):
                    print("EASY")
                    loggedIn = False
                    user = ""
                print(number)
    print("SessionEnded")

def addLostItem():
    return False
def updateLostItem():
    return False
def removePost():
    return False
def viewAllPosts():
    return False

main()