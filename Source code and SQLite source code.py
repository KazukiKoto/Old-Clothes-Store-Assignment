import sqlite3
import tkinter
import numpy
import qrcode
import cv2


######################################################################## SQLite

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@# Inventory
def Establish_Inventory():
    try: #Creating initial inventory table
        Connection = sqlite3.connect("Inventory.db") #Establish a connection
        Cursor = Connection.cursor() #Creates cursor for database
        Inventory_Create=''' CREATE TABLE IF NOT EXISTS INVENTORY (
            Item_ID integer PRIMARY KEY,
            Item_Name text,
            Item_Type text,
            Item_Quantity integer,
            Item_Price real,
            Item_Offer_Price real,
            Item_Colour text
        )'''
        #^^^ Creates Inventory table, does not populate table with records.
        Cursor.execute(Inventory_Create) #Executes
        Connection.commit() #Saves changes
    except sqlite3.Error as Error:
        print("Error ",error)

    try: #Inserting all initial items into inventory
        Inventory_Insert_1=''' INSERT INTO INVENTORY (Item_ID, Item_Name, Item_Type, Item_Quantity, Item_Price, Item_Offer_Price, Item_Colour) VALUES (0001, "ASOS_4505_icon_training_t-shirt_with_quick_dry_in_black", "T-SHIRT", 1000, 12.00, 0.0, "BLACK")
        '''
        Inventory_Insert_2=''' INSERT INTO INVENTORY (Item_ID, Item_Name, Item_Type, Item_Quantity, Item_Price, Item_Offer_Price, Item_Colour) VALUES (0002, "ASOS_DESIGN_slim_jeans_in_washed_black", "JEANS", 1000, 25.00, 0.0, "BLACK")
        '''
        Inventory_Insert_3=''' INSERT INTO INVENTORY (Item_ID, Item_Name, Item_Type, Item_Quantity, Item_Price, Item_Offer_Price, Item_Colour) VALUES (0003, "ASOS_DESIGN_driving_shoes_in_grey_suede_with_lace_detail", "SHOES", 1000, 40.00, 0.53, "GREY")
        '''
        Inventory_Insert_4=''' INSERT INTO INVENTORY (Item_ID, Item_Name, Item_Type, Item_Quantity, Item_Price, Item_Offer_Price, Item_Colour) VALUES (0004, "ASOS_DESIGN_formal_skinny_fit_oxford_shirt_with_double_cuff_in_white", "SHIRT", 1000, 28.00, 0.14, "WHITE")
        '''
        Inventory_Insert_5=''' INSERT INTO INVENTORY (Item_ID, Item_Name, Item_Type, Item_Quantity, Item_Price, Item_Offer_Price, Item_Colour) VALUES (0005, "ASOS_DESIGN_Arabelle_chain_trim_hiker_boots_in_black", "BOOTS", 1000, 38.00, 0.63, "BLACK")
        '''
        Inventory_Insert_6=''' INSERT INTO INVENTORY (Item_ID, Item_Name, Item_Type, Item_Quantity, Item_Price, Item_Offer_Price, Item_Colour) VALUES (0006, "ASOS_DESIGN_faux_fur_bucket_hat_in_black", "HAT", 1000, 15.00, 0.13, "BLACK")
        '''
        #^^^Adding each record individually for initial startup
        Cursor.execute(Inventory_Insert_1)#executing each record addition.
        Cursor.execute(Inventory_Insert_2)
        Cursor.execute(Inventory_Insert_3)
        Cursor.execute(Inventory_Insert_4)
        Cursor.execute(Inventory_Insert_5)
        Cursor.execute(Inventory_Insert_6)
        Connection.commit() #Saves changes
    except sqlite3.Error as error:
        print("Records already exist")
    finally:
        Connection.close() #Close connection
        
class Label_:
    def __init__(self, number,Basket_Array): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        Basket_Label_ = tkinter.Label(basket_view_page, text = Basket_Array[number]) # Creates the Label
        Basket_Label_.grid(row=(1+number), column=0) # Places Label in grid, uses number to find correct row.
    
class Button_:
    def __init__(self, number,Basket_Array): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        Basket_Button_ = tkinter.Button(basket_view_page, text = "Delete", command = lambda:[(Basket_Array.pop(number)), basket_view_page.destroy(), Delete_Basket_Item(Basket_Array)]) #Button creation
        #^^^ Button pops the corresponding item from the array and deletes the current UI and makes a new one.
        Basket_Button_.grid(row=(1+number), column=3) # Places Button in grid
        
class Inventory_Label:
    def __init__(self, number, Inventory_All): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        Inventory_Label_ = tkinter.Label(customer_main_page, text = Inventory_All[number]) # Creates the Label
        Inventory_Label_.grid(row=(3+number), column=0) # Places Label in grid, uses number to find correct row.
    
class Inventory_Button:
    def __init__(self, number, Inventory_All): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        try:
            Connection = sqlite3.connect("Inventory.db") #Establishes a connection
            Cursor = Connection.cursor() #Creates a cursor
            Inventory_View = ''' SELECT * FROM INVENTORY WHERE Item_Name = ?
            '''
            #^^^Searchs for item name in database
            Cursor.execute(Inventory_View, Inventory_All[number]) #Executes the search with name on same row
            Item_Desc = Cursor.fetchall() #Retrieves results from search
        except sqlite3.Error as error:
            print("Error",error)
        finally:
            Connection.close() #Terminates connection
        Inventory_Button_ = tkinter.Button(customer_main_page, text = "Go", command = lambda:[customer_main_page.destroy(), SEARCH_RESULT_UI(Item_Desc)]) #Button creation
        #^^^ Button Searches for the corresponding item
        Inventory_Button_.grid(row=(3+number), column=3) # Places Button in grid
    
class Name_Label:
    def __init__(self, number, Item_ID): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        try:
            Connection = sqlite3.connect("Inventory.db") #Establishes a connection
            Cursor = Connection.cursor() #Creates a cursor
            Name_Grab = ''' SELECT Item_Name FROM INVENTORY WHERE Item_ID = ?
            '''
            #^^^Gets the name of the item with a certain ID
            Cursor.execute(Name_Grab, Item_ID[number]) #Executes the search
            Item_Desc = numpy.array(Cursor.fetchall()) #Retrieves results from search
            Item_Name = REMOVE_CHARACTERS_1(str(Item_Desc)) #Formats the data to remove additional characters
        except sqlite3.Error as error:
            print("Error",error)
        finally:
            Connection.close() #Terminates connection
        Name_Label = tkinter.Label(purchase_page, text = Item_Name) #Label creation
        Name_Label.grid(row=(1+number), column=0) # Places Label in grid
        
class Price_Label:
    def __init__(self, number, Item_ID): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        try:
            Connection = sqlite3.connect("Inventory.db") #Establishes a connection
            Cursor = Connection.cursor() #Creates a cursor
            Price_Grab = ''' SELECT Item_Price FROM INVENTORY WHERE Item_ID = ?
            '''
            #^^^Gets the Price of the item with a certain ID
            Cursor.execute(Price_Grab, Item_ID[number]) #Executes the search
            Item_Desc = numpy.array(Cursor.fetchall()) #Retrieves results from search
            Item_Price = REMOVE_CHARACTERS_1(str(Item_Desc))
        except sqlite3.Error as error:
            print("Error",error)
        finally:
            Connection.close() #Terminates connection
        Price_Label = tkinter.Label(purchase_page, text = Item_Price) #Label creation
        Price_Label.grid(row=(1+number), column=1) # Places Label in grid
        
class Return_Name_Label:
    def __init__(self, number, Item_ID): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        try:
            Connection = sqlite3.connect("Inventory.db") #Establishes a connection
            Cursor = Connection.cursor() #Creates a cursor
            Name_Grab = ''' SELECT Item_Name FROM INVENTORY WHERE Item_ID = ?
            '''
            #^^^Gets the name of the item with a certain ID
            Cursor.execute(Name_Grab, Item_ID[number]) #Executes the search
            Item_Desc = numpy.array(Cursor.fetchall()) #Retrieves results from search
            Item_Name = REMOVE_CHARACTERS_1(str(Item_Desc))
        except sqlite3.Error as error:
            print("Error",error)
        finally:
            Connection.close() #Terminates connection
        Name_Label = tkinter.Label(return_purchase_receipt_page, text = Item_Name) #Label creation
        Name_Label.grid(row=(1+number), column=0) # Places Label in grid
        
class Return_Price_Label:
    def __init__(self, number, Item_ID): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        try:
            Connection = sqlite3.connect("Inventory.db") #Establishes a connection
            Cursor = Connection.cursor() #Creates a cursor
            Price_Grab = ''' SELECT Item_Price FROM INVENTORY WHERE Item_ID = ?
            '''
            #^^^Gets the Price of the item with a certain ID
            Cursor.execute(Price_Grab, Item_ID[number]) #Executes the search
            Item_Desc = numpy.array(Cursor.fetchall()) #Retrieves results from search
            Item_Price = REMOVE_CHARACTERS_1(str(Item_Desc))
        except sqlite3.Error as error:
            print("Error",error)
        finally:
            Connection.close() #Terminates connection
        Price_Label = tkinter.Label(return_purchase_receipt_page, text = Item_Price) #Label creation
        Price_Label.grid(row=(1+number), column=1) # Places Label in grid
        
