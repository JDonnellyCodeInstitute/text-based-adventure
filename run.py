# Write your code to expect a terminal of 80 characters wide and 24 rows high
#Every input method needs a \n at the end of the text to work in heroku
import gspread
from google.oauth2.service_account import Credentials
import sys
import random

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

#class PlayerDataManipulation:
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
            sex = input("Enter your character's sex (man, woman, other): \n").lower()
            if sex in sexes:
                return sex
            else:
                print("Invalid sex, please input male, female or other.")

    def create_player(self):
        player = Player("","","")
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
            print(f"Restarting with {player.name}.")
            print("Proceeding to the tavern...")
            tavern(player)
            break
        elif restart_choice == "new":
            player = intro()
            tavern(player)
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
    if call_to_adventure(player):
        print("Proceeding to the tavern...")
    else:
        game_over(player)

    return player

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

# Tavern Section
def tavern(player):
    """
    Includes all choices user can make in the tavern
    """
    initial_dialogue_tavern(player)
    heard_info = False
    min_bet = 1

    while True:
        print("\nWhat would you like to do in the tavern?")
        print("""
        1. Drink ale (increases minimum bet)
        2. Bet on a game of dice
        3. Bet on a coin flip
        4. Listen out for info on treasure
        5. Head for the castle (available only after hearing about the treasure)
        """)

        choice = input("Choose an option (1-5): \n")
        if choice == "1":
            min_bet = drink_ale(player, min_bet)
        elif choice == "2":
            bet_game(player, min_bet, game="dice")
        elif choice == "3":
            bet_game(player, min_bet, game="coin flip")
        elif choice == "4":
            if not heard_info:
                heard_info = listen_for_treasure_info(player)
            else:
                print("You've already heard about the treasure.")
        elif choice == "5":
            if heard_info:
                print(f"\n{player.name} decides to head for the castle!")
                guard_interaction(player)
                break  # Loop ends here to move onto next phase
            else:
                print("You need to gather information about the treasure first.")
        else:
            print("Invalid option, please choose 1-5.")

def initial_dialogue_tavern(player):
    print("""\nThe mysterious stranger leads you to a murky tavern.\n
    As you approach you hear raucous laughter and the door swings open.
    A rotten drunk, mostly toothless, sailor is being dragged by
    the scruff of the neck and thrown out the door.
    
    'And STAY OUT!' shouts the tavern owner as he notices you and the
    mysterious stranger.\n""")
    if player.height == "short":
        print("'Awoite shortarse, in or out. Same goes for your creepy mate'")
    elif player.height == "tall":
        print("'Awoite lanky, in or out. Same goes for your creepy mate'")
    elif player.height == "average":
        print("'Awoite average Joe, in or out. Same goes for your creepy mate'")
    
    print("""\nThe mysterious strangers bows, wishes you luck, and takes his leave.
    You enter the tavern""")

def drink_ale(player, min_bet):
    """
    Drink ale and increase minimum bet.
    """
    print(f"{player.name} drinks a frothy ale. The room spins slightly.")
    min_bet *= 2
    print(f"Your new minimum bet is now {min_bet} gold.")
    return min_bet

