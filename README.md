# Weekly_Spendings_Tracker
This program will provide prompts and generate calculations based on the users weekly spendings. Ultimately an analysis of the users weekly spendings will be provided.

CALCULATIONS

Weekly Summary
  The weekly summary is part of the f-string that is developed in the weekly_summary method.
  f“Weekly Summary”

Starting Amount
  The starting amount is a float. This is the amount of money the user is starting with. This should not change. 
  In order to determine this variable, the tuition, yearly_salary, rent, and utilities must be converted to weekly variables, by dividing by twelve months, then four weeks.   After those calculations, then the weekly_tuition, weekly_rent, and weekly_utilities should get subtracted from the weekly_salary. 
  weekly_tuition = 0.00 / 12 = 0.00 / 4 = 0.00
  weekly_rent = 20400.00 / 12 = 1700 / 4 = 425
  weekly_utilities = 64.53 / 12 = 5.38 / 4 = 1.35
  weekly_salary = 31200.00 / 12 = 2600.00 / 4 = 650.00
  self.starting_amount = 650.00 - (0.00 + 425 + 1.35) = 223.65
  self.starting_amount = weekly_salary - (weekly_tuition + weekly_rent + weekly_utilities)
  f”Starting Amount: ${self.starting_amount}”

Remaining Balance
  The remaining balance is a float. This is the amount of money the user has left. This cannot be negative. The lowest amount this will be is zero. In other words, the default is zero. If this variable becomes negative, the amount will get saved in overdraft, then be set to zero.
  In order to determine this variable, all the spending calculations must be determined. If there is money remaining, then that will be added to this variable.
  This variable will be initialized by the starting_amount variable. As spendings are calculated, this amount will change. This amount increases if there is a windfall amount discovered in the csv files.
  self.remaining_balance = starting_amount
  self.remaining_balance = self.remaining_balance - self.total_spendings
  self.remaining_balance = self.remaining_balance + self.windfall
  f”Remaining Balance: ${self.remaining_balance}”

Overdraft
  The overdraft is a float. This is the amount of money the user owes. Otherwise known as the negative balance. The lowest amount this will be is zero. In other words, the default is zero.
  self.overdraft = self.remaining_balance
  f”Overdraft: ${self.overdraft}”

Windfall
  The windfall is a float. This is the amount of money the user unexpectedly gathered, such as winning the lottery. The lowest amount this will be is zero. In other words,  the default is zero.
  In order to determine this variable, when searching the csv files, if there are rows that contain the keyword: windfall, then that amount will be added to this variable.
  This amount will be automatically added to the remaining_balance. If the user does not want to add this amount to the remaining_balance, then they should just not include   it into the system. Otherwise, the system assumes they are trying to save the amount.
  self.windfall = 50
  f”Windfall: ${self.windfall}

Weekly Tuition Percentage
  The weekly tuition percentage is a float. This is the weekly percentage of money spent on tuition.
  In order to determine this variable, the weekly_tuition is divided by the weekly_salary, then multiplied by one-hundred to get the percent.
  self.weekly_tuition_perc = self.weekly_tuition / self.weekly_salary = amount * 100 = amount%
  self.weekly_tuition_perc = 0.00 / 650.00 = 0.00 * 100 = 0.00%
  f”Weekly Tuition Percentage: {self.weekly_tuition_perc}”

Weekly Rent Percentage
  The weekly rent percentage is a float. This is the weekly percentage of money spent on rent.
  In order to determine this variable, the weekly_rent is divided by the weekly_salary, then multiplied by one-hundred to get the percent.
  self.weekly_rent_perc = self.weekly_rent / self.weekly_salary = amount * 100 = amount%
  self.weekly_rent_perc = 425 / 650.00 = 0.6538 * 100 = 65.38%
  f”Weekly Rent Percentage: {self.weekly_rent_perc}”

Weekly Utilities Percentage
  The weekly rent percentage is a float. This is the weekly percentage of money spent on rent.
  In order to determine this variable, the weekly_rent is divided by the weekly_salary, then multiplied by one-hundred to get the percent.
  self.weekly_utilities_perc = self.weekly_rent / self.weekly_salary = amount * 100 = amount%
  self.weekly_utilities_perc = 1.35 / 650.00 = 0.0021 * 100 = 0.21%

Total Spendings
  The total spendings is a float. This is the total amount of money the user spent in a week. This amount will never be negative. This does not consider the rent, utilities, or tuition. Strictly considering the wants/needs spendings.
  f”Total Spendings {self.total_spendings}”

Spending Wants
  The spending wants is a f-string. This is the amount of money that was spent on items that were labeled a want by the user. A want is referring to an item that is not essential. For example, a cup of coffee from Dunkin’ Donuts is not essential.
  In order to determine the total, the csv files will be examined. Every item that is labeled as “want” will get added to the total of spending wants. After gathering all the items, then the percentage will be calculated by dividing the total by the starting_amount, and then multiplying by one-hundred.
  self.spending_wants += each item
  self.spendings_wants_perc = (self.spending_wants / self.total_spendings) * 100
  f”Spending Wants:
			Total: {self.total_want_spendings}
			Wants Spending Percentage: {self.want_spendings_perc}%”

Spending Needs
  The spending needs is a f-string. This is the amount of money that was spent on items that were labeled as a need by the user. A need is referring to an item that is essential. For example, a required textbook for a college class is essential.
  In order to determine the total, the csv files will be examined. Every item that is labeled as “need” will get added to the total of spending needs. After gathering all the items, then the percentage will be calculated by dividing the total by the starting_amount, and then multiplying by one-hundred.
  self.spending_needs += each item
  self.spendings_needs_perc = (self.spending_needs / self.total_spendings) * 100
  f”Spending Needs:
			Total: {self.total_need_spendings}
			Needs Spending Percentage: {self.need_spendings_perc}%”

Thorough Category Analysis
  The thorough analysis is f-string. This analysis will provide percentages of the categories the user places each name in. 

Thorough Name Analysis
  The thorough name analysis is f-string. The thorough name analysis will provide the percentages of every item in regards to the starting amount.
  In order to determine the percentages for each item, every item's total amount will be divided by the starting amount and then multiplied by one-hundred.
  f”Thorough Name Analysis
      Name: %
      Name: %”


EXAMPLE OUTPUT

A file containing this information:

Weekly Summary

Starting Amount: $223.65
Remaining Balance: $0.00
Overdraft: $41.52
Windfall: $50.00
Weekly Tuition Percentage: 0.00%
Weekly Rent Percentage: 65.38%
Weekly Utilities Percentage: 0.21%
Total Spendings: $ 315.17

Spending Wants:
	Total: $169.57
	Spending Percentage: 53.80%

Spending Needs:
	Total: $145.6
Spending Percentage: 46.2%

Thorough Category Analysis
	Dining Out Food: %
	Groceries: %
	Personal Care: %
	Gardening Supplies: %
	Clothing: %
	Household Items: %
	Technology: %
	Entertainment: %
	Health & Fitness: %
	Gifts: %
	School Resources: %
	Work Resources: %
	Pet Care: %
	Other: %
	Windfall: %

Thorough Name Analysis
inst327 textbook: 18.28%
	coffee: 9.49%
	groceries: 21.58%
	clothes: 24.16%
	movie tickets: 5.44%
	squishmallow: 7.93%
	dog food: 6.34%
	lunch: 6.79%

