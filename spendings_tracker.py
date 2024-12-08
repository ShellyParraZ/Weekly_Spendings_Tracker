""" This program will provide an in-depth analysis on your weekly spendings.
The apps target audience are college students.

Driver/Navigator: Shelly Parra
Assignment: Final Project
Date: 12/09/2024

Challenges Encountered: Understanding databases and fixing errors.

"""


import csv
import sqlite3
import os
import pandas as pd


class Week:
    """ A weekly tracker of the users spendings. 
    
    Attributes:
        database_conn (connection): The connection to the database.
        self.cursor (cursor): To manipulate the database.
        self.weekly_tuition_perc (float): The weekly percentage of money spent on tuition.
        self.weekly_rent_perc (float): The weekly percentage of money spent on rent.
        self.weekly_utilities_perc (float): The weekly percentage of money spent on utilities.
        self.starting_amount (float): The amount of money the user has at the beginning of the week.
        self.want_spendings_perc (float): The percentage of spendings on total wants.
        self.need_spendings_perc (float): The percentage of spendings on total needs.
        self.total_spendings (float): The total amount of spendings, specifically the wants and needs.
        self.total_want_spendings (float): The total amount of spendings on wants.
        self.total_need_spendings (float): The total amount of spendings on needs.
        self.windfall (float): The amount of money the user unexpectedly gathered.
        self.overdraft (float): The amount of money the user used past their spendings amount and windfall.
        self.remaining_balance (float): The amount of money the user has left after substracting from starting amount.
    
    """
    
    
    def __init__(self, database_conn):
        
        self.database_conn = database_conn
        self.cursor = database_conn.cursor() # used to create queries
        
        # create table query
        cq = f'''CREATE TABLE week (
                priority_type TEXT, category TEXT, name TEXT NULL, cost FLOAT NULL
                )'''
        self.cursor.execute(cq) # creates table
            
            
    def insert_data(self, file_path):
        """ Inserts the data from the file to the table.
        
        Attributes:
            file_path (str): The file path.
        
        Special Effects:
            Each row in the file is implemented into the week table.
        
        """
        
        with open(file_path, 'r', encoding = 'utf-8') as csv_file: # to read the file
            csv_reader = csv.reader(csv_file, delimiter = ',') # object, the comma is default
            
            next(csv_reader, None) # skips the header
            
            # convert to list
            file_list = list(csv_reader)
            
            data = [] # empty list that will get populated by the data inside the csv
            
            for row in file_list: # adds all the data to the list
                data.append(row)
                
            imq = f'''INSERT INTO week VALUES(?,?,?,?)'''
            self.cursor.executemany(imq, data) # inserts the data      
            
            self.database_conn.commit() # commits changes 
            
    
    def retrieve_analysis(self, weekly_info):
        """ Based on all the data gathered, an analysis is provided.
        
        Attributes:
            weekly_info (dict): Containing the weekly salary, tuition, rent, and utilities.
            
        Special Effects:
            Using the week table, different variations of information is collected an assigned a variable.
        
        """
        
        # percentage version
        # a ZeroDivisonError could occur if the income is 0.0
        if weekly_info["Income"] == 0.0:
            self.weekly_tuition_perc = 0.0
            self.weekly_rent_perc = 0.0
            self.weekly_utilities_perc = 0.0
        else:
            self.weekly_tuition_perc = round((weekly_info["Tuition"] / weekly_info["Income"]) * 100.0, 2)
            self.weekly_rent_perc = round((weekly_info["Rent"] / weekly_info["Income"]) * 100.0, 2)
            self.weekly_utilities_perc = round((weekly_info["Utilities"] / weekly_info["Income"]) * 100.0, 2)
                
        # the amount of money that is left after considering the unavoidable financial payments
        self.starting_amount = round(weekly_info["Income"] - (weekly_info["Tuition"] + weekly_info["Rent"] + weekly_info["Utilities"]), 2)

        # locate the "Windfall" in priority type column, then add the costs in those rows
        sq1 = '''SELECT SUM(cost) FROM week WHERE priority_type = "Windfall"'''
        self.cursor.execute(sq1)
        t = self.cursor.fetchone() # the sum of the windfall
        self.windfall = round(t[0], 2) # get the float from the tuple
        
        # calculate the total spendings by finding the sums of all the rows, except windfall
        sq2 = '''SELECT SUM(cost) FROM week WHERE priority_type != "Windfall"'''
        self.cursor.execute(sq2)
        t = self.cursor.fetchone()
        self.total_spendings = round(t[0], 2) # get the float from the tuple
        
        # locate the "Want" in priority type column, then add the costs in those rows
        sq3 = f'''SELECT SUM(cost) FROM week WHERE priority_type = "Want"'''
        self.cursor.execute(sq3)
        t = self.cursor.fetchone()
        self.spending_wants = round(t[0], 2) # get the float from the tuple
        
        # get the want percentage
        self.want_spendings_perc = round((self.spending_wants / self.total_spendings) * 100.0, 2)
        
        # locate the "Need" in priority type column, then add the costs in those rows
        sq4 = f'''SELECT SUM(cost) FROM week WHERE priority_type = "Need"'''
        self.cursor.execute(sq4)
        t = self.cursor.fetchone()
        self.spending_needs = round(t[0], 2) # get the float from the tuple
        
        # get the need percentage
        self.need_spendings_perc = round((self.spending_needs / self.total_spendings) * 100.0, 2)
        
        # get the overdraft and remaining balance
        overdraft_balance = round((self.starting_amount + self.windfall) - self.total_spendings, 2)
        if overdraft_balance < 0.0:
            self.overdraft = overdraft_balance * -1.0
            self.remaining_balance = 0.0
        else:
            self.overdraft = 0.0
            self.remaining_balance = overdraft_balance
        
        
    def category_analysis(self, category):
        """ Calculates the percentage of each category.
        
        Attributes:
            category (str): A category from the Week database.
        
        Special Effects:
            Prints the categories with their percentages.
        
        """
        
        sq = f'''SELECT SUM(cost) FROM week WHERE category = ?'''
        self.cursor.execute(sq, (category,))
        t = self.cursor.fetchone() # get the float from the tuple
        category_cost = t[0] if t[0] is not None else 0.0
        
        # check if total_spendings is 0.0 to avoid an error
        if self.total_spendings == 0.0:
            percent = 0.0
        else:
            percent = round((category_cost / self.total_spendings) * 100.0, 2)
        
        print(f"\t{category}: {percent}%")
        
        
    def name_analysis(self, names_cost):
        """ Calculates the percentage of each name in the dictionary.
        
        Attributes:
            names_cost (dict): The names with their cost. The name is the key and the cost is the value.
            
        Special Effects:
            Prints the names with their percentages.
        
        """
        
        print()
        print("Thorough Name Analysis")
        
        for key in names_cost:  
            # check if total_spendings is 0.0 to avoid an error
            if self.total_spendings == 0.0:
                percent = 0.0
            else:
                percent = round((names_cost[key] / self.total_spendings) * 100.0, 2)
                print(f"\t{key}: {percent}%")
        
        print()
        
        
    def __repr__(self):
        """ Prints out all the information gathered regarding the week.
        
        Side Effects:
            All the data is structured and organized to get printed.
        
        """
        
        print()
        print("Weekly Summary")
        print("-----------------------------------------------------------")
        print(f"Starting Amount: ${self.starting_amount}")
        print(f"Remaining Balance: ${self.remaining_balance}")
        print(f"Overdraft: ${self.overdraft}")
        print(f"Windfall: ${self.windfall}")
        print(f"Weekly Tuition Percentage: {self.weekly_tuition_perc}%")
        print(f"Weekly Rent Percentage: {self.weekly_rent_perc}%")
        print(f"Weekly Utilities Percentage: {self.weekly_utilities_perc}%")
        print(f"Total Spendings: ${self.total_spendings}")
        print()
        print(f"Spending Wants:")
        print(f"\tTotal: ${self.spending_wants}")
        print(f"\tSpending Percentage: {self.want_spendings_perc}%")
        print()
        print(f"Spending Needs:")
        print(f"\tTotal: ${self.spending_needs}")
        print(f"\tSpending Percentage: {self.need_spendings_perc}%")
        print()
    

