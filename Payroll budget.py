# Create a program that can calculate the hours allocated to payroll at a X store.
# The goal will be to be able to punch in the number of planned hours for the week for each employee,
# and the total real sales month to date and year to date in order to calculate what the store is tracking.
# This is because this particular company calculates payroll as a percent of sales.
# for example: if the store had a strong couple of months and for some reason it was having a slow month.
# the program will be able to take in to account previous performance , and advice the user as to how many hours
# to add or to cut.


import json


# name and hourly rate for each team member.
def get_team():
    return [['Greg ', 17.5],
            ['Ashley ', 16.5],
            ['Sydney ', 14],
            ['Denise ', 14],
            ['Stetson ', 15.5],
            ['Alyssa The Rat ', 14.5]]


# takes in all rates and returns an average.
def ave_hour_cost():
    name_and_rate = get_team()
    rates = [item[1] for item in name_and_rate]
    rate_sum = sum(rates)
    number_of_employees = len(rates)
    average_rate = rate_sum / number_of_employees
    return average_rate
    print('')


# Takes in all the hours the team will work and returns a total cost.
def labor_cost():
    total_costs = float(0)
    name_and_rate = get_team()
    rates = [item[1] for item in name_and_rate]
    names = [item[0] for item in name_and_rate]

    for name in names:
        hours = float(input("how many hours will " + name + "work? "))
        single_cost = int((rates.pop(0) * hours))
        total_costs += single_cost
        print("")

    return total_costs


def month_config(user_month):
    month_list = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']

    return month_list[user_month]


# Creates a save file that adds the monthly variance to a running yearly variance.
def yearly_running_variance(run_result, variance1):
    update = input('Do you want to update the running variance? (y)es or (n)o ')
    print('')
    variance = float(variance1)
    if 'y' == update.lower():
        variance += float(run_result)
        filename = 'variance.json'

        with open(filename, 'w') as f_obj:
            json.dump(variance, f_obj)
            print('The new running variance is: ' + '{:,.2f}'.format(variance))

    else:
        zero_out = input('Do you want to reset the running total to Zero?  (Y)es or (N)o ')
        print('')

        if 'y' == zero_out.lower():
            variance = 0
            filename = 'variance.json'
            with open(filename, 'w') as f_obj:
                json.dump(variance, f_obj)
                print('The running variance has been set to ' + '{:,.2f}'.format(variance))
                print('')
        else:
            print('The running variance will remain to be ' + '{:,.2f}'.format(variance))


# Loads the yearly running variance.
def load_variance():
    filename = 'variance.json'

    with open(filename) as f_obj:
        variance1 = json.load(f_obj)
        return variance1


# Calculates the payroll budget based on corporate give percentages, and hours give by the user.
def corp_plan_payroll(t_cost):

    average_hour_cost = ave_hour_cost()

    payroll_budget = dict(January=.14, February=.107, March=.127, April=.127, May=.093, June=.121, July=.121,
                          August=.123, September=.121, October=.114, November=.08, December=.061)

    for month, value in payroll_budget.items():
        if month_config(user_month) == month:
            avg_wkly_pr = int((value * month_to_date_sales) / week_of_month)
            print('The average weekly budget vs sales for the month of ' + month_config(user_month) +
                  ' is ' + '${:,.2f}'.format(avg_wkly_pr) + '.')
            print('')

            if avg_wkly_pr < t_cost:
                over_by = t_cost - avg_wkly_pr
                hours_to_cut = over_by / average_hour_cost
                print('You are currently over corporate budget by ' + '${:,.2f}'.format(over_by) + '.')
                print('')
                print('To get payroll back in line, try to cut ' + '{:,.2f}'.format(hours_to_cut) + ' hours')
                print('')
                neg_hours_to_cut = '{:,.2f}'.format(-hours_to_cut)

                return neg_hours_to_cut

            elif avg_wkly_pr > t_cost:
                under_by = avg_wkly_pr - t_cost
                hours_to_add = under_by / average_hour_cost
                print('You are currently under corporate budget by ' + '${:,.2f}'.format(under_by) + '.')
                print('')
                print('To get payroll back in line, try to add ' + '{:,.2f}'.format(hours_to_add) + ' hours')
                print('')
                return hours_to_add


month_to_date_sales = int(input('What is the total store sales for this month? '))
print('${:,.2f}'.format(month_to_date_sales))
user_month = int(input('Enter the corporate month as a number. '))
user_month = user_month - 1
print(month_config(user_month))
week_of_month = int(input('What is the week of the month for this month? '))
print('')
t_cost = labor_cost()
print('The total labor cost for this week will be: ' + '${:,.2f}'.format(t_cost))
print('')
variance1 = load_variance()
run_result = corp_plan_payroll(t_cost)
yearly_running_variance(run_result, variance1)