def bet_game(player, min_bet, game):
    """
    Handle betting on dice or coin flip, allowing the player to choose their bet.
    """
    print("In each game, if you win you earn what you staked. If not, you lose it.")

    if player.gold <= 0 | player.gold < min_bet:
        print(f"You don't have enough gold ({player.gold}) left to cover your minimum bet ({min_bet}). You can't place any bets.")
        return

    # Prompts player to choose bet, greater than or equal to min bet, less than or equal to total gold
    while True:
        try:
            bet = int(input(f"How much would you like to bet? (min: {min_bet}, max: {player.gold}): \n"))
            if min_bet <= bet <= player.gold:
                break
            else:
                print(f"Invalid bet. You must bet at least {min_bet} and no more than {player.gold}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Programming for dice roll and coin flip games
    if game == "dice":
        print("""You challenge the barkeep to a game of dice.\n If you roll higher you win.""")
        player_roll = random.randint(1, 6)
        keeper_roll = random.randint(1, 6)
        print(f'You rolled {player_roll}, the tavern keeper rolled {keeper_roll}.')
        if player_roll > keeper_roll:
            player.gold += bet
            print(f'You win {bet} gold! You now have {player.gold} gold pieces.')
        else:
            player.gold -= bet
            print(f'You lose {bet} gold! You now have {player.gold} gold pieces.')

    elif game == "coin flip":
        print("You make a bet with the innkeeper that you can call a coin toss.")
        
        while True:
            call = input("Call the coin flip! (heads or tails): \n").lower()
            if call not in ["heads", "tails"]:
                print("Invalid selection. Please input 'heads' or 'tails'.")
            else:
                break

        coin = random.choice(["heads", "tails"])
        print(f"The coin landed on {coin}.")

        if call == coin:
            player.gold += bet
            print(f'You win {bet} gold! You now have {player.gold} gold pieces.')
        else:
            player.gold -= bet
            print(f'You lose {bet} gold! You now have {player.gold} gold pieces.')

def listen_for_treasure_info(player):
    """
    Player listens out for treasure information.
    """
    print(f"""\n{player.name} overhears a drunken smuggler talking about The Beast Lord's
    castle.\n'Hiccup!'...'That bloody guard! Hiccup!'...'I tell ya, he's got some bloody gaul!
    Trying to take me for 50 pieces!? Pah! Doesn't he know that I know, which he don't know
    but I do know that there's...' the smuggler takes a moment to belch loudly, 'A bloody
    secret bloody passageway! In the shadows! On the east side of the castle! Shhhh!
    Hiccup!'...'Trade secret that is!' He shouted, seemingly to his shadow, then drifted to sleep
    and began to snore loudly.""")
    return True

# Entering the castle
def guard_interaction(player):
    """
    Player approaches castle gate and is pestered for a bribe.
    If they can afford to pay the guard they enter the main gate,
    else they have to search for the secret entry
    """
    bribe_required = 50
    initial_dialogue_guard(player)
    if player.gold >= bribe_required:
        give_bribe = input(f"You have {player.gold} gold. Bribe guard? (yes / no)\n").lower()
        if give_bribe == "yes":
            print(f"""'Pleasure doing business wif ya. Now move along. Before I change my mind.'
            You enter the castle.""")
            #enter castle method goes here
        elif give_bribe == "no":
            print("""'Watchu wasting my time for then pillock. Sling
            yer hook.' 
            
            Head held high and moral superiority assured, you slink off in 
            the dark and mud to the east side of the castle in search of 
            the passageway from the drunken smuggler's ramblings.""")
            #secret passageway method goes here
        else:
            print("Invalid input, please write yes or no.")
    else:
        print(f"""You empty your pockets. You pick a handful of buttons
        from one, and a moth flies from the other.
        
        You have {player.gold} gold and can't afford to bribe the guard. 
        
        'Watchu wasting my time for pillock. Sling yer hook.'
        
        You head into the shadows, in search of the passageway
        on the east side of the building.""")
        secret_passageway(player)

def initial_dialogue_guard(player):
    """
    Starting dialogue with guard
    """
    print("""As you approach the castle you spot a guard posted
    at the front gate. His head droops as he appears on the verge of 
    nodding off. A branch breaks under your foot and the guard jolts
    awake.\n""")
    if player.sex == "woman":
        print("""The guard lets out a long wolf whistle. 'Well, well,
        well. It must be my lucky day! Not often fine young ladies like 
        yourself be approaching MY turf. You 'ere to keep me company?'

        Through browned and blackened teeth the guard gives you his best
        smile.
        
        You try your best to hide your anger and disgust but the guard
        must spot it on your face as his own expression hardens.
        
        'You want in, it'll cost ya like everyone else. 50 pieces.
        Otherwise, clear off!'""")
    else:
        print("""'Well, well, well. It must be my lucky day! You 
        'ere to keep me company?'

        Through browned and blackened teeth the guard gives you 
        a sinister smile.
        
        'You want in, it'll cost ya. 50 pieces. Otherwise, clear 
        off!\n'""")

# The secret entrance
def secret_passageway(player):
    """
    Describes the player's journey into the secret passageway
    leading to a confrontation with a troll.
    """
    print(f"\n{player.name} sneaks into the shadows and locates the hidden entrance on the east side.")
    print("You find a narrow, dark passageway that seems to spiral downward into the earth.")
    print("The air grows colder and damper as you descend.")
    print("Suddenly, a booming voice echoes in the darkness...\n")
    print("'WHO DARES TO ENTER MY DOMAIN?!'")
    
    troll_encounter(player)

def troll_encounter(player):
    """
    Initiates the troll encounter with a riddle game.
    """
    print(f"A massive, hulking figure steps out of the shadows. It's a troll! He blocks your path.")
    print("'If you want to pass, you must answer my riddles!' the troll growls.")
    #riddles_game(player)


#main
def main():
    """
    Main function where all other required functions will be called
    """
    player = intro()
    tavern(player)
    #player = Player("Keith", "tall", "man")
    guard_interaction(player)

#Call main and play the game
main()