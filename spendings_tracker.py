""" This program will track your weekly spendings. It will automatically submit a summary by the
beginning of each Sunday. The apps target audience are college students.

Driver/Navigator: Shelly Parra
Assignment: Check-in 2
Date: 10/27/2024

Challenges Encountered: 

"""

# whenever a user inputs a description 
# that is similar to a previous submission, then it will add to the previous submission.
# For example, I add "coffee, $5.00", then later "CoFFee, $2,50". The dictionary will update the previous
# submission to "coffee, $7.50". All the dictionary descriptions will be lowercase.


import datetime
import sys
import argparse
import csv
# allow the user to input the date they want the report?

class Week:
    """ A weekly tracker of the users spendings. It will provide a report of the previous week on Sundays.
    
    Attributes:
        daily_spendings (dict): a dictionary containing the daily spendings of the user.
        self.date (date): The date of the sunday of the week.
        self.weekly_tuition_perc (float): The weekly percentage of money spent on tuition.
        self.weekly_rent_perc (float): The weekly percentage of money spent on rent.
        self.weekly_utilities_perc (float): The weekly percentage of money spent on utilities.
        self.starting_amount (float): The amount of money the user has at the beginning of the week.
        self.want_spendings_perc (float): The percentage of spendings on total wants.
        self.need_spendings_perc (float): The percentage of spendings on total needs.
    
    """
    
    
    def __init__(self, daily_spendings, yearly_salary = 0.00, tuition = 0.00, rent = 0.00, utilities = 0.00):
        
        self.daily_spendings = []
        self.daily_spendings.append(daily_spendings) # a full week, each weekday is a tuple with two dictionaries
        self.date = datetime.date.today() # the current date
        
        # weekly versions of the yearly_salary, tuition, rent, and utilities
        self.weekly_salary = (yearly_salary / 12) / 4
        self.tuition = (tuition / 12) / 4
        self.rent = (rent / 12) / 4
        self.utilities = (utilities / 12) / 4
        
        # percentage version
        self.weekly_tuition_perc = (self.tuition / self.weekly_salary) * 100
        self.weekly_rent_perc = (self.rent / self.weekly_salary) * 100
        self.weekly_utilities_perc = (self.utilities / self.weekly_salary) * 100
        
        self.starting_amount = self.weekly_salary - (self.tuition + self.rent + self.utilities)
        
        # percentage of wants and needs
        self.want_spendings_perc = (self.total_want_spendings / self.total_spendings) * 100
        self.need_spendings_perc = (self.total_need_spendings / self.total_spendings) * 100
        
        # might have to do this in if name == "main"
        if datetime.date(self.date).weekday() == 6 and len(self.daily_spendings) == 7: # sunday and all seven days are included
            # call a method that will add all the information within the dictionaries
            thorough_analysis(self.daily_spendings)
            
            
    def thorough_analysis(self):
        """ Combines the information in the dictionaries in order to provide thorough analysis of
        wants and needs. In otherwords, combines duplicates.
        
        Returns:
            self.remaining_balance (float): The amount of money that remains after the spendings are subtracted.
            self.overdraft (float): The amount of money the user owes. Gets updated if the remaining balance is negative.
        
        """
        
        # create a dictionary that will have all the combined information
        dict_summary = {}
        
        # delete all the empty strings that represent the empty days
        updated_daily_spend = [x for x in self.daily_spendings if x != "empty"]
        
        # Combine the value of all the keys that contain the same name
        for day in updated_daily_spend: # day = tuple
            for dict in day: # for each dictionary in the tuple
                for key in dict: # for each key in dictionary
                    if dict_summary.get(key, False) == False: # if False, then key does not exist
                        dict_summary[key] = updated_daily_spend[key]
                    else: # the key already exists, so add the previous value to the current value
                        dict_summary[key] = dict_summary[key] + updated_daily_spend[key]
        
        # self.remaining_balance: needs to be determined after adding the 
        
        
    def __repr__(self):
        """ Prints out all the information gathered regarding the week.
        
        """
        
        print("Weekly Summary")
        print()
        print(f"Date: {self.date}")
        print()
        
        pass


class Day: # what relationship would this have with the other class, maybe composition?
    """ Every day in a week. It will collect the information for each individual day.
    
    Attributes:
        self.total_spendings (float): The total amount of spendings, specifically the wants and needs.
        self.total_want_spendings (float): The total amount of spendings on wants.
        self.total_need_spendings (float): The total amount of spendings on needs.
        self.windfall (float): The amount of money the user unexpectedly gathered.
    
    """
    
    # We need to collect the file and then get all the information.
    
    def __init__(self, journal_file_path):
        
        self.journal_file_path = journal_file_path
        self.total_spendings = 0.00
        self.total_want_spendings = 0.00
        self.total_need_spendings = 0.00
        self.windfall = 0.00
            
    
    def parsed_file(self):
        """ Creates two dictionaries for each day of the week.
        
        Attributes:
            self.windfall (float): The amount of money the user unexpectedly gathered.
        
        Returns:
            A tuple with two dictionaries. The first element in the tuple is a dictionary of the spending wants and
            the second element in the tuple is a dictionary of the spending needs.
        
        """
        # a database would store their information overtime!!!
        # allows you to import their information as a table
        # like columns  (want, need, windfall)
        # to access later, you'd query the database
        # DATABASES!!!
        
        # open the csv file
        with open(self.journal_file_path, 'r', encoding = 'utf-8') as csv_file: # to read file
            file_reader = csv.reader(csv_file)
            
            # convert to list
            file_list = list(file_reader)
            
            # check if list is empty
            if not file_list: # list is empty
                return "empty"
            
            # the dictionary that will be returned
            weekday_dict_wants = {}
            weekday_dict_needs = {}
            
            for line in file_list:
                if line[0].lower() == "want":
                    weekday_dict_wants[line[1].lower()] = float(line[2])
                    self.total_want_spendings += float(line[2])
                elif line[0].lower() == "need":
                    weekday_dict_needs[line[1].lower()] = float(line[2])
                    self.total_need_spendings += float(line[2])
                else:
                    self.windfall += float(line[2])
                    
                self.total_spendings += float(line[2])
            
        return weekday_dict_wants, weekday_dict_needs
    

def parse_args(args_list):
    """ Allows user to input their csv file, yearly salary, tuition, rent, and utilities.
    
    Attributes:
        args_list (list[str]): A list of strings containing the command-line arguments for the program.
    
    Returns:
        The parsed arguments object.
        
    """
    
    # initialize the parser
    parser = argparse.ArgumentParser(description = 'Provide your csv file, yearly salary, tuition, rent, and utilities. Do not use the dollar sign.')
    
    # add the arguments
    parser.add_argument('csvFile', type = str, help = 'input your csv file')
    parser.add_argument('yearlySalary', type = float, help = 'input your yearly salary')
    parser.add_argument('tuition', type = float, help = 'input your yearly tuition')
    parser.add_argument('rent', type = float, help = 'input your yearly rent')
    parser.add_argument('utilities', type = float, help = 'input your yearly utilities')
    
    return parser.parse_args(args_list)


if __name__ == "__main__":
    
    week_obj = Week()
    args = parse_args(sys.argv[1:]) # contains two arguments
    
    day = Day(args.csvFile)
    want_need_tuple = day.parsed_file()
    
    week_obj(want_need_tuple, args.yearlySalary, args.tuition, args.rent, args.utilities)