class Admin_Label:
    def __init__(self, number, Inventory_Name, Inventory_Quantity): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        Name_Label = tkinter.Label(admin_track_inventory_page, text = Inventory_Name[number]) # Creates the Label
        Name_Label.grid(row=(1+number), column=0) # Places Label in grid, uses number to find correct row.
        Quantity_Label = tkinter.Label(admin_track_inventory_page, text = Inventory_Quantity[number])
        Quantity_Label.grid(row = 1+number, column = 1)
        
class Sales_Label:
    def __init__(self, number, Inventory_Name, Inventory_Quantity): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        Name_Label = tkinter.Label(sales_track_inventory_page, text = Inventory_Name[number]) # Creates the Label
        Name_Label.grid(row=(1+number), column=0) # Places Label in grid, uses number to find correct row.
        Quantity_Label = tkinter.Label(sales_track_inventory_page, text = Inventory_Quantity[number])
        Quantity_Label.grid(row = 1+number, column = 1)

class Delete_Label:
    def __init__(self, number,Item_Name): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        Delete_Item_Label = tkinter.Label(admin_delete_items_page, text = (Item_Name[number])) # Creates the Label
        Delete_Item_Label.grid(row=(1+number), column=0) # Places Label in grid, uses number to find correct row.
    
class Delete_Button:
    def __init__(self, number, Item_ID): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        Delete_Item_Button = tkinter.Button(admin_delete_items_page, text = "Delete", command = lambda:[ admin_delete_items_page.destroy(), Admin_Delete_Items(Item_ID,number)])
        Delete_Item_Button.grid(row=(1+number), column=3) # Places Button in grid

class Delete_Account_Label:
    def __init__(self, number,Account_Name): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        Account_Label = tkinter.Label(admin_delete_account_page, text = (str(Account_Name[number]).replace("['","")).replace("']","")) # Creates the Label
        Account_Label.grid(row=(1+number), column=0) # Places Label in grid, uses number to find correct row.
    
class Delete_Account_Button:
    def __init__(self, number,Account_Name): #Constructor
        self.number = number #Which number the Label corresponds to in the array
        Account_Button = tkinter.Button(admin_delete_account_page, text = "Delete", command = lambda:[admin_delete_account_page.destroy(), Admin_Delete_Account(Account_Name[number])])
        Account_Button.grid(row=(1+number), column=3) # Places Button in grid

def Inventory_View_All(): #Displays results for a whitespace search
    i = 0
    try:
        Connection = sqlite3.connect("Inventory.db") #Establishes a connection
        Cursor = Connection.cursor() #Creates a cursor
        Inventory_View = ''' SELECT Item_Name FROM INVENTORY 
        '''
        #^^^Selects all names in the inventory
        Cursor.execute(Inventory_View) #Executes the search
        Inventory_All = Cursor.fetchall() #Retrieves results from search
        for i in range(len(Inventory_All)): #Makes a label and button for each record
            Inventory_Display_Label = Inventory_Label(i,Inventory_All)
            Inventory_Display_Button = Inventory_Button(i,Inventory_All)
    except sqlite3.Error as error:
        print("Error",error)
    finally:
        Connection.close() #Terminates connection
        
def Inventory_Search(): #Displays results for a text search
    Search_Target = SearchBar_Entry.get() # Retrieves user input from searchbar
    try:
        Connection = sqlite3.connect("Inventory.db") # Establishes connection to database
        Cursor = Connection.cursor() # Creates cursor
        Inventory_Search = '''SELECT * FROM INVENTORY WHERE Item_Name=? OR Item_ID=?
        '''
        #^^^Selects the item if the ID/name matches
        Cursor.execute(Inventory_Search,(Search_Target, Search_Target,)) # Runs the sql statement
        Search_Results = Cursor.fetchall() # Retrieves all results if any
        if str(Search_Results) != "[]": # If the SQL query returns a record
            customer_main_page.destroy() #Destroy current UI
            SEARCH_RESULT_UI(Search_Results) #Make new UI to display search results.
        else: # If no results are found
            Search_Error_Label = tkinter.Label(customer_main_page, text = "Error: No results found") #Display error to UI
            Search_Error_Label.grid(row = 2, column = 0) #Place error message in grid
    except sqlite3.Error as Error: # Error handling
        print("Error",Error)
    finally:
        Connection.close() # Terminate connection
        
def Admin_Add_Item(Item_Name_, Item_Type_, Item_Quantity, Item_Price, Item_Offer, Item_Colour_): #Allows admin to add an item to the inventory
    Error_Label = tkinter.Label(admin_add_item_page, text = "") #Label made in advance for displaying errors to user
    Error_Label.grid(row = 8, column = 0, columnspan=2)
    Item_Name = Item_Name_.upper() #Formats results to all caps
    Item_Type = Item_Type_.upper()
    Item_Colour = Item_Colour_.upper()
    if Item_Name == "" or Item_Type == "" or Item_Quantity == "" or Item_Price == "" or Item_Offer == "" or Item_Colour == "": #Checks if any fields are left blank
        Error_Label["text"] = "Error: Fields cannot be left blank"
    else:
        if Item_Price == "0.0": #Checks if item is free
            Error_Label["text"] = "Error: Price cannot be zero"
        else:
            if Item_Offer.count(".") != 1: #Checks offer will be a decimal
                Error_Label["text"] = "Error: Item Offer has incorrect number of decimal point (1 expected)"
            else:
                Item_Offer_Temp = Item_Offer.replace(".","")
                Item_Price_Temp = Item_Price.replace(".","")
                if Item_Offer_Temp.isdigit() != True or Item_Price_Temp.isdigit() != True: #Checks that price or offer are numbers
                    Error_Label["text"] = "Error: Item Offer or Item Price not correct format (E.G. 10.50)"
                else:
                    Connection = sqlite3.connect("Inventory.db") # Establishes connection to db
                    Cursor = Connection.cursor()
                    try:
                        Find_Item_ID = ''' SELECT Item_ID FROM INVENTORY ORDER BY Item_ID
                        '''
                        #^^^Selects all item Ids in order
                        Add_Item=''' INSERT INTO INVENTORY (Item_ID, Item_Name, Item_Type, Item_Quantity, Item_Price, Item_Offer_Price, Item_Colour) VALUES (?,?,?,?,?,?,?)
                        '''
                        #^^^ Inserts new entry into inventory
                        Cursor.execute(Find_Item_ID)
                        Results = Cursor.fetchall()
                        Formatted_Results = (str(Results).replace("[","")).replace("]","") #Formating result 
                        Results_Array = Formatted_Results.split(", ") #Converting to array
                        Last_ID = Results_Array[len(Results_Array)-1] #Popping unusable item generated as byproduct of split.
                        Formatted_Last_ID = ((Last_ID.replace("(","")).replace(",","")).replace(")","")
                        Next_Available_ID = int(Formatted_Last_ID)+1 #Designates next available ID
                        Cursor.execute(Add_Item,(Next_Available_ID,Item_Name,Item_Type,Item_Quantity,Item_Price,Item_Offer,Item_Colour,))
                        Connection.commit()    #Saves changes
                    except sqlite3.Error as error:
                        print("Error",error)                
                    finally:
                        Error_Label["text"] = "Item Added Successfully" #Tells user item has been added
                        Connection.close()

def Admin_Update_Item(Item_ID,Item_Name_, Item_Type_, Item_Quantity, Item_Price, Item_Offer, Item_Colour_): #Change an item already in the db
    Error_Label = tkinter.Label(admin_edit_item_page, text = "")
    Error_Label.grid(row = 8, column = 0)
    Item_Name = Item_Name_.upper() #Format inputs
    Item_Type = Item_Type_.upper()
    Item_Colour = Item_Colour_.upper()
    if Item_Name == "" or Item_Type == "" or Item_Quantity == "" or Item_Price == "" or Item_Offer == "" or Item_Colour == "":
        Error_Label["text"] = "Error: Fields cannot be left blank"
    else:
        if Item_Price == "0.0":
            Error_Label["text"] = "Error: Price cannot be zero"
        else:
            if Item_Offer.count(".") != 1:
                Error_Label["text"] = "Error: Item Offer has incorrect number of decimal point (1 expected)"
            else:
                Item_Offer_Temp = Item_Offer.replace(".","")
                Item_Price_Temp = Item_Price.replace(".","")
                if Item_Offer_Temp.isdigit() != True or Item_Price_Temp.isdigit() != True:
                    Error_Label["text"] = "Error: Item Offer or Item Price not correct format (E.G. 10.50)"
                else:
                    Connection = sqlite3.connect("Inventory.db")
                    Cursor = Connection.cursor()
                    try:
                        Update_Item = ''' UPDATE INVENTORY SET 
                            Item_ID = (?),
                            Item_Name = (?),
                            Item_Type = (?), 
                            Item_Quantity = (?), 
                            Item_Price = (?),
                            Item_Offer_Price = (?), 
                            Item_Colour = (?) WHERE ITEM_ID = (?)
                        '''
                        #^^^ Changes item in db
                        Cursor.execute(Update_Item, (Item_ID,Item_Name,Item_Type,Item_Quantity,Item_Price,Item_Offer,Item_Colour,Item_ID,))
                        Connection.commit() #Saves
                    finally:
                        Connection.close()

