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

"""
Methods for initial set-up and player creation
"""

class Player:
    def __init__(self, name, height, sex, gold=10):
        """
        Player constructor
        """
        self.name = name
        self.height = height
        self.sex = sex
        self.gold = gold

    def get_name(self):
        """
        Name validation to ensure only letters are input
        """
        while True:
            name = input("Enter your character's name (letters only): \n")
            if name.isalpha():
                return name
            else:
                print("Invalid name, please use letters only")

    def get_height(self):
        """
        Height validation to ensure users input only from the three
        options
        """
        while True:
            valid_heights = ["tall", "short", "average"]
            height = input("Enter your character's height (short, average, tall): \n").lower()
            if height in valid_heights:
                return height
            else:
                print("Invalid height, please enter short, average or tall.")

    def get_sex(self):
        """
        Sex validation to ensure users input only from the three
        options
        """
        while True:
            sexes = ["male", "female", "other"]
            sex = input("Enter your character's sex (male, female, other): \n")
            if sex in sexes:
                return sex
            else:
                print("Invalid sex, please input male, female or other.")

    def create_player(self):
        player = Player("", "", "")
        name = player.get_name()
        height = player.get_height()
        sex = player.get_sex()


    def show_stats(self):
        """
        Display user inputs and amount of gold
        """
        print(f"Name: {self.name}")
        print(f"Height: {self.height}")
        print(f"Sex: {self.sex}")
        print(f"Gold: {self.gold} pieces")

# Intro

def intro():
    """
    Method that combines player creation and stat-display
    """
    print("""
    Welcome intrepid adventurer! And say 'Hello World!' to the world
    of Pythonia! You, a daring youth in search of your fortune,
    may one day soon be asked to answer the call to adventure.
    
    Off in distant lands riches and danger await. In Pythonia,
    bravery, wit, and a little bit of luck will determine your fate. 
    
    A treasure lies hidden in the depths of a haunted castle,
    but only those strong enough to overcome the challenges may claim it.

    First, let's get to know who are you, and what you look like?
    """)
    player = Player("", "", "").create_player()  # Create the player
    player.show_stats()  # Display the player's stats
    return player


player = Player(name, height, sex)


player.show_stats()