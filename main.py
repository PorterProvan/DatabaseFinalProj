import sqlite3
from config import DB_PATH
from createPost import addLostItem, claimItem, updateDonated
from termcolor import colored
import time

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
    clear()
    while(running):
        # Show login menu
        print(colored("Welcome to the St. Thomas Lost and Found!", "magenta"))
        print()
        print("1: Login")
        print(colored("2: Quit", "red"))
        print()
        while True:
            try:
                user_input = input("Option: ")
                value = int(user_input)
                break
            except ValueError:
                print(colored("Enter a valid option please!", "red"))
                print()
        if(value == 2): running = False
        if(value == 1):
            clear()
            print(colored("Please enter your St. Thomas email.", "magenta"))
            NotLoggedIn = True
            while NotLoggedIn:
                    print()
                    email = input("Email: ")
                    email.strip
                    email.lower
                    username = email.split("@")[0]
                    if len(username)!=8 or email.endswith("stthomas.edu") == False:
                        print(colored("Please enter a valid UST Email.", "red"))
                    else:
                        clear()
                        cur = con.cursor()
                        cur.execute("INSERT OR IGNORE INTO User (email) VALUES (?)", (email,))
                        cur.execute("SELECT User_ID FROM User WHERE Email = ?", (email,))
                        userID = cur.fetchone()[0]
                        con.commit()
                        clear()
                        print(colored("Successfully logged in:", "green") + ": " + email)
                        print()
                        
                        print(colored("" +
                            "ooooo     ooo  .oooooo..o ooooooooooooo\n" +
                            "`888'     `8' d8P'    `Y8 8'   888   `8\n" +  
                            " 888       8  Y88bo.           888\n" +
                            ' 888       8   `"Y8888o.       888\n' +      
                            ' 888       8       `"Y88b      888\n'      
                            " `88.    .8'  oo     .d8P      888\n"      
                            "   `YbodP'    8oo88888P'      o888o", 
                        "magenta"))
                        print()
                        print(". ", end="")
                        time.sleep(0.5)
                        print(". ", end="")
                        time.sleep(0.5)
                        print(".", end="")
                        print()
                        print()
                        print()
                        time.sleep(0.5)
                        NotLoggedIn = False

            skip_to_posts = False
            loggedIn = True
            while(loggedIn):
                ### Main menu
                if not skip_to_posts:
                    while True:
                        try:
                            clear()
                            print(colored("" +
                                "ooooo     ooo  .oooooo..o ooooooooooooo\n" +
                                "`888'     `8' d8P'    `Y8 8'   888   `8\n" +  
                                " 888       8  Y88bo.           888\n" +
                                ' 888       8   `"Y8888o.       888\n' +      
                                ' 888       8       `"Y88b      888\n'      
                                " `88.    .8'  oo     .d8P      888\n"      
                                "   `YbodP'    8oo88888P'      o888o", 
                            "magenta"))
                            print()
                            print("---------------------------------------------------------")
                            print()
                            print(colored("Would you like to do?", "magenta"))
                            print()
                            print( 
                            "1: Create a post for a lost item\n" + 
                            "2: Claim a lost item item\n" +
                            "3: View all posts")
                            print(colored("4: Log out", "red"))
                            print()
                            number = int(input("Choose: "))
                            break
                        except ValueError:
                            print(colored("Enter a valid option please!", "red"))

                ### Create a post for a lost item        
                if(number == 1):
                    ### TODO: finish touching up this function
                    clear()
                    addLostItem(userID, con) # This will prompt user to add item

                ### Claim item    
                if(number == 2):
                    clear()
                    cur.execute("SELECT * FROM Item WHERE Status_ID = 1") # Select all items that are lost 
                    items = cur.fetchall()

                    # Print description of each item
                    count = 1
                    for item in items:
                        print(str(count) + ": " + item[3])
                        count += 1
                    itemID = input("Enter the ID of the item you want to claim: ")
                    claimItem(itemID, con)  # Updates the status of the item to be claimed

                ### View all posts    
                if(skip_to_posts or number == 3):
                    clear()
                    print(colored("All posts:", "magenta"))
                    print()
                    
                    # Select all lost items
                    cur.execute("SELECT * FROM Item WHERE Status_ID = 1")

                    # Print description of every current posted item
                    items = cur.fetchall()
                    count = 1
                    for item in items:
                        print(str(count) + ": " + item[3])
                        count += 1

                    # Ask user to pick an item to view more details about it
                    print()
                    item_num = input("Enter Q to return to the main menu, or choose an item to view details: ")
                    if item_num != "Q":
                        skip_to_posts = False

                        selected_item = items[int(item_num)-1]
                        selected_item_id = selected_item[0]
                        
                        # Show details
                        clear()

                        # Get post's item type
                        cur.execute("SELECT Item_Category FROM ItemType where Item_Type_ID = ?", (item[6],))
                        item_type = cur.fetchall()[0][0]
                        
                        # Get post's location
                        cur.execute("SELECT Building FROM Location WHERE Location_ID = ?", (selected_item[5],))
                        item_location = cur.fetchall()[0][0]
                        
                        # Get poster's email
                        cur.execute("SELECT Email FROM User WHERE User_ID = ?", (selected_item[1],))
                        item_user = cur.fetchall()[0][0]

                        print(colored(f"Details for the {item_type}:", "magenta"))
                        print()
                        print(colored("Description: ", "magenta") + selected_item[3]+ "\n" +
                            colored("Location found: ", "magenta") + item_location + "\n" +
                            colored("Type: ", "magenta") + item_type + "\n" +
                            colored("Date found: ", "magenta") + selected_item[7] + "\n" +
                            colored("Posted by: ", "magenta") + item_user)

                        # Prompt user to see comments
                        print()
                        view_comment = input("Enter C to view comments, or P to go back: ")
                        if view_comment.lower() == "c":                        
                            cur.execute("SELECT * FROM Comment WHERE Item_ID = ?", (selected_item[0],))
                            comments_table = cur.fetchall()
                            
                            # Show comments
                            print()
                            print(f"Comments from post {item_num}:")
                            print()

                            count = 1
                            for comment_row in comments_table:
                                print(f"{count}: " + comment_row[3])
                                count += 1
                            
                            # Handle comment
                            print()
                            make_comment = input("Make a comment? " + colored("Y", "green") + "/" + colored("N", "red") + ": ")
                            if make_comment.lower() == "y":
                                comment = input("Enter your comment: ")
                                cur.execute("INSERT INTO Comment (User_ID, Item_ID, Comment) VALUES (?, ?, ?)", (userID, selected_item_id, comment))
                                con.commit()
                            print()

                        # Handle user going from 
                        elif view_comment.lower() == "p":
                            skip_to_posts = True
                            print("Returning to posts...")
                            time.sleep(0.5)

                    elif item_num == "Q":
                        skip_to_posts = False
                        print("Returning to main menu")
                        time.sleep(0.5)
                    
                    else:
                        ## TODO: handle invalid option
                        print("Invalid option")
                        time.sleep(0.5)

                    
                ### Log out, end session
                if(number == 4):
                    loggedIn = False
                    print("Session ended.")
                    exit()
                print(number)
    print("Session ended.")

### Clears the terminal
def clear():
    print("\033c", end="")


main()
con.close()