def Admin_Delete_Items(Item_ID,number):
    Formatted_Item_ID = (((str(Item_ID).replace("[","")).replace("(","")).replace(")","")).replace("]","") #Formats item
    Item_ID_Array = Formatted_Item_ID.split(", ") #Converts to array
    Item = (str(Item_ID_Array[number])).replace(",","")
    Connection = sqlite3.connect("Inventory.db")
    Cursor = Connection.cursor()
    try:
        Delete_Item = ''' DELETE FROM INVENTORY WHERE Item_ID = (?)
        '''
        #^^^Deletes item from db
        Cursor.execute(Delete_Item, Item)
        Connection.commit()
    finally:
        Connection.close()
        ADMIN_DELETE_ITEM_UI() #Goes back to UI

def Admin_Delete_Account(Account_Name):
    Formated_Account_Name = REMOVE_CHARACTERS_1(str(Account_Name))
    Connection = sqlite3.connect("Accounts.db")
    Cursor = Connection.cursor()
    try:
        Delete_Account = ''' DELETE FROM ACCOUNTS WHERE Accounts_UserName = (?)
        '''
        #^^^Deletes account from db
        Cursor.execute(Delete_Account, (Formated_Account_Name,))
        Connection.commit()
    finally:
        Connection.close()
        ADMIN_MAIN_PAGE_UI() #Goes back to UI

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@# Accounts/Login

def Establish_Accounts():
    try: #Creating initial Accounts table
        Connection = sqlite3.connect("Accounts.db") #Establish a connection
        Cursor = Connection.cursor() #Creates cursor for database
        Accounts_Create = ''' CREATE TABLE IF NOT EXISTS ACCOUNTS (
            Accounts_UserName text PRIMARY KEY,
            Accounts_Password text,
            Accounts_User_Type text
        )'''
        #^^^ Creates Accounts table, does not populate table with records.
        Cursor.execute(Accounts_Create) #Executes
        Connection.commit() #Saves changes
    except sqlite3.Error as Error:
        print("Error creating Accounts table",Error)
    
    try: #Inserting all initial users into accounts
        Accounts_Insert_1=''' INSERT INTO ACCOUNTS (Accounts_UserName, Accounts_Password, Accounts_User_Type) VALUES ("PH_ADMIN", "PH_PASSWORD_ADMIN", "ADMIN")
        '''
        Accounts_Insert_2=''' INSERT INTO ACCOUNTS (Accounts_UserName, Accounts_Password, Accounts_User_Type) VALUES ("PH", "PH_PASSWORD", "CUSTOMER")
        '''
        Accounts_Insert_3=''' INSERT INTO ACCOUNTS (Accounts_UserName, Accounts_Password, Accounts_User_Type) VALUES ("PH_SALES", "PH_PASSWORD_SALES", "SALES")
        '''
        #^^^Adding each record individually for initial startup
        Cursor.execute(Accounts_Insert_1)#executing each record addition.
        Cursor.execute(Accounts_Insert_2)
        Cursor.execute(Accounts_Insert_3)
        Connection.commit() #Saves changes
    except sqlite3.Error as error:
        print("Records already exist")
    finally:
        Connection.close() #Close connection
    
def Login():
    UserName_Get = UserName_Entry.get()
    Password_Get = Password_Entry.get()
    if UserName_Get == "" or Password_Get == "":
        Login_Error_Label = tkinter.Label(root, text = "Field cannot be blank")
        Login_Error_Label.grid(row = 3, column = 0)
    else:
        try:
            Connection = sqlite3.connect("Accounts.db") #Establishes a connection
            Cursor = Connection.cursor() #Creates a cursor
            Accounts_Search = '''SELECT Accounts_User_Type FROM ACCOUNTS WHERE Accounts_UserName = ? AND Accounts_Password = ?
            '''
            #^^^Searches for username and password
            Cursor.execute(Accounts_Search, (UserName_Get, Password_Get)) #Executes the search
            Search_Results = Cursor.fetchall() #Retrieves search result
            if str(Search_Results) == "[]":
                Login_Error_Label = tkinter.Label(root, text = "Account Not found")
                Login_Error_Label.grid(row = 3, column = 0)
            else:
                if str(Search_Results) == "[('CUSTOMER',)]": #Checks the user type to send to appropriate UI
                    global Current_Customer
                    Current_Customer = UserName_Get
                    root.destroy()
                    CUSTOMER_MAIN_PAGE_UI()
                elif str(Search_Results) == "[('ADMIN',)]":
                    root.destroy()
                    ADMIN_MAIN_PAGE_UI()
                elif str(Search_Results) == "[('SALES',)]":
                    root.destroy()
                    SALES_MAIN_PAGE_UI()
                else:
                    print("Error, User Type not found")
        except sqlite3.Error as Error:
            print("Error",Error)
        finally:
            Connection.close()

def Admin_Add_User(UserName, Password, Confirm_Password, User_Type_): 
    User_Type = User_Type_.upper() #Formats inputs
    if Password == Confirm_Password: #If password and confirm password are the same
        if UserName != "" and Password != "" and Confirm_Password != "" and User_Type != "": #Checks for blank fields
            if (User_Type == "CUSTOMER" or User_Type == "SALES" or User_Type == "ADMIN"): #Checks user type is correct
                try:
                    Connection = sqlite3.connect("Accounts.db")
                    Cursor = Connection.cursor()
                    Add_User = ''' INSERT INTO ACCOUNTS (Accounts_UserName, Accounts_Password, Accounts_User_Type) VALUES (?,?,?)
                    '''
                    #^^^Adds user to db
                    Cursor.execute(Add_User, (UserName, Password, User_Type,))
                    Add_User_Confirmation_Label = tkinter.Label(admin_main_page, text = "User Added Successfully")
                    Add_User_Confirmation_Label.grid(row = 6, column = 0)
                    Connection.commit()
                except sqlite3.Error as error:
                    print("Error",error)
                finally:
                    Connection.close()
            else:
                Add_User_Confirmation_Label = tkinter.Label(admin_main_page, text = "User Type invalid")
                Add_User_Confirmation_Label.grid(row = 6, column = 0)
        else:
            Add_User_Confirmation_Label = tkinter.Label(admin_main_page, text = "A field has been left blank")
            Add_User_Confirmation_Label.grid(row = 6, column = 0)

    else:
        Add_User_Confirmation_Label = tkinter.Label(admin_main_page, text = "Passwords Do not match")
        Add_User_Confirmation_Label.grid(row = 6, column = 0)

def Customer_Add_User(UserName, Password, Confirm_Password, User_Type): #Same as admin but limits the user type to customer
    if Password == Confirm_Password:
        if UserName != "" and Password != "" and Confirm_Password != "":
            try:
                Connection = sqlite3.connect("Accounts.db")
                Cursor = Connection.cursor()
                Add_User = ''' INSERT INTO ACCOUNTS (Accounts_UserName, Accounts_Password, Accounts_User_Type) VALUES (?,?,?)
                '''
                Cursor.execute(Add_User, (UserName, Password, User_Type,))
                Connection.commit()
                Add_User_Confirmation_Label = tkinter.Label(create_account_page, text = "User Added Successfully, Go back to Login Page.")
                Add_User_Confirmation_Label.grid(row = 5, column = 0)
            except sqlite3.Error as error:
                print("Error",error)
            finally:
                Connection.close()
        else:
            Add_User_Confirmation_Label = tkinter.Label(create_account_page, text = "A field has been left blank")
            Add_User_Confirmation_Label.grid(row = 5, column = 0)
    else:
        Add_User_Confirmation_Label = tkinter.Label(create_account_page, text = "Passwords Do not match")
        Add_User_Confirmation_Label.grid(row = 5, column = 0)
        
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@# Basket

def Establish_Basket():
    try: #Creating initial Basket table
        Connection = sqlite3.connect("Basket.db") #Establish a connection
        Cursor = Connection.cursor() #Creates cursor for database
        Basket_Create=''' CREATE TABLE IF NOT EXISTS BASKET (
            Basket_Receipt_ID integer PRIMARY KEY,
            Basket_UserName text,
            Basket_Items text
        )'''
        #^^^ Creates Basket table, does not populate table with records.
        Cursor.execute(Basket_Create) #Executes
        Connection.commit() #Saves changes
    except sqlite3.Error as Error:
        print("Error creating Basket table",Error)
    finally:
        Connection.close()
            
