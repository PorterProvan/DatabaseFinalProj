import sqlite3
import time
from config import DB_PATH
from createPost import addLostItem, claimItem

#DONT TOUCH DIS
userID = None
con = sqlite3.connect(DB_PATH)

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

def main():
    running = True
    while(running):
        print("** Welcome to the St. Thomas Lost and Found! **")
        print("1: To Login")
        print("2: To Quit")
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
                        cur = con.cursor()
                        cur.execute("INSERT OR IGNORE INTO User (email) VALUES (?)", (user,))
                        cur.execute("SELECT User_ID FROM User WHERE Email = ?", (user,))
                        userID = cur.fetchone()[0]
                        con.commit()
                        print("\nThank you: " + user + "\nWelcome to UST Lost and Found")
                        break
            while(loggedIn):
                while True:
                    try:
                        print("Would you like too:\n\t1: To add a new lost item\\n\t2: Claim Item\n\t3: View all posts\n\t4: Log out")
                        number = int(input("Enter a Command: "))
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid command integer.")
                if(number == 1):
                    addLostItem(userID, con) #this will prompt user to add item
                if(number == 2):
                    itemID = input("Enter the ID of the item you want to claim: ")
                    claimItem(itemID, con) #this will automatically update the status of the item to be claimed
                if(number == 3):
                    viewAllPosts()
                if(number == 4):
                    loggedIn = False
                    user = ""
                print(number)
    print("SessionEnded")

def updateLostItem():
    return False
def viewAllPosts():
    return False

main()
con.close()