# Write your code to expect a terminal of 80 characters wide and 24 rows high
#Every input method needs a \n at the end of the text to work in heroku
import gspread
from google.oauth2.service_account import Credentials
import sys

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

#Methods for initial set-up and player creation
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
            name = input("Enter your character's name (letters only): \n").capitalize()
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
            sexes = ["man", "woman", "other"]
            sex = input("Enter your character's sex (man, woman, other): \n")
            if sex in sexes:
                return sex
            else:
                print("Invalid sex, please input male, female or other.")

    def create_player(self):
        player = Player("", "", "")
        name = player.get_name()
        height = player.get_height()
        sex = player.get_sex()
        return Player(name, height, sex)

    def show_stats(self):
        """
        Display user inputs and amount of gold
        """
        print(f"Name: {self.name}")
        print(f"Height: {self.height}")
        print(f"Sex: {self.sex}")
        print(f"Gold: {self.gold} pieces")

# For handling game over events
def game_over(player=None):
    """
    Game over, with option to restart or quit
    """
    print("\nGAME OVER!\n")
    while True:
        play_again = input("Play again? (yes/no): \n").lower()
        if play_again == "yes":
            restart_game(player)
        elif play_again == "no":
            print("Thanks for playing!")
            sys.exit()
        else:
            print("Invalid input, please type 'yes' or 'no'.")

def restart_game(player=None):
    """
    Handle restarting the game with the same or new character
    """
    while True:
        restart_choice = input("Do you want to restart with the same character? (yes/new): \n").lower()
        if restart_choice == "yes":
            call_to_adventure(player)
            break
        elif restart_choice == "new":
            intro()
            break
        else:
            print("Invalid input, please type 'yes' or 'new'.")

# Intro and call to adventure
def intro():
    """
    Method that combines player creation, stat-display and call to
    adventure to start the game
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
    player = Player("", "", "").create_player()
    player.show_stats()
    # NEED TO PICK UP FROM THIS IF STATEMENT
    if call_to_adventure(player):
        print("Proceeding to the tavern...")
    else:
        print("The game is over.")

def call_to_adventure(player):
    """
    Presents the player with the call to adventure.
    """
    print(f"""
    A mysterious figure approaches you as you rest by the fire.
    "{player.name}, I have been watching you. You seem like someone
    destined for great things. 
    
    It is prophecied that a brave, {player.height}, {player.sex} like
    you will some day make it to the Beast Lord's castle 
    and end his tyrannous reign. 
    
    I can guide you to a tavern frequented by smugglers and
    mercenaries who know ways of entering the castle.
    
    However, you first must make the choice. Will you answer the call 
    to adventure, claim untold riches, and liberate the people of 
    Pythonia or will you sit here by the fire and live a quiet life?"
    """)

    while True:
        choice = input("Do you accept the call to adventure? (yes/no): \n").lower()
        if choice == "yes":
            print(f"Brave {player.name}, you will now begin your adventure!")
            return True
        elif choice == "no":
            print(f"{player.name} chooses a quiet life by the fire. Game Over.")
            return False
        else:
            print("Invalid input, please type 'yes' or 'no'.")



def main():
    """
    Main function where all other required functions will be called
    """
    player = intro()
    call_to_adventure(player)

#Call main and play the game
main()