def Add_To_Basket(Item_ID):
    global Is_Basket_Real
    Is_Basket_Real = 0
    Connection = sqlite3.connect("Basket.db") #Establishes a connection
    Cursor = Connection.cursor() #Creates a cursor
    try: #Search for existing Basket
        Basket_Search = ''' SELECT * FROM BASKET WHERE Basket_UserName = (?)
        '''
        #^^^Searches for a basket with the same username as current user
        Cursor.execute(Basket_Search, (Current_Customer,))
        Connection.commit()
        Basket_Search_Results = Cursor.fetchall()
        if str(Basket_Search_Results) != "[]":
            Is_Basket_Real = 1
    except sqlite3.Error as error:
            print("Error",error)
    if Is_Basket_Real == 0: # If there is no existing Basket
        try: #Search for existing Basket
            Most_Recent_ID_Search = ''' SELECT Basket_Receipt_ID FROM BASKET ORDER BY Basket_Receipt_ID
            '''
            #^^^Searches for the highest basket ID
            Cursor.execute(Most_Recent_ID_Search)
            Connection.commit()
            ID_Search_Results = Cursor.fetchall()
            if len(ID_Search_Results) != 0:
                Highest_ID = int(((str(ID_Search_Results[(len(ID_Search_Results)-1)]).replace("(","")).replace(",","")).replace(")","")) #formatting data to be an int to perform calculations on
            else:
                Highest_ID = 0
        except sqlite3.Error as error:
            print("Error",error)
        try: #Creating new basket
            Basket_Insert=''' INSERT INTO BASKET (Basket_Receipt_ID, Basket_UserName, Basket_Items) VALUES ((?+1), ?, ?)
            '''
            #^^^Adding Basket record individually for initial startup
            Item=Item_ID+","
            Cursor.execute(Basket_Insert, (Highest_ID, Current_Customer, Item))#executing each record addition.
            Connection.commit() #Saves changes
        except sqlite3.Error as error:
            print("Error",error)
        finally:
            Connection.close() #Close connection
    else:
        try:
            Basket_Items_Retrieve = ''' SELECT * FROM BASKET WHERE Basket_UserName =?
            '''
            Basket_Update = ''' UPDATE BASKET SET Basket_Items = (?) WHERE Basket_UserName = (?)
            '''
            Cursor.execute(Basket_Items_Retrieve, (Current_Customer,))
            Basket = numpy.array(Cursor.fetchall()) #saves basket as an array
            Formated_Basket = REMOVE_CHARACTERS_2(Basket[0,2]) #Formats basket
            Item_ID+=","
            Formated_Basket+=Item_ID #Appends an item to the basket
            Cursor.execute(Basket_Update, (Formated_Basket, Current_Customer,))
            Connection.commit()
        except sqlite3.Error as error:
            print("Error adding Basket",error)
        finally:
            Connection.close()
            
def Grab_Basket():
    Connection = sqlite3.connect("Basket.db") #Establishes a connection
    Cursor = Connection.cursor() #Creates a cursor
    try: #Search for existing Basket
        Basket_Search = ''' SELECT * FROM BASKET WHERE Basket_UserName = (?)
        '''
        #^^^Searches for a basket with the same username as current user
        Cursor.execute(Basket_Search, (Current_Customer,))
        Connection.commit()
        Basket = numpy.array(Cursor.fetchall())
        if str(Basket) != "[]": #If basket isnt blank
            Formated_Basket = REMOVE_CHARACTERS(Basket[0,2])
            Basket_Array = (Formated_Basket.split(","))
            Basket_Array.pop(len(Basket_Array)-1) #Removes byproduct array position
        else:
            CUSTOMER_MAIN_PAGE_UI()
    finally:
        Connection.close()
        BASKET_VIEW_UI(Basket_Array)

def Delete_Basket_Item(Basket_Array):
    Basket_Array = str(Basket_Array) #Formats updated basket
    Connection = sqlite3.connect("Basket.db")
    Cursor = Connection.cursor()
    try:
        Basket_Update = ''' UPDATE BASKET SET Basket_Items = (?) WHERE Basket_UserName = (?)
        '''
        Formated_Basket = REMOVE_CHARACTERS_3(Basket_Array)
        Formated_Basket+=","
        Cursor.execute(Basket_Update, (Formated_Basket,Current_Customer,))
        Connection.commit()
    finally:
        Connection.close()
        Basket_Array_ = (Formated_Basket.split(","))
        Basket_Array_.pop(len(Basket_Array_)-1)
        BASKET_VIEW_UI(Basket_Array_) #Goes back to UI with edited array to remake UI without the removed item
        
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@# Purchases/Returns

def Establish_Purchases():
    Connection = sqlite3.connect("Purchases.db")
    Cursor  = Connection.cursor()
    try:
        Establish_Purchases = ''' CREATE TABLE IF NOT EXISTS PURCHASES (
            Purchases_Receipt_ID integer PRIMARY KEY,
            Purchases_Items text,
            Purchase_Price real,
            Purchase_Is_Invoice_Sent text,
            Purchase_Is_Returned text    
        )
        '''
        Cursor.execute(Establish_Purchases)
        Connection.commit()
    finally:
        Connection.close()
        
def Establish_Returns():
    Connection = sqlite3.connect("Returns.db")
    Cursor = Connection.cursor()
    try:
        Establish_Returns = ''' CREATE TABLE IF NOT EXISTS RETURNS_RECEIPT (
            Returns_Receipt_ID integer PRIMARY KEY,
            Returns_Items text,
            Returns_Price real    
        )
        '''
        Cursor.execute(Establish_Returns)
        Connection.commit()
    finally:
        Connection.close()
        
def Make_Purchase(Item_Array,Total_Price):
    i=0
    Item_Array = REMOVE_CHARACTERS_1(Item_Array) # Formats item array
    Connection = sqlite3.connect("Basket.db")
    Cursor = Connection.cursor()
    try:
        Find_Basket_Receipt_ID = ''' SELECT Basket_Receipt_ID FROM BASKET WHERE Basket_UserName = (?)
        '''
        #^^^Grabs basket id for current user
        Cursor.execute(Find_Basket_Receipt_ID,(Current_Customer,))
        Receipt_ID = Cursor.fetchall()
        Formated_Receipt_ID = (REMOVE_CHARACTERS_1(str(Receipt_ID))).replace(",","")
    finally:
        Connection.close()
        Connection = sqlite3.connect("Purchases.db")
        Cursor = Connection.cursor()
        try:
            Make_Receipt = ''' INSERT INTO PURCHASES (Purchases_Receipt_ID, Purchases_Items, Purchase_Price, Purchase_Is_Invoice_Sent, Purchase_Is_Returned) VALUES (?,?,?,"FALSE","FALSE")
            '''
            #^^^Saves receipt to purchases
            Cursor.execute(Make_Receipt, (Formated_Receipt_ID, Item_Array, Total_Price))
            Connection.commit()
        finally:
            Connection.close()
            Item_Array_Array = Item_Array.split(",") #Creates array
            for i in range(len(Item_Array_Array)): #Updates quantity for every item in basket
                Connection = sqlite3.connect("Inventory.db")
                Cursor = Connection.cursor()
                try:
                    Get_Quantity = ''' SELECT Item_Quantity FROM INVENTORY WHERE Item_ID = (?)
                    '''
                    Update_Quantity = ''' UPDATE INVENTORY SET Item_Quantity = (?) WHERE ITEM_ID = (?)
                    '''
                    #^^^Finds and lowers quantity by 1
                    Cursor.execute(Get_Quantity, (Item_Array_Array[i],))
                    Current_Quantity = REMOVE_CHARACTERS_1(Cursor.fetchall()).replace(",","")
                    New_Quantity = int(Current_Quantity) - 1 #Lowers quantity by 1
                    Cursor.execute(Update_Quantity, (New_Quantity, Item_Array_Array[i]))
                finally:
                    Connection.commit()
                    Connection.close()
                    try:
                        Connection = sqlite3.connect("Basket.db")
                        Cursor = Connection.cursor()
                        Delete_Basket = ''' UPDATE BASKET SET Basket_UserName = "" WHERE Basket_UserName = (?)
                        '''
                        #^^^Removes username from basket as username is no longer needed but basket is
                        Cursor.execute(Delete_Basket, (Current_Customer,))
                    finally:
                        Connection.commit()
                        Connection.close()
                        RECEIPT_DISPLAY_UI(Formated_Receipt_ID,"PURCHASE")

def Make_Return_Receipt(Item_Array,Total_Price, Purchases_ID):
    i=0
    Item_Array = REMOVE_CHARACTERS_1(Item_Array) #Formats array
    Connection = sqlite3.connect("Returns.db")
    Cursor = Connection.cursor()
    try:
        Make_Receipt = ''' INSERT INTO RETURNS_RECEIPT (Returns_Receipt_ID, Returns_Items, Returns_Price) VALUES (?,?,?)
        '''
        #^^^Creates return receipt
        Cursor.execute(Make_Receipt, (int(Purchases_ID), Item_Array, float(Total_Price)))
        Connection.commit()
    finally:
        Connection.close()
        Item_Array_Array = Item_Array.split(",") #Creates array
        for i in range(len(Item_Array_Array)): #Updates quantity of each item in array
            Connection = sqlite3.connect("Inventory.db")
            Cursor = Connection.cursor()
            try:
                Get_Quantity = ''' SELECT Item_Quantity FROM INVENTORY WHERE Item_ID = (?)
                 '''
                Update_Quantity = ''' UPDATE INVENTORY SET Item_Quantity = (?) WHERE ITEM_ID = (?)
                '''
                #^^^Increase returned items quantity by 1
                Cursor.execute(Get_Quantity, (Item_Array_Array[i],))
                Current_Quantity = REMOVE_CHARACTERS_1(Cursor.fetchall()).replace(",","")
                New_Quantity = int(Current_Quantity) + 1
                Cursor.execute(Update_Quantity, (New_Quantity, Item_Array_Array[i]))
            finally:
                Connection.commit()
                Connection.close()
                try:
                    Connection = sqlite3.connect("Purchases.db")
                    Cursor = Connection.cursor()
                    Mark_Purchase = ''' UPDATE PURCHASES SET Purchase_Is_Returned = "TRUE" WHERE Purchases_Receipt_ID = (?)
                    '''
                    #^^^Marks a purchase as returned so it cannot be returned multiple times
                    Cursor.execute(Mark_Purchase, (Purchases_ID,))
                finally:
                    Connection.commit()
                    Connection.close()
                    RECEIPT_DISPLAY_UI(Purchases_ID,"RETURN")

