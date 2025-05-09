import sqlite3
import time
from config import DB_PATH
from createPost import addLostItem, claimItem, updateDonated

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
    ('2', '1', '1', 'This is the secon dcomment')
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
    updateDonated(con)
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
                        print("Would you like too:\n" + 
                        "1: To add a new lost item\n" + 
                        "2: Claim Item\n" +
                        "3: View all posts\n" +
                        "4: Log out")
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
                    print("All posts:")
                    cur.execute("SELECT * FROM Item WHERE Status_ID = 1")
                    items = cur.fetchall()
                    # Print description of each item
                    count = 1
                    for item in items:
                        print(str(count) + ": " + item[3])
                        count += 1
            
                    item_num = input("Enter an item number to view details: ")
                    selected_item = items[int(item_num)-1]
                    selected_item_id = selected_item[0]
                    
                    print()
                    print(f"Details for {item[3]}:")
                    cur.execute("SELECT Building FROM Location WHERE Location_ID = ?", (selected_item[5],))
                    item_location = cur.fetchall()[0][0]
                    
                    cur.execute("SELECT Email FROM User WHERE User_ID = ?", (selected_item[1],))
                    item_user = cur.fetchall()[0][0]

                    print()
                    print("Location found: " + item_location + "\n" +
                          "Date found: " + selected_item[7] + "\n" +
                          "Posted by: " + item_user)

                    print()
                    view_comment = input("View comments? Y/N: ")
                    if view_comment.lower() == "y":                        
                        cur.execute("SELECT * FROM Comment WHERE Item_ID = ?", (selected_item[0],))
                        comments_table = cur.fetchall()
                        
                        print()
                        print(f"Comments from post {item_num}:")
                        print()

                        count = 1
                        for comment_row in comments_table:
                            print(f"{count}: " + comment_row[3])
                            count += 1
                        
                        print()
                        make_comment = input("Make comment? Y/N: ")
                        if make_comment.lower() == "y":
                            comment = input("Enter your comment: ")
                            cur.execute("INSERT INTO Comment (User_ID, Item_ID, Comment) VALUES (?, ?, ?)", (userID, selected_item_id, comment))
                            con.commit()
                        print()
                    

                if(number == 4):
                    loggedIn = False
                    user = ""
                    print("SessionEnded")
                    exit()
                print(number)
    print("SessionEnded")

def updateLostItem():
    return False
def viewAllPosts():

    return False

main()
con.close()