
import sqlite3
from config import DB_PATH
from datetime import datetime


#This function is used to display the available options for ItemType and Location.
def display_options(cursor, table, id_col, name_col):
    cursor.execute(f"SELECT {id_col}, {name_col} FROM {table}")
    rows = cursor.fetchall()
    print(f"\nAvailable {table}:")
    for row in rows:
        print(f"{row[0]}: {row[1]}")
    return [row[0] for row in rows]


#This function is used to get valid input from the user. 
# It prompts the user with a message and checks if the input is in the list of valid IDs.
def get_valid_input(prompt, valid_ids):
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
def addLostItem(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    #Get status ID for "lost"
    cursor.execute("SELECT Status_ID FROM Status WHERE Status = 'Lost'")
    result = cursor.fetchone()
    if not result:
        print("Error: 'Lost' status not found in the database.")
        return
    lost_status_id = result[0]

    #Display and select ItemType
    item_type_ids = display_options(cursor, "ItemType", "Item_Type_ID", "Item_Category")
    item_type_id = get_valid_input("Enter the ItemType ID: ", item_type_ids)

    #Display and select Location
    location_ids = display_options(cursor, "Location", "Location_ID", "Building")
    location_id = get_valid_input("Enter the Location ID: ", location_ids)

    #Get other item details
    description = input("Enter item description: ")

    image_blob = None
    date_posted = datetime.now().strftime("%Y-%m-%d")

    #Insert the item
    cursor.execute("""
        INSERT INTO Item (Location_ID, Image, Description, Status_ID, User_ID, Item_Type_ID, Date_Posted)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (location_id, image_blob, description, lost_status_id, user_id, item_type_id, date_posted))

    conn.commit()
    print("Item successfully added.")
    conn.close()