def Generate_Purchase_QR(QR_Data): #Creates QR code for purchase
    QR_Name = ("Purchase_Receipt"+str(QR_Data)+".png")
    QR_Object = qrcode.QRCode(version=1, box_size=12)
    QR_Object.add_data(QR_Data)
    QR_Object.make()
    image = QR_Object.make_image()
    image.save(QR_Name)
    
def Generate_Return_QR(QR_Data): # Creates QR code for returns
    QR_Name = ("Return_Receipt"+str(QR_Data)+".png")
    QR_Object = qrcode.QRCode(version=1, box_size=12)
    QR_Object.add_data(QR_Data)
    QR_Object.make()
    image = QR_Object.make_image()
    image.save(QR_Name)
    
def Return_Purchase(Receipt_ID): 
    if ".png" in Receipt_ID: #Checks if user is uploading a qr code
        QR_Code = cv2.imread(Receipt_ID)
        Detector = cv2.QRCodeDetector()
        Data, Array, QR = Detector.detectAndDecode(QR_Code)
        if Array is not None: #If it is a qr code
            Receipt_ID = Data #Changes input to be equivalent of receipt ID
    Connection = sqlite3.connect("Purchases.db")
    Cursor = Connection.cursor()
    Error_Message_Label = tkinter.Label(return_purchase_page, text = "") #Error label in advance
    Error_Message_Label.grid(row = 2, column = 0)
    try:
        Retrieve_Purchase = ''' SELECT * FROM PURCHASES WHERE Purchases_Receipt_ID = (?)
        '''
        #^^^Finds receipt
        Cursor.execute(Retrieve_Purchase, (Receipt_ID,))
        Results = numpy.array(Cursor.fetchall())
    finally:
        Connection.close()
    if str(Results) != "[]": #If there is a receipt
        if Results[0,4] == "FALSE": #Checks if item has already been returned
            return_purchase_page.destroy()
            RETURN_PURCHASE_RECEIPT_UI(Results)
        else:
            Error_Message_Label["text"] = "Order has already been returned"
    else:
        Error_Message_Label["text"] = "No Receipt Found"
        
######################################################################## Tkinter

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@# Login Page

def LOGIN_UI():
    global UserName_Entry
    global Password_Entry
    global root
    root = tkinter.Tk()
    UserName_Label = tkinter.Label(root, text = "Username:")
    Password_Label = tkinter.Label(root, text = "Password:")
    UserName_Label.grid(row = 0, column = 0)
    Password_Label.grid(row = 1, column = 0)
    UserName_Entry = tkinter.Entry(root)
    Password_Entry = tkinter.Entry(root)
    UserName_Entry.grid(row = 0, column = 1)
    Password_Entry.grid(row = 1, column = 1)
    Submit_Button = tkinter.Button(root, text = "Submit", command = Login)
    Submit_Button.grid(row = 2, column = 0)
    Create_Account_Label = tkinter.Label(root, text = "No Account?")
    Create_Account_Label.grid(row = 3, column = 0)
    Create_Account_Button = tkinter.Button(root, text = "Create Account", command = lambda:[root.destroy(),CREATE_ACCOUNT_UI()])
    Create_Account_Button.grid(row = 3, column = 1)
    
    root.mainloop()
    
def CREATE_ACCOUNT_UI():
    global create_account_page
    create_account_page = tkinter.Tk()
    Add_User_Label = tkinter.Label(create_account_page, text = "Add User:")
    Add_User_Label.grid(row = 0, column = 0, columnspan = 2)
    Add_UserName_Label = tkinter.Label(create_account_page, text = "UserName")
    Add_UserName_Label.grid(row = 1, column = 0)
    Add_UserName_Entry = tkinter.Entry(create_account_page, width = 75)
    Add_UserName_Entry.grid(row = 1, column = 1)
    Add_Password_Label = tkinter.Label(create_account_page, text = "Add Password")
    Add_Password_Label.grid(row = 2, column = 0)
    Add_Password_Entry = tkinter.Entry(create_account_page, width = 75)
    Add_Password_Entry.grid(row = 2, column = 1)
    Add_Confirm_Password_Label = tkinter.Label(create_account_page, text = "Confirm Password")
    Add_Confirm_Password_Label.grid(row = 3, column = 0)
    Add_Confirm_Password_Entry = tkinter.Entry(create_account_page, width = 75)
    Add_Confirm_Password_Entry.grid(row = 3, column = 1)
    Create_Account_Button = tkinter.Button(create_account_page, text = "Create Account", command = lambda:[Customer_Add_User(Add_UserName_Entry.get(),Add_Password_Entry.get(),Add_Confirm_Password_Entry.get(),"CUSTOMER")])
    Create_Account_Button.grid(row = 4, column = 0)
    Back_Button = tkinter.Button(create_account_page, text = "Back", command = lambda:[create_account_page.destroy(),LOGIN_UI()])
    Back_Button.grid(row = 0, column = 3)
    
    create_account_page.mainloop()

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@# User Page

def CUSTOMER_MAIN_PAGE_UI():
    global customer_main_page
    global SearchBar_Entry
    customer_main_page = tkinter.Tk() # Creating the window for all widgets
    SearchBar_Label = tkinter.Label(customer_main_page, text = "Search: ") #Label to indicate the Search bar
    SearchBar_Label.grid(row = 0, column = 0) #Places the widget in a grid inside the window
    SearchBar_Entry = tkinter.Entry(customer_main_page, width = 100) #Creates an entry to allow user to type their input.
    SearchBar_Entry.grid(row = 0, column = 1, columnspan = 2) #Places the widget in the grid
    Search_Button = tkinter.Button(customer_main_page, text = "Search", command = Inventory_Search) #Button to allow user to submit the entry, will run a search using the input from the user
    Search_Button.grid(row = 1, column = 0) #Places the widget in the grid
    View_All_Button = tkinter.Button(customer_main_page, text = "View All Items", command = Inventory_View_All) #Button to view the whole inventory, runs function to display all items
    View_All_Button.grid(row = 0, column = 4) #Places the widget in the grid
    View_Basket_Button = tkinter.Button(customer_main_page, text = "View Basket", command = lambda:[customer_main_page.destroy(),Grab_Basket()]) #Button to allow user to view their basket.
    View_Basket_Button.grid(row = 0, column = 5) #Places the widget in the grid
    Return_Items_Button = tkinter.Button(customer_main_page, text = "Return_Items", command = lambda:[customer_main_page.destroy(),RETURN_PURCHASE_UI()])
    Return_Items_Button.grid(row = 1, column= 5)
    
    customer_main_page.mainloop() #Begins an infinite loop to get inputs from the user.
    
def SEARCH_RESULT_UI(Search_Result):
    global search_result_page #Make window global to edit in other functions
    String_Search_Result = (((((str(Search_Result)).replace("[", "")).replace("(", "")).replace(")", "")).replace("]", "")).replace("'", "") #Format the SQL result to make it easier to use.
    Array_Search_Result = (String_Search_Result.split(",")) #Turn Formatted result into an array to make it easier to access elements.
    search_result_page = tkinter.Tk() #Create window
    Search_result_ItemName_Label = tkinter.Label(search_result_page, text = "Item Name: ") #Creates Label
    Search_result_ItemName_Label.grid(row = 0, column = 0) #Places in grid
    Search_result_Name_Label = tkinter.Label(search_result_page, text = Array_Search_Result[1]) #Finds name from array and prints name
    Search_result_Name_Label.grid(row = 0, column = 1)
    Search_result_ItemType_Label = tkinter.Label(search_result_page, text = "Item Type: ")
    Search_result_ItemType_Label.grid(row = 1, column = 0)
    Search_result_Type_Label = tkinter.Label(search_result_page, text = Array_Search_Result[2]) 
    Search_result_Type_Label.grid(row = 1, column = 1)
    Search_result_ItemQuantity_Label = tkinter.Label(search_result_page, text = "Quantity: ")
    Search_result_ItemQuantity_Label.grid(row = 2, column = 0)
    Search_result_Quantity_Label = tkinter.Label(search_result_page, text = Array_Search_Result[3])
    Search_result_Quantity_Label.grid(row = 2, column = 1)
    Search_Result_Filler_Row_Label = tkinter.Label(search_result_page, text = "")
    Search_Result_Filler_Row_Label.grid(row = 3, column = 0)
    Search_result_ItemPrice_Label = tkinter.Label(search_result_page, text = "Price: ")
    Search_result_Price_Label = tkinter.Label(search_result_page, text = Array_Search_Result[4])
    Search_result_Price_Label.grid(row = 4, column = 1)
    Search_result_ItemPrice_Label.grid(row = 4, column = 0)
    if Array_Search_Result[5] != " 0.0": #If there is a current discount add discounted price widgets
        Actual_Price = float(Array_Search_Result[4])*float(Array_Search_Result[5]) #Calculate discounted price
        Search_result_ItemDiscountedPrice_Label = tkinter.Label(search_result_page, text = "Current Discounted Price: ")
        Search_result_ItemDiscountedPrice_Label.grid(row = 5, column = 0)
        Search_result_DiscountedPrice_Label = tkinter.Label(search_result_page, text = str(Actual_Price), bg = "green")
        Search_result_DiscountedPrice_Label.grid(row = 5, column = 1)
    Search_result_Basket_Button = tkinter.Button(search_result_page, text = "Add to Basket", command = lambda:[Add_To_Basket(Array_Search_Result[0])]) #Add the item ID to basket
    Search_result_Basket_Button.grid(row = 6, column = 0)
    Back_To_Mainpage_Button = tkinter.Button(search_result_page, text = "Back", command = lambda:[search_result_page.destroy(), CUSTOMER_MAIN_PAGE_UI()]) #Returns to the main page
    Back_To_Mainpage_Button.grid (row = 0, column = 4, columnspan= 2)
    
    search_result_page.mainloop() #Begin UI loop
    