def weekly_calculation(yearly_values):
    """ Calculate the weekly income, tuition, rent, and utilities based on the users yearly submission.
    
    Attribute:
        yearly_values (tuple): the yearly income, tuition, rent, utilities.
    
    Returns:
        general_info (dict): A dictionary of the weekly income, tuition, rent and utilities.
    
    """
    general_info = {}
    
    for index, item in enumerate(yearly_values):
        
        updated_item = (item / 12) / 4
        
        if index == 0:
            general_info["Income"] = updated_item
        elif index == 1:
            general_info["Tuition"] = updated_item
        elif index == 2:
            general_info["Rent"] = updated_item
        else:
            general_info["Utilities"] = updated_item
    
    return general_info


def general_info():
    """ Collecting general information regarding the user.
    
    Returns:
        A tuple containing the general information.
    
    """
    
    while True: 
        yearly_income = retrieve_float("Input your yearly income: ")
        yearly_tuition = retrieve_float("Input your yearly tuition: ")
        yearly_rent = retrieve_float("Input your yearly rent: ")
        yearly_utilities = retrieve_float("Input your yearly utilities: ")
        
        print("These are your current responses:")
        print(f"Yearly Income: {yearly_income}")
        print(f"Tuition: {yearly_tuition}")
        print(f"Rent: {yearly_rent}")
        print(f"Utilities: {yearly_utilities}")
        restart = input("Would you like to change a response? (enter \"no\" to continue) ")
        if restart == "no":
            return yearly_income, yearly_tuition, yearly_rent, yearly_utilities


