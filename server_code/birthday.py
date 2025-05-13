import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from datetime import datetime


'''MODIFY TO MAKE FIT THE SCHEMA OF NEW USERS TABLE
birth_month
birth_day
birth_date_text


NOT MAKING GENERIC JUST YET, JUST SEE IF THE COMPONENT CAN BE USED
Requires the Users table to have the following fields:
birth_month - number
Name - text
birth_date - number

Test if no 'Birthday' field, just do date printout.

'''


@anvil.server.callable
def get_this_month_birthdays():
  print('get_birthdays_called')
  now_time = datetime.now()
  month = now_time.month
  month_text = now_time.strftime("%b")
  birthday_list = app_tables.users.search(tables.order_by("birth_day", ascending=True), birth_month=month)
  birthday_text = ''

  if birthday_list:
    birthday_text = 'Birthdays this month: \n'
    for player in birthday_list:
      if player['enabled']:               
        birthday_text += f"{player['first_name']} {player['last_name']}: {month_text} {player['birth_day']} \n"

    return birthday_text

    def convert_date_to_text(month, day):
      months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
      suffixes = {1: "st", 2: "nd", 3: "rd"}
      suffix = suffixes.get(day if day < 20 else day % 10, "th")
      return f"{months[month - 1]} {day}{suffix}"