def BASKET_VIEW_UI(Basket_Array): # UI element for Basket
    i=0
    global basket_view_page # global so widgets can be make in class funcion
    basket_view_page = tkinter.Tk()
    Basket_Label = tkinter.Label(basket_view_page, text = "Basket: ") # Creates Basket Label
    Basket_Label.grid(row = 0, column = 0) # Places Label in grid
    Back_Button = tkinter.Button(basket_view_page, text = "Back", command = lambda:[basket_view_page.destroy(),CUSTOMER_MAIN_PAGE_UI()])
    Back_Button.grid(row = 0, column = 4)
    Purchase_Button = tkinter.Button(basket_view_page, text = "Purchase", command = lambda:[basket_view_page.destroy(),PURCHASE_UI(Basket_Array)])
    Purchase_Button.grid(row = 1, column = 4)
    for i in range(len(Basket_Array)): # Creates Labels and Buttons for every entity in the array.
        Display_Label = Label_(i,Basket_Array) # Triggers Constructor
        Display_Button = Button_(i,Basket_Array) # Triggers Constructor 
    basket_view_page.mainloop() # Begins UI mainloop
    
def PURCHASE_UI(Basket_Array):
    i=0
    Total_Price = 0.0
    global purchase_page
    purchase_page = tkinter.Tk()
    Purchase_Label = tkinter.Label(purchase_page, text = "Purchase Summary: ")
    Purchase_Label.grid(row = 0, column = 0, columnspan = 2)
    for i in range(len(Basket_Array)): #Gets price of every item in basket and adds the total cost
        Connection = sqlite3.connect("Inventory.db")
        Cursor = Connection.cursor()
        try:
            Price_Get = '''SELECT Item_Price FROM INVENTORY WHERE Item_ID = (?)
            '''
            #Gets price
            Cursor.execute(Price_Get, (Basket_Array[i],))
            Results = numpy.array(Cursor.fetchall())
            Total_Price = Total_Price + float((str(Results).replace("[","")).replace("]","")) #Adds to total price
        finally:
            Connection.close()
        Item_Name_Label = Name_Label(i,Basket_Array)
        Item_Price_Label = Price_Label(i,Basket_Array)
    Total_Price_Label = tkinter.Label(purchase_page, text = "Total Price: ")
    Total_Price_Label.grid(row = 2+len(Basket_Array), column = 0)
    Total_Price_Label_2 = tkinter.Label(purchase_page, text = str(Total_Price))
    Total_Price_Label_2.grid(row = 2+len(Basket_Array), column = 1)
    Purchase_Proceed_Button = tkinter.Button(purchase_page, text = "Purchase", command = lambda:[purchase_page.destroy(),Make_Purchase(Basket_Array,Total_Price)])
    Purchase_Proceed_Button.grid(row = 0, column = 3)
    
def RECEIPT_DISPLAY_UI(Formatted_Receipt_ID,Return_Or_Purchase):
    global receipt_page
    receipt_page = tkinter.Tk()
    Receipt_Label = tkinter.Label(receipt_page, text = "Receipt Code:")
    Receipt_Label.grid(row = 0, column = 0)
    Receipt_ID_Label = tkinter.Label(receipt_page, text = str(Formatted_Receipt_ID))
    Receipt_ID_Label.grid(row = 0, column = 1)
    if Return_Or_Purchase == "RETURN": #Checks if receipt is for a return or a purchase
        Generate_Return_QR(Formatted_Receipt_ID)
    elif Return_Or_Purchase == "PURCHASE":
        Generate_Purchase_QR(Formatted_Receipt_ID)
    
    receipt_page.mainloop()
    
def RETURN_PURCHASE_UI():
    global return_purchase_page
    return_purchase_page = tkinter.Tk()
    Return_Purchase_Label = tkinter.Label(return_purchase_page, text = "Return Purchase:")
    Return_Purchase_Label.grid(row = 0, column = 0)
    Enter_Receipt_ID_Label = tkinter.Label(return_purchase_page, text = "Enter Receipt Code/ QR Code File Name:")
    Enter_Receipt_ID_Label.grid(row = 1, column = 0)
    Enter_Receipt_ID_Entry = tkinter.Entry(return_purchase_page)
    Enter_Receipt_ID_Entry.grid(row = 1, column = 1)
    Return_Items_Button = tkinter.Button(return_purchase_page, text = "Return", command = lambda:[Return_Purchase(Enter_Receipt_ID_Entry.get())])
    Return_Items_Button.grid(row = 1, column = 2)
    Back_Button = tkinter.Button(return_purchase_page, text = "Back", command = lambda:[return_purchase_page.destroy(),CUSTOMER_MAIN_PAGE_UI()])
    Back_Button.grid(row = 0, column = 2)
    
    return_purchase_page.mainloop()
    
def RETURN_PURCHASE_RECEIPT_UI(Results):
    global return_purchase_receipt_page
    Total_Price = 0.0
    return_purchase_receipt_page = tkinter.Tk()
    Item_Array = (Results[0,1]).split(",") #Creates array
    i=0
    for i in range(len(Item_Array)): #For every item in the purchase
        Connection = sqlite3.connect("Inventory.db")
        Cursor = Connection.cursor()
        try:
            Price_Get = '''SELECT Item_Price FROM INVENTORY WHERE Item_ID = (?)
            '''
            #^^^Gathers price
            Cursor.execute(Price_Get, (Item_Array[i],))
            Search_Results = numpy.array(Cursor.fetchall())
            Total_Price = Total_Price + float((str(Search_Results).replace("[","")).replace("]","")) #Adds to total
        finally:
            Connection.close()
        Item_Name_Label = Return_Name_Label(i,Item_Array)
        Item_Price_Label = Return_Price_Label(i,Item_Array)
    Return_Items_Label = tkinter.Label(return_purchase_receipt_page, text = "Return Items:")
    Return_Items_Label.grid(row = 0, column = 0)
    Total_Price_Label = tkinter.Label(return_purchase_receipt_page, text = "Total Price: ")
    Total_Price_Label.grid(row = 2+len(Item_Array), column = 0)
    Total_Price_Label_2 = tkinter.Label(return_purchase_receipt_page, text = str(Total_Price))
    Total_Price_Label_2.grid(row = 2+len(Item_Array), column = 1)
    Return_Proceed_Button = tkinter.Button(return_purchase_receipt_page, text = "Return", command = lambda:[return_purchase_receipt_page.destroy(),Make_Return_Receipt(Item_Array,Total_Price,Results[0,0])])
    Return_Proceed_Button.grid(row = 3+len(Item_Array), column = 0)
    
    return_purchase_receipt_page.mainloop()
    
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@# Admin Page 
    