def retrieve_float(prompt):
    """ Insures the user is providing a float.
    
    Returns:
        response (float): The response to the prompt.
    
    """
    
    while True:
        try:
            response = float(input(prompt))
            if response >= 0.0:
                return response
            print("Negative value. Please enter a positive float.")
        except ValueError: # not a float
            print("Incorrect value. Please enter a float.")


def main():
    """ Prompts the user for general information. Handles the overall program.
    
    Attributes:
        week (obj): Object of Week class.
    
    """
    
    print("Hello! This is the Weekly Spendings Tracker.")
    print("In order to provide a significant analysis, please provide your yearly income, tuition, rent, and utilities.")
    print("These values should be a positive float. Otherwise, input 0.0.")
    info = general_info() # a tuple
    print("Your information was successfully saved.")
    
    # calculate the weekly amount of the users general information
    weekly_info = weekly_calculation(info) # a dictionary
    
    # create a database to collect the information in the csv files
    conn = sqlite3.connect('week.db')
    
    # create a class that will collect all the information
    week = Week(conn)
    
    # go through the files in your folder
    folder_path = input("Provide the name of your weekly spendings folder: ")
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            
            # use pandas
            # check if the file is empty
            try:
                pd.read_csv(f"{folder_path}\\{file}")
                week.insert_data(f"{folder_path}\\{file}")
            except pd.errors.EmptyDataError:
                print("Empty File Located.")
                
    week.retrieve_analysis(weekly_info)
    
    # print the basic information by using repr
    week.__repr__()
        
    # thorough category analysis
    print("Thorough Category Analysis")
    categories = ["Dining Out Food", "Groceries", "Personal Care", "Gardening Supplies", "Clothing", 
                  "Household Items", "Technology", "Entertainment", "Health & Fitness", "Gifts", 
                  "School Resources", "Work Resources", "Pet Care", "Other"]
    for category in categories:
        week.category_analysis(category)
    
    # thorough name analysis
    sq = """SELECT name FROM week WHERE priority_type != "Windfall" """ # grabs all the names
    week.cursor.execute(sq)
    name_list = week.cursor.fetchall() # a list of tuples that contain one element
    
    name_with_cost = {}
    for name in name_list:
        sq = f'''SELECT SUM(cost) FROM week WHERE name = ?'''
        week.cursor.execute(sq, (name[0],))
        t = week.cursor.fetchone() # get the float from the tuple
        cost = t[0] if t[0] is not None else 0.0 # provides the cost of the name
        name_l = name[0].title() # change to title to elimiate duplicates that are different letter cases
        if name_l in name_with_cost: # the name exists in the dictionary
            name_with_cost[name_l] = name_with_cost[name_l] + cost
        else:
            name_with_cost[name_l] = cost
    
    # call a method that will determine the percentages
    week.name_analysis(name_with_cost)
    
    # After collecting and printing all the information, close the database connection
    conn.close()


if __name__ == "__main__":
    main()