# Write your code to expect a terminal of 80 characters wide and 24 rows high
#Every input method needs a \n at the end of the text to work in heroku
import gspread
from google.oauth2.service_account import Credentials

"""
Section facilitates API use to update user stats in 
google sheets
"""

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('adventurer')

adventurer = SHEET.worksheet('Adventurer')
print(adventurer.row_values(1))

"""
Methods for initial set-up and player creation
"""

class Player:
    def __init__(self, name, height, sex, gold=10):
        self.name = name
        self.height = height
        self.sex = sex
        self.gold = gold

    def show_stats(self):
        print(f"Name: {self.name}")
        print(f"Height: {self.height}")
        print(f"Sex: {self.sex}")
        print(f"Gold: {self.gold} pieces")

# Player creation process from user input
name = input("Enter your character's name: \n")
height = input("Enter your character's height: \n")
sex = input("Enter your character's sex: \n")

player = Player(name, height, sex)
player.show_stats()