def ADMIN_MAIN_PAGE_UI():
    global admin_main_page
    admin_main_page = tkinter.Tk()
    Add_User_Label = tkinter.Label(admin_main_page, text = "Add User:")
    Add_User_Label.grid(row = 0, column = 0, columnspan = 2)
    Add_UserName_Label = tkinter.Label(admin_main_page, text = "UserName")
    Add_UserName_Label.grid(row = 1, column = 0)
    Add_UserName_Entry = tkinter.Entry(admin_main_page, width = 75)
    Add_UserName_Entry.grid(row = 1, column = 1)
    Add_Password_Label = tkinter.Label(admin_main_page, text = "Add Password")
    Add_Password_Label.grid(row = 2, column = 0)
    Add_Password_Entry = tkinter.Entry(admin_main_page, width = 75)
    Add_Password_Entry.grid(row = 2, column = 1)
    Add_Confirm_Password_Label = tkinter.Label(admin_main_page, text = "Confirm Password")
    Add_Confirm_Password_Label.grid(row = 3, column = 0)
    Add_Confirm_Password_Entry = tkinter.Entry(admin_main_page, width = 75)
    Add_Confirm_Password_Entry.grid(row = 3, column = 1)
    Add_User_Type_Label = tkinter.Label(admin_main_page, text = "User Type: CUSTOMER/SALES/ADMIN")
    Add_User_Type_Label.grid(row = 4, column = 0)
    Add_User_Type_Entry = tkinter.Entry(admin_main_page, width = 75)
    Add_User_Type_Entry.grid(row = 4, column = 1)
    Add_User_Button = tkinter.Button(admin_main_page, text = "Add User", command = lambda:[Admin_Add_User(Add_UserName_Entry.get(),Add_Password_Entry.get(),Add_Confirm_Password_Entry.get(),Add_User_Type_Entry.get())])
    Add_User_Button.grid(row = 5, column = 0)
    Add_Item_Button = tkinter.Button(admin_main_page, text = "Go to Add Item Page", command = lambda:[admin_main_page.destroy(),ADMIN_ADD_ITEM_UI()])
    Add_Item_Button.grid(row = 0, column = 2)
    Edit_Item_Button = tkinter.Button(admin_main_page, text = "Go to Edit Item Page", command = lambda:[admin_main_page.destroy(),ADMIN_EDIT_ITEM_SEARCH_UI()])
    Edit_Item_Button.grid(row = 1, column = 2)
    Delete_Item_Button = tkinter.Button(admin_main_page, text = "Go to Delete Item Page", command = lambda:[admin_main_page.destroy(),ADMIN_DELETE_ITEM_UI()])
    Delete_Item_Button.grid(row = 2, column = 2)
    Track_Inventory_Button = tkinter.Button(admin_main_page, text = "Track Inventory", command = lambda:[admin_main_page.destroy(),ADMIN_TRACK_INVENTORY_UI()])
    Track_Inventory_Button.grid(row = 3, column = 2)
    Delete_Account_Button = tkinter.Button(admin_main_page, text = "Delete User", command = lambda:[admin_main_page.destroy(),ADMIN_DELETE_ACCOUNT_UI()])
    Delete_Account_Button.grid(row = 4, column = 2)

    admin_main_page.mainloop()
    
def ADMIN_DELETE_ACCOUNT_UI():
    i=0
    global admin_delete_account_page
    admin_delete_account_page = tkinter.Tk()
    Delete_Account_Label_ = tkinter.Label(admin_delete_account_page, text = "Delete an Account: ") # Creates Basket Label
    Delete_Account_Label_.grid(row = 0, column = 0) # Places Label in grid
    Back_Button = tkinter.Button(admin_delete_account_page, text = "Back", command = lambda:[admin_delete_account_page.destroy(),ADMIN_MAIN_PAGE_UI()])
    Back_Button.grid(row = 0, column = 1)
    try:
        Connection = sqlite3.connect("Accounts.db") #Establishes a connection
        Cursor = Connection.cursor() #Creates a cursor
        Accounts_View = ''' SELECT Accounts_UserName FROM ACCOUNTS 
        '''
        #^^^Selects all Accounts
        Cursor.execute(Accounts_View) #Executes the search
        Accounts_All = numpy.array(Cursor.fetchall()) #Retrieves results from search
        Connection.commit()
    finally:
        Connection.close()
        for i in range(len(Accounts_All)): # Creates Labels and Buttons for every entity in the array.
            Display_Delete_Label = Delete_Account_Label(i,Accounts_All) # Triggers Constructor
            Display_Delete_Button = Delete_Account_Button(i,Accounts_All) # Triggers Constructor 
        
    admin_delete_account_page.mainloop() # Begins UI mainloop
    

def ADMIN_DELETE_ITEM_UI():
    i=0
    global admin_delete_items_page # global so widgets can be make in class funcion
    admin_delete_items_page = tkinter.Tk()
    Delete_Items_Label = tkinter.Label(admin_delete_items_page, text = "Delete Items:")
    Delete_Items_Label.grid(row = 0, column = 0, columnspan = 2)
    Back_Button = tkinter.Button(admin_delete_items_page, text = "Back", command = lambda:[admin_delete_items_page.destroy(),ADMIN_MAIN_PAGE_UI()])
    Back_Button.grid(row = 0, column = 3)
    try:
        Connection = sqlite3.connect("Inventory.db") #Establishes a connection
        Cursor = Connection.cursor() #Creates a cursor
        Delete_Name_View = ''' SELECT Item_Name FROM INVENTORY 
        '''
        Delete_ID_View = ''' SELECT Item_ID FROM INVENTORY 
        '''
        #^^^Selects all Item names and ids
        Cursor.execute(Delete_Name_View) #Executes the search
        Delete_Name_All = Cursor.fetchall() #Retrieves results from search
        Cursor.execute(Delete_ID_View) #Executes the search
        Delete_ID_All = Cursor.fetchall() #Retrieves results from search
        for i in range(len(Delete_Name_All)): #Makes labels and buttons for each item in inventory
            Admin_Display_Delete_Label = Delete_Label(i,Delete_Name_All)
            Admin_Display_Delete_Button = Delete_Button(i, Delete_ID_All)
    except sqlite3.Error as error:
        print("Error",error)
    finally:
        Connection.close() #Terminates connection
    
    admin_delete_items_page.mainloop() # Begins UI mainloop
    
def ADMIN_TRACK_INVENTORY_UI():
    global admin_track_inventory_page
    admin_track_inventory_page = tkinter.Tk()
    i = 0
    Track_Inventory_Label = tkinter.Label(admin_track_inventory_page, text = "Item: Quantity")
    Track_Inventory_Label.grid(row = 0, column = 0, columnspan = 2)
    Back_Button = tkinter.Button(admin_track_inventory_page, text = "Back", command = lambda:[admin_track_inventory_page.destroy(),ADMIN_MAIN_PAGE_UI()])
    Back_Button.grid(row = 0, column = 3)
    try:
        Connection = sqlite3.connect("Inventory.db") #Establishes a connection
        Cursor = Connection.cursor() #Creates a cursor
        Inventory_Name_View = ''' SELECT Item_Name FROM INVENTORY 
        '''
        Inventory_Quantity_View = ''' SELECT Item_Quantity FROM INVENTORY
        '''
        #^^^Selects all rnames and quantities in inventory
        Cursor.execute(Inventory_Name_View) #Executes the search
        Inventory_Name_All = Cursor.fetchall() #Retrieves results from search
        Cursor.execute(Inventory_Quantity_View)
        Inventory_Quantity_All = Cursor.fetchall()
        for i in range(len(Inventory_Name_All)): #Makes a label displaying item name and quantity
            Admin_Display_Label = Admin_Label(i,Inventory_Name_All,Inventory_Quantity_All)
    except sqlite3.Error as error:
        print("Error",error)
    finally:
        Connection.close() #Terminates connection

    admin_track_inventory_page.mainloop()

def ADMIN_ADD_ITEM_UI():
    global admin_add_item_page
    admin_add_item_page = tkinter.Tk()
    Add_Item_Label = tkinter.Label(admin_add_item_page, text = "Add_Item:")
    Add_Item_Label.grid(row = 0, column = 0, columnspan = 2)
    Add_Item_Name_Label = tkinter.Label(admin_add_item_page, text = "Item Name: ")
    Add_Item_Name_Label.grid(row = 1, column = 0)
    Add_Item_Name_Entry = tkinter.Entry(admin_add_item_page, width = 75)
    Add_Item_Name_Entry.grid(row = 1, column = 1)
    Add_Item_Type_Label = tkinter.Label(admin_add_item_page, text = "Item Type: ")
    Add_Item_Type_Label.grid(row = 2, column = 0)
    Add_Item_Type_Entry = tkinter.Entry(admin_add_item_page, width = 75)
    Add_Item_Type_Entry.insert(0,"(T-SHIRT,JEANS,SHOES,SHIRT,HAT)")
    Add_Item_Type_Entry.grid(row = 2, column = 1)
    Add_Item_Quantity_Label = tkinter.Label(admin_add_item_page, text = "Item Quantity: ")
    Add_Item_Quantity_Label.grid(row = 3, column = 0)
    Add_Item_Quantity_Entry = tkinter.Entry(admin_add_item_page, width = 75)
    Add_Item_Quantity_Entry.grid(row = 3, column = 1)
    Add_Item_Price_Label = tkinter.Label(admin_add_item_page, text = "Item Price(E.G 10.50): ")
    Add_Item_Price_Label.grid(row = 4, column = 0)
    Add_Item_Price_Entry = tkinter.Entry(admin_add_item_page, width = 75)
    Add_Item_Price_Entry.grid(row = 4, column = 1)
    Add_Item_Offer_Label = tkinter.Label(admin_add_item_page, text = "Offer(0.0-1.0): ")
    Add_Item_Offer_Label.grid(row = 5, column = 0)
    Add_Item_Offer_Entry = tkinter.Entry(admin_add_item_page, width = 75)
    Add_Item_Offer_Entry.grid(row = 5, column = 1)
    Add_Item_Colour_Label = tkinter.Label(admin_add_item_page, text = "Item Colour: ")
    Add_Item_Colour_Label.grid(row = 6, column = 0)
    Add_Item_Colour_Entry = tkinter.Entry(admin_add_item_page, width = 75)
    Add_Item_Colour_Entry.grid(row = 6, column = 1)
    Add_Item_Button = tkinter.Button(admin_add_item_page, text = "Add Item", command = lambda:[Admin_Add_Item(Add_Item_Name_Entry.get(),Add_Item_Type_Entry.get(),Add_Item_Quantity_Entry.get(),Add_Item_Price_Entry.get(),Add_Item_Offer_Entry.get(),Add_Item_Colour_Entry.get())])
    Add_Item_Button.grid(row = 7, column = 0, columnspan = 2)
    Back_Button = tkinter.Button(admin_add_item_page, text = "Back", command = lambda:[admin_add_item_page.destroy(),ADMIN_MAIN_PAGE_UI()])
    Back_Button.grid(row = 0, column = 3)

    admin_add_item_page.mainloop()
    
