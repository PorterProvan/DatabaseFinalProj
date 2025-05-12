import sqlite3
from config import DB_PATH
from datetime import datetime, timedelta
from termcolor import colored
import time

NUM_CATEGORIES = 9
NUM_LOCATIONS = 21

#This function is used to display the available options for ItemType and Location.
def displayOptions(cursor, table, id_col, name_col):
    cursor.execute(f"SELECT {id_col}, {name_col} FROM {table}")
    rows = cursor.fetchall()
    for row in rows:
        print(colored(f"{row[0]}: ", "magenta") + f"{row[1]}")
    return [row[0] for row in rows]


#This function is used to get valid input from the user. 
# It prompts the user with a message and checks if the input is in the list of valid IDs.
def getValidInput(prompt, valid_ids):
    while True:
        try:
            value = int(input(prompt))
            if value in valid_ids:
                return value
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a number.")

#
#This function is used to add a lost item to the database. It requires only the user_id to be passed to it.
#The function automatically fetches the status ID for "lost" and prompts the user to select the item type and location from the database.
#The helper functions display_options and get_valid_input are used to display the available options and validate user input.
#
def addLostItem(user_id, conn):
    cursor = conn.cursor()
    #Get status ID for "lost"
    cursor.execute("SELECT Status_ID FROM Status WHERE Status = 'Lost'")
    result = cursor.fetchone()
    if not result:
        print("Error: 'Lost' status not found in the database.")
        return
    lost_status_id = result[0]

    cursor.execute("SELECT * FROM ItemType")
    category = cursor.fetchone()

    #Display and select ItemType
    while True:
        clear()
        print(colored("What category does the item fall under?", "magenta"))
        print()
        displayOptions(cursor, "ItemType", "Item_Type_ID", "Item_Category")
        print()
        item_type_id = input("Choose a category, or enter " + colored("Q", "red")+ " to " + colored("cancel the post", "red") + ": ")
        if item_type_id.lower() == "q":
            ### return to posts
            clear()
            print("\n\nPost cancelled")
            print("\nReturning to main menu...\n\n")
            time.sleep(1)
            return
        else:
            ### HANDLE ERROR
            try:
                item_type_id = int(item_type_id)
                if item_type_id >= 1 and item_type_id <= NUM_CATEGORIES:
                    # User entered valid value, continue
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


    #Display and select Location
    while True:
        clear()
        print(colored("Where did you find it?", "magenta"))
        print()
        displayOptions(cursor, "Location", "Location_ID", "Building")
        print()
        location_id = input("Choose a location, or enter " + colored("Q", "red")+ " to " + colored("cancel the post", "red") + ": ")
        if location_id.lower() == "q":
            ### return to posts
            clear()
            print("\n\nPost cancelled")
            print("\nReturning to main menu...\n\n")
            time.sleep(0.5)
            return
        else:
            try:
                location_id = int(location_id)
                if location_id >= 1 and location_id <= NUM_LOCATIONS:
                    # User entered valid value, continue
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
    
    #Get other item details
    clear()
    print("Enter a " + colored("description", "magenta") + " of the item. Describe briefly what it looks like, where you found it, etc. ")
    print()
    description = input(" -- ")

    ### Not possible in terminal
    image = None

    # Check with user if correct data
    cursor.execute("SElECT * FROM ItemType WHERE Item_Type_ID = ?", (item_type_id,))
    item_type_name = cursor.fetchone()[1]
    cursor.execute("SElECT * FROM Location WHERE Location_ID = ?", (location_id,))
    location_name = cursor.fetchone()[1]
    while True:
        clear()
        print(colored("Category: ", "magenta") + item_type_name)
        print(colored("Location: ", "magenta") + location_name)
        print(colored("Description: ", "magenta") + description)
        print()
        user_choice = input("Confirm post? " + colored("Y", "green") + "/" + colored("N", "red") + ": ")
        if user_choice.lower() == "y":
            clear()
            print(colored("\n\nPosted successfully!\n\n", "green"))
            time.sleep(1)
            break
        elif user_choice.lower() == "n":
            clear()
            print("\n\nYour post has been cancelled.\n\n")
            time.sleep(1)
            return
        else:
            clear()
            print(colored("\n\nEnter a valid option please!\n\n", "red"))
            time.sleep(0.5)


    # Record date
    date_posted = datetime.now().strftime("%Y-%m-%d")

    #Insert the item
    cursor.execute("""
        INSERT INTO Item (Location_ID, Image, Description, Status_ID, User_ID, Item_Type_ID, Date_Posted)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (location_id, image, description, lost_status_id, user_id, item_type_id, date_posted))

    conn.commit()
    print("Item successfully added.")

# This function is used to claim an item as found. It requires the item_id to be passed to it.
# The function fetches the status ID for "found" and updates the item's status in the database.
# It also checks if the item exists in the database and prints a message accordingly.
def claimItem(item_id, conn):
    cursor = conn.cursor()

    #get the Status_ID for "found"
    cursor.execute("SELECT Status_ID FROM Status WHERE Status = 'Found'")
    result = cursor.fetchone()

    if not result:
        print("Error: 'Found' status not found in the database.")
        conn.close()
        return
    
    found_status_id = result[0]

    #update the item to set its status to "found"
    cursor.execute("""
        UPDATE Item
        SET Status_ID = ?
        WHERE Item_ID = ?
    """, (found_status_id, item_id))

    #commit the change and close the connection
    conn.commit()
    
#This function is used to update the status of items that have been posted for more than 2 weeks to "Donated".
def updateDonated(conn):
    cursor = conn.cursor()

    #get the Status_ID for "Donated"
    cursor.execute("SELECT Status_ID FROM Status WHERE Status = 'Donated'")
    result = cursor.fetchone()
    
    if not result:
        print("Error: 'Donated' status not found in the database.")
        return
    
    donated_status_id = result[0]

    #get the date 2 weeks ago
    two_weeks_ago = (datetime.now() - timedelta(weeks=2)).strftime("%Y-%m-%d")

    #update items posted more than 2 weeks ago
    cursor.execute("""
        UPDATE Item
        SET Status_ID = ?
        WHERE Date(Date_Posted) < Date(?)
    """, (donated_status_id, two_weeks_ago))

    conn.commit()

    if cursor.rowcount > 0:
        print(f"Successfully updated {cursor.rowcount} items to 'Donated'.")
    else:
        print("No items found that were posted more than 2 weeks ago.")

### Clears the terminal
def clear():
    print("\033c", end="")