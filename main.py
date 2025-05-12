import sqlite3
from config import DB_PATH
from otherFuncs import addLostItem, claimItem
from termcolor import colored
import time

#from datetime import datetime, timedelta

# DONT TOUCH DIS
userID = None
con = sqlite3.connect(DB_PATH)

cur = con.cursor()

# read the airline.sql DDL file 
with open("DatabaseSetupScript.sql", "r") as f:
    ddl = f.read()

cur.executescript(ddl)

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
con.commit()

def main():
    running = True
    while(running):

        while True:
            clear()
            # Show login menu
            print(colored("Welcome to the St. Thomas Lost and Found!", "magenta"))
            print()
            print("1: Login")
            print(colored("2: Quit", "red"))
            print()
            try:
                user_input = input("Option: ")
                value = int(user_input)
                break
            except ValueError:
                clear()
                print(colored("\n\nEnter a valid option please!\n\n", "red"))
                time.sleep(0.5)

        if (value == 2): 
            running = False
        elif (value == 1):
            NotLoggedIn = True
            while NotLoggedIn:
                    clear()
                    print(colored("Please enter your St. Thomas email.", "magenta"))
                    print()
                    email = input("Email: ").strip("").lower()
                    username = email.split("@")[0]
                    if len(username)!=8 or email.endswith("stthomas.edu") == False:
                        clear()
                        print(colored("\n\nPlease enter a valid UST Email!\n\n", "red"))
                        time.sleep(.5)
                    else:
                        clear()
                        cur = con.cursor()
                        cur.execute("INSERT OR IGNORE INTO User (email) VALUES (?)", (email,))
                        cur.execute("SELECT User_ID FROM User WHERE Email = ?", (email,))
                        userID = cur.fetchone()[0]
                        con.commit()

                        # Print "loading" screen
                        clear()
                        print(colored("Successfully logged in: ", "green") + email)
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
                            print("--------------------------------------")
                            print("---     LOST     AND     FOUND     ---")
                            print("--------------------------------------")
                            print()
                            print(colored("Would you like to do?", "magenta"))
                            print()
                            print( 
                            "1: Create a post for a lost item\n" + 
                            "2: Claim a lost item\n" +
                            "3: View all posts")
                            print(colored("4: Log out", "red"))
                            print()
                            number = int(input("Option: "))
                            break
                        except ValueError:
                            clear()
                            print(colored("\n\nEnter a valid option please!\n\n", "red"))
                            time.sleep(.5)

                ### Create a post for a lost item        
                if(number == 1):
                    addLostItem(userID, con) # This will prompt user to add item

                ### Claim item    
                elif(number == 2):
                    cur.execute("SELECT * FROM Item WHERE Status_ID = 1") # Select all items that are lost 
                    items = cur.fetchall()
                    zero_items = len(items) == 0
                    while True:
                        clear()
                        the_items = colored("Available items to claim:\n", "magenta")

                        # Print description of each item
                        if zero_items:
                            print(the_items)
                            print("No items posted!")
                            print()
                        else:
                            count = 1
                            the_items = the_items + "\n"
                            for item in items:
                                the_items = the_items + colored(str(count) + ": ", "magenta") + item[3] + "\n"
                                count += 1
                            print(the_items)
                        itemID = input("Enter the " + colored("item", "magenta") + " you would like to claim, or " + colored("Q", "red") + " to go back: ")
                        if itemID.lower() == "q" or zero_items:
                            clear()
                            print("\n\nReturning to main menu...\n\n")
                            time.sleep(0.5)
                            break
                        try:
                            itemID = int(itemID)
                            if itemID >= 1 and itemID <= len(items):
                                while True:
                                    clear()
                                    claim_input = input(f"Are you sure you'd like to claim item {itemID}? " + colored("Y", "green") + "/" + colored("N\n\n", "red"))
                                    if claim_input.lower() == "y":
                                        claimed_item_id = items[itemID-1][0]
                                        claimItem(claimed_item_id, con)
                                        clear()
                                        print(colored("\n\nItem successfully claimed.\n\n", "green"))
                                        time.sleep(0.5)
                                        break
                                    elif claim_input.lower() == "n":
                                        clear()
                                        print("\n\nReturning to main menu...\n\n")
                                        time.sleep(0.5)
                                        break
                                    else:
                                        clear()
                                        print(colored("\n\nEnter a valid option please!\n\n", "red"))
                                        time.sleep(0.5) 

                                break

                            else:
                                # User entered invalid int
                                clear()
                                print(colored("\n\nEnter a valid option please!\n\n", "red"))
                                time.sleep(0.5) 

                        except ValueError:
                            # User entered invalid string
                            clear()
                            print(colored("\n\nEnter a valid option please!\n\n", "red"))
                            time.sleep(0.5) 

                ### View all posts    
                elif(skip_to_posts or number == 3):
                    # Select all lost items
                    cur.execute("SELECT * FROM Item WHERE Status_ID = 1")
                    items = cur.fetchall()
                    

                    zero_items = len(items) == 0
                    clear()
                    print(colored("All posts:", "magenta"))
                    print()
                    

                    if zero_items:
                        print("No items posted!")
                    else:
                        # Print description of every current posted item
                        count = 1
                        for item in items:
                            print(colored(str(count) + ": ", "magenta") + item[3])
                            count += 1

                    # Ask user to pick an item to view more details about it
                    print()
                    item_num = input("Enter " + colored("Q", "red") + " to return to the main menu, or " + colored("enter an item number", "magenta") + " to view details: ")    

                    # Handle user going from all posts to main menu
                    if item_num.lower() == "q" or zero_items:
                        skip_to_posts = False
                        clear()
                        print("\n\nReturning to main menu...\n\n")
                        time.sleep(0.5)
                    else:

                        try:
                            while True:
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
                                # Show post details
                                print(colored("Details:", "magenta"))
                                print()
                                print(colored("Description: ", "magenta") + selected_item[3]+ "\n" +
                                    colored("Location found: ", "magenta") + item_location + "\n" +
                                    colored("Type: ", "magenta") + item_type + "\n" +
                                    colored("Date found: ", "magenta") + selected_item[7] + "\n" +
                                    colored("Posted by: ", "magenta") + item_user)
                                print()

                                # Prompt user to see comments
                                view_comment = input("Enter " + colored("C", "magenta") +" to view comments, or " + colored("Q", "red")+ " to go back: ")
                                if view_comment.lower() == "c":                        
                                    cur.execute("SELECT * FROM Comment WHERE Item_ID = ?", (selected_item[0],))
                                    comments_table = cur.fetchall()
                                    
                                    # Show comments
                                    print()
                                    print(colored("Comments:", "magenta"))
                                    print()

                                    count = 1
                                    if len(comments_table) != 0:
                                        for comment_row in comments_table:
                                            print(colored(f"{count}: ", "magenta") + comment_row[3])
                                            count += 1
                                    else:
                                        print("             No comments :(") 
                                        print("Do you know who's this is? Let them know!")
                                    
                                    # Handle comment
                                    print()
                                    make_comment = input("Enter " + colored("C", "green") + " to make comment / " + colored("Q", "red") + " to return to posts: ")
                                    if make_comment.lower() == "c":
                                        print()
                                        comment = input("Enter your comment: ")
                                        cur.execute("INSERT INTO Comment (User_ID, Item_ID, Comment) VALUES (?, ?, ?)", (userID, selected_item_id, comment))
                                        con.commit()

                                        clear()
                                        print(colored("\n\nComment successfully added on ", "green") + f"post {item_num}\n\n")
                                        skip_to_posts = True
                                        time.sleep(1)
                                        break
                                    else:
                                        skip_to_posts = True
                                        clear()
                                        print("\n\nReturning to posts...\n\n")
                                        time.sleep(0.5)
                                        break

                                # Handle user going from details to c posts
                                elif view_comment.lower() == "q":
                                    skip_to_posts = True
                                    clear()
                                    print("\n\nReturning to posts...\n\n")
                                    time.sleep(0.5)
                                    break
                                else:
                                    clear()
                                    print(colored("\n\nEnter a valid option please!\n\n", "red"))
                                    time.sleep(0.5) 

                        except ValueError:
                            skip_to_posts = True
                            clear()
                            print(colored("\n\nEnter a valid option please!\n\n", "red"))
                            time.sleep(0.5) 
                    
                ### Log out, end session
                elif (number == 4):
                    loggedIn = False
                    NotLoggedIn = True
                
                ### Handle invalid input on main menu
                else:
                    clear()
                    print(colored("\n\nEnter a valid option please!\n\n", "red"))
                    time.sleep(0.5)
        else:
            clear()
            print(colored("\n\nEnter a valid option please!\n\n", "red"))
            time.sleep(.5)
    clear()
    print("Goodbye!")

### Clears the terminal
def clear():
    print("\033c", end="")


main()
con.close()