def ADMIN_EDIT_ITEM_SEARCH_UI():
    global admin_edit_item_page
    admin_edit_item_page = tkinter.Tk()
    Search_Item_Label = tkinter.Label(admin_edit_item_page, text = "Search: ")
    Search_Item_Label.grid(row = 0, column = 0)
    Search_Item_Entry = tkinter.Entry(admin_edit_item_page, width = 75)
    Search_Item_Entry.grid(row = 0, column = 1)
    Search_Item_Button = tkinter.Button(admin_edit_item_page, text = "Search", command = lambda:[ADMIN_EDIT_ITEM_UI(Search_Item_Entry.get())])
    Search_Item_Button.grid(row = 0, column = 2)
    Filler_Column = tkinter.Label(admin_edit_item_page, text = "                           ")# Adds a gap between search and back
    Filler_Column.grid(row = 0, column =3)
    Back_Button = tkinter.Button(admin_edit_item_page, text = "Back", command = lambda:[admin_edit_item_page.destroy(),ADMIN_MAIN_PAGE_UI()])
    Back_Button.grid(row = 0, column = 4)
    
    admin_edit_item_page.mainloop()
    
def ADMIN_EDIT_ITEM_UI(Search_Item):
    Error_Label = tkinter.Label(admin_edit_item_page, text = "")
    Error_Label.grid(row = 9, column = 0)
    if Search_Item != "":
        Connection = sqlite3.connect("Inventory.db")
        Cursor = Connection.cursor()
        try:
            Item_Search = ''' SELECT * FROM INVENTORY WHERE Item_Name = ? OR Item_ID = ?
            '''
            #^^^Searches for item
            Cursor.execute(Item_Search,(Search_Item,Search_Item))
            Connection.commit()
            Item_Details = Cursor.fetchall()
            Formatted_Item_Details = (REMOVE_CHARACTERS_1(Item_Details)).split(",")
        finally:
            Connection.close()
        if str(Formatted_Item_Details) != "['']": #If item exists make labels for all its attributes
            Edit_Item_Label = tkinter.Label(admin_edit_item_page, text = "Edit_Item:")
            Edit_Item_Label.grid(row = 1, column = 0, columnspan = 2)
            Edit_Item_Name_Label = tkinter.Label(admin_edit_item_page, text = "Item Name: ")
            Edit_Item_Name_Label.grid(row = 2, column = 0)
            Edit_Item_Name_Entry = tkinter.Entry(admin_edit_item_page, width = 75)
            Edit_Item_Name_Entry.insert(0,Formatted_Item_Details[1])
            Edit_Item_Name_Entry.grid(row = 2, column = 1)
            Edit_Item_Type_Label = tkinter.Label(admin_edit_item_page, text = "Item Type: ")
            Edit_Item_Type_Label.grid(row = 3, column = 0)
            Edit_Item_Type_Entry = tkinter.Entry(admin_edit_item_page, width = 75)
            Edit_Item_Type_Entry.insert(0,Formatted_Item_Details[2])
            Edit_Item_Type_Entry.grid(row = 3, column = 1)
            Edit_Item_Quantity_Label = tkinter.Label(admin_edit_item_page, text = "Item Quantity: ")
            Edit_Item_Quantity_Label.grid(row = 4, column = 0)
            Edit_Item_Quantity_Entry = tkinter.Entry(admin_edit_item_page, width = 75)
            Edit_Item_Quantity_Entry.insert(0,Formatted_Item_Details[3])
            Edit_Item_Quantity_Entry.grid(row = 4, column = 1)
            Edit_Item_Price_Label = tkinter.Label(admin_edit_item_page, text = "Item Price(E.G 10.50): ")
            Edit_Item_Price_Label.grid(row = 5, column = 0)
            Edit_Item_Price_Entry = tkinter.Entry(admin_edit_item_page, width = 75)
            Edit_Item_Price_Entry.insert(0,Formatted_Item_Details[4])
            Edit_Item_Price_Entry.grid(row = 5, column = 1)
            Edit_Item_Offer_Label = tkinter.Label(admin_edit_item_page, text = "Offer(0.0-1.0): ")
            Edit_Item_Offer_Label.grid(row = 6, column = 0)
            Edit_Item_Offer_Entry = tkinter.Entry(admin_edit_item_page, width = 75)
            Edit_Item_Offer_Entry.insert(0,Formatted_Item_Details[5])
            Edit_Item_Offer_Entry.grid(row = 6, column = 1)
            Edit_Item_Colour_Label = tkinter.Label(admin_edit_item_page, text = "Item Colour: ")
            Edit_Item_Colour_Label.grid(row = 7, column = 0)
            Edit_Item_Colour_Entry = tkinter.Entry(admin_edit_item_page, width = 75)
            Edit_Item_Colour_Entry.insert(0,Formatted_Item_Details[6])
            Edit_Item_Colour_Entry.grid(row = 7, column = 1)
            Edit_Item_Button = tkinter.Button(admin_edit_item_page, text = "Edit Item", command = lambda:[Admin_Update_Item(Formatted_Item_Details[0],Edit_Item_Name_Entry.get(),Edit_Item_Type_Entry.get(),Edit_Item_Quantity_Entry.get(),Edit_Item_Price_Entry.get(),Edit_Item_Offer_Entry.get(),Edit_Item_Colour_Entry.get())])
            Edit_Item_Button.grid(row = 8, column = 1)
        else:
            Error_Label["text"] = "Error: Search Found no results"
    else:
        Error_Label["text"] = "Error: Search cannot be blank"
    
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@# Sales Page
    
def SALES_MAIN_PAGE_UI():
    global sales_main_page
    sales_main_page = tkinter.Tk()
    Track_Inventory_Button = tkinter.Button(sales_main_page, text = "Track Inventory", command = lambda:[sales_main_page.destroy(),SALES_TRACK_INVENTORY_UI()])
    Track_Inventory_Button.grid(row = 0, column = 0)
    
    sales_main_page.mainloop()
    
def SALES_TRACK_INVENTORY_UI():
    global sales_track_inventory_page
    sales_track_inventory_page = tkinter.Tk()
    i = 0
    Track_Inventory_Label = tkinter.Label(sales_track_inventory_page, text = "Item: Quantity")
    Track_Inventory_Label.grid(row = 0, column = 0, columnspan = 2)
    Back_Button = tkinter.Button(sales_track_inventory_page, text = "Back", command = lambda:[sales_track_inventory_page.destroy(),SALES_MAIN_PAGE_UI()])
    Back_Button.grid(row = 0, column = 3)
    try:
        Connection = sqlite3.connect("Inventory.db") #Establishes a connection
        Cursor = Connection.cursor() #Creates a cursor
        Inventory_Name_View = ''' SELECT Item_Name FROM INVENTORY 
        '''
        Inventory_Quantity_View = ''' SELECT Item_Quantity FROM INVENTORY
        '''
        #^^^Selects all names and quantities in inventory
        Cursor.execute(Inventory_Name_View) #Executes the search
        Inventory_Name_All = Cursor.fetchall() #Retrieves results from search
        Cursor.execute(Inventory_Quantity_View)
        Inventory_Quantity_All = Cursor.fetchall()
        for i in range(len(Inventory_Name_All)):
            Sales_Display_Label = Sales_Label(i,Inventory_Name_All,Inventory_Quantity_All)
    except sqlite3.Error as error:
        print("Error",error)
    finally:
        Connection.close() #Terminates connection

    sales_track_inventory_page.mainloop()


########################################################################## Formating inputs

def REMOVE_CHARACTERS(String):
    New_String = (String.replace("[","")).replace("]","")
    return New_String
def REMOVE_CHARACTERS_1(String):
    New_String = (((((str(String).replace("[","")).replace("]","")).replace("(","")).replace(")","")).replace(" ","")).replace("'","")
    return New_String
def REMOVE_CHARACTERS_2(String):
    New_String_1 = (String.replace("[",""))
    New_String_2 = (New_String_1.replace("(",""))
    New_String_3 = (New_String_2.replace(")",""))
    New_String_4 = (New_String_3.replace("]",""))
    return New_String_4
def REMOVE_CHARACTERS_3(String):
    New_String = ((String.replace("[","")).replace("]","").replace("'","")).replace(" ","")
    return New_String

######################################################################## Main Code

Establish_Accounts()
Establish_Basket()
Establish_Inventory()
Establish_Purchases()
Establish_Returns()
LOGIN_UI()