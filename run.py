import gspread
from google.oauth2.service_account import Credentials
import sys
import random
import colorama
from colorama import Fore, Style
# Initialising colorama for Windows compatibility
colorama.init(autoreset=True)

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
        self.heard_info = False
        # Items for endgame stats print
        self.ales_drank = 0 
        self.dice_wins = 0  
        self.dice_losses = 0 
        self.coin_wins = 0  
        self.coin_losses = 0 
        self.guard_bribed = 0 
        self.riddles_correct = 0 
        self.riddles_incorrect = 0 
        self.rps_won = 0  
        self.rps_lost = 0 
        self.restarts = 0

#player data manipulation
    def show_stats(self):
        """
        Display user inputs and amount of gold
        """
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Name: {self.name}")
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Height: {self.height}")
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Sex: {self.sex}")
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Gold: {self.gold} pieces")

    def get_name(self):
        """
        Name validation to ensure only letters are input
        """
        while True:
            name = get_input_with_length("Enter your character's name (letters only): \n").capitalize()
            if name.isalpha():
                return name
            else:
                print(Fore.RED + "Invalid name, please use letters only.")

    def get_height(self):
        """
        Height validation to ensure users input only from the three options
        """
        while True:
            valid_heights = ["tall", "short", "average"]
            height = get_input_with_length("Enter your character's height (short, average, tall): \n").lower()
            if height in valid_heights:
                return height
            else:
                print(Fore.RED + "Invalid height, please enter short, average or tall.")

    def get_sex(self):
        """
        Sex validation to ensure users input only from the three options
        """
        while True:
            sexes = ["man", "woman", "other"]
            sex = get_input_with_length("Enter your character's sex (man, woman, other): \n").lower()
            if sex in sexes:
                return sex
            else:
                print(Fore.RED + "Invalid sex, please input man, woman or other.")

    def create_player(self):
        player = Player("","","")
        name = player.get_name()
        height = player.get_height()
        sex = player.get_sex()
        return Player(name, height, sex)

# For handling game over events
def game_over(player):
    """
    Game over, with option to restart or quit.
    First saves player stats and shows them to the player.
    """
    print(Fore.RED + Style.BRIGHT + "GAME OVER!\n")
    save_player_stats(player)
    game_over_stats(player)

    while True:
        play_again = get_input_with_length("Play again? (yes/no): \n").lower()
        if play_again == "yes":
            restart_game(player)
        elif play_again == "no":
            print("Thanks for playing!")
            sys.exit()
        else:
            print(Fore.RED + "Invalid input, please type 'yes' or 'no'.")

def restart_game(player=None):
    """
    Handle restarting the game with the same or new character
    """
    while True:
        player.heard_info = False
        restart_choice = get_input_with_length("Do you want to restart with the same character? (yes/new): \n").lower()
        if restart_choice == "yes":
            player.restarts += 1
            print(f"Restarting with {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.name}{Style.RESET_ALL}.")
            print(f"Proceeding to {Fore.CYAN}{Style.BRIGHT}{Style.BRIGHT}The Tavern...{Style.RESET_ALL}")
            press_enter_to_continue()
            tavern(player)
            break
        elif restart_choice == "new":
            player = intro()
            tavern(player)
            break
        else:
            print(Fore.RED + "Invalid input, please type 'yes' or 'new'.")

def save_player_stats(player):
    """
    List of data created to be stored in excel file
    """
    data = [
        player.name,
        player.height,
        player.sex,
        player.gold,
        player.ales_drank,  
        player.dice_wins,   
        player.dice_losses, 
        player.coin_wins,   
        player.coin_losses, 
        player.guard_bribed, 
        player.riddles_correct, 
        player.riddles_incorrect, 
        player.rps_won,      
        player.rps_lost,
        player.restarts      
    ]
    adventurer.append_row(data)

def game_over_stats(player):
    """
    Display user inputs and statistics at end of game
    """
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "--- Player Stats ---")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Name: {player.name}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Height: {player.height}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Sex: {player.sex}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Gold: {player.gold} pieces")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Ales Drank: {player.ales_drank}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Dice Wins: {player.dice_wins}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Dice Losses: {player.dice_losses}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Coin Wins: {player.coin_wins}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Coin Losses: {player.coin_losses}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Guard Bribed: {player.guard_bribed}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Riddles Correct: {player.riddles_correct}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Riddles Incorrect: {player.riddles_incorrect}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Rock-Paper-Scissors Won: {player.rps_won}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Rock-Paper-Scissors Lost: {player.rps_lost}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Restarts: {player.restarts}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "---------------------")

# Simple pacing function to improve the user experience
def press_enter_to_continue():
    get_input_with_length("\nPress Enter to continue...\n")

# Control to stop inputs that are too long
def get_input_with_length(prompt, max_length=25):
    """
    Prompts user for input and ensures the input does not exceed the max length
    """
    while True:
        user_input = input(Fore.YELLOW + prompt + Style.RESET_ALL)
        if len(user_input) <= max_length:
            return user_input
        else:
            print(Fore.RED + f"Input must be {max_length} characters or less. Please try again.")

# Intro and call to adventure
def intro():
    """
    Method that combines player creation, stat-display and call to
    adventure to start the game
    """
    print(f"""
    Welcome intrepid adventurer! And say '{Fore.LIGHTGREEN_EX}Hello World!{Style.RESET_ALL}' to the world
    of {Fore.MAGENTA}Pythonia{Style.RESET_ALL}! You, a daring youth in search of your fortune,
    may one day soon be asked to answer {Fore.CYAN}{Style.BRIGHT}{Style.BRIGHT}The Call to Adventure{Style.RESET_ALL}.
    
    Off in distant lands riches and danger await. In {Fore.MAGENTA}Pythonia{Style.RESET_ALL},
    bravery, wit, and a little bit of luck will determine your fate. 
    
    A treasure lies hidden in the depths of a {Fore.CYAN}{Style.BRIGHT}{Style.BRIGHT}Haunted Castle{Style.RESET_ALL},
    but only those strong enough to overcome the challenges may claim it.

    First, let's get to know who are you, and what you look like?
    """)
    player = Player("", "", "").create_player()
    player.show_stats()
    if call_to_adventure(player):
        print(f"Proceeding to {Fore.CYAN}{Style.BRIGHT}{Style.BRIGHT}The Tavern...{Style.RESET_ALL}")
        press_enter_to_continue()
    else:
        game_over(player)

    return player

def call_to_adventure(player):
    """
    Presents the player with the call to adventure.
    """
    print(f"""
    A {Fore.LIGHTWHITE_EX}Mysterious Stranger{Style.RESET_ALL} approaches you as you rest by the fire.
    {Fore.LIGHTWHITE_EX}"{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.name}{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}, I have been watching you. You seem like someone
    destined for great things. 
    
    It is prophecied that a brave,{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.height}{Style.RESET_ALL}, {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.sex}{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}like
    you will some day make it to the{Style.RESET_ALL} {Fore.RED}{Style.BRIGHT}Beast Lord{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}'s{Style.RESET_ALL} {Fore.CYAN}{Style.BRIGHT}{Style.BRIGHT}Castle{Style.RESET_ALL} 
    {Fore.LIGHTWHITE_EX}and end his tyrannous reign. 
    
    I can guide you to a{Style.RESET_ALL} {Fore.CYAN}{Style.BRIGHT}{Style.BRIGHT}Tavern{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}frequented by smugglers and
    mercenaries who know ways of entering{Style.RESET_ALL} {Fore.CYAN}{Style.BRIGHT}{Style.BRIGHT}The Castle{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}.
    
    However, you first must make the choice. Will you answer{Style.RESET_ALL} {Fore.CYAN}{Style.BRIGHT}The Call 
    To Adventure{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}, claim untold riches, and liberate the people of{Style.RESET_ALL} 
    {Fore.MAGENTA}Pythonia{Style.RESET_ALL} {Fore.LIGHTWHITE_EX}or will you sit here by the fire and live a quiet life?"
    """)

    while True:
        choice = get_input_with_length(f"Do you accept {Fore.CYAN}{Style.BRIGHT}The Call to Adventure{Style.RESET_ALL}{Fore.YELLOW}? (yes/no): \n").lower()
        if choice == "yes":
            print(f"\nBrave {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.name}{Style.RESET_ALL}, you will now begin your adventure!\n")
            return True
        elif choice == "no":
            print(f"\n{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.name}{Style.RESET_ALL} chooses a quiet life by the fire.\n")
            return False
        else:
            print(f"{Fore.RED}Invalid input, please type 'yes' or 'no'.")

# Tavern Section
def tavern(player):
    """
    Includes full tavern sequence
    """
    initial_dialogue_tavern(player)
    tavern_options(player)
    
def initial_dialogue_tavern(player):
    print(f"""The {Fore.LIGHTWHITE_EX}Mysterious Stranger{Style.RESET_ALL} leads you to a murky {Fore.CYAN}{Style.BRIGHT}Tavern{Style.RESET_ALL}.\n
    As you approach you hear raucous laughter and the door swings open.
    A rotten drunk, mostly toothless, sailor is being dragged by
    the scruff of the neck and thrown out the door.
    
    {Fore.LIGHTGREEN_EX}'And STAY OUT!'{Style.RESET_ALL} shouts the {Fore.LIGHTGREEN_EX}Tavern Keeper{Style.RESET_ALL} as he notices you and the
    {Fore.LIGHTWHITE_EX}Mysterious Stranger{Style.RESET_ALL}.\n""")
    if player.height == "short":
        print(f"{Fore.LIGHTGREEN_EX}'Awoite{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{Style.BRIGHT}shortarse{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}, in or out. Same goes for your creepy mate.'")
    elif player.height == "tall":
        print(f"{Fore.LIGHTGREEN_EX}'Awoite{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{Style.BRIGHT}lanky{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}, in or out. Same goes for your creepy mate.'")
    elif player.height == "average":
        print(f"{Fore.LIGHTGREEN_EX}'Awoite{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{Style.BRIGHT}average Joe{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}, in or out. Same goes for your creepy mate.'")
    
    print(f"\nThe {Fore.LIGHTWHITE_EX}Mysterious Stranger{Style.RESET_ALL} bows, wishes you luck, and takes his leave.\n")
    print(f"You enter {Fore.CYAN}{Style.BRIGHT}The Tavern...{Style.RESET_ALL}")
    press_enter_to_continue()

def tavern_options(player):
    """
    Includes all choices user can make in the tavern
    """
    min_bet = 1

    while True:
        print(f"What would you like to do in {Fore.CYAN}{Style.BRIGHT}The Tavern{Style.RESET_ALL}?")
        print(f"""
        1. Drink ale (increases {Fore.LIGHTBLUE_EX}{Style.BRIGHT}minimum bet{Style.RESET_ALL})
        2. Bet on a game of {Fore.CYAN}{Style.BRIGHT}dice{Style.RESET_ALL}
        3. Bet on a {Fore.CYAN}{Style.BRIGHT}coin flip{Style.RESET_ALL}
        4. Listen out for info on treasure
        5. Head for {Fore.CYAN}{Style.BRIGHT}The Castle{Style.RESET_ALL} (available only after hearing about the treasure)
        """)

        choice = get_input_with_length("Choose an option (1-5): \n")
        if choice == "1":
            min_bet = drink_ale(player, min_bet)
        elif choice == "2":
            bet_game(player, min_bet, game="dice")
        elif choice == "3":
            bet_game(player, min_bet, game="coin flip")
        elif choice == "4":
            if not player.heard_info:
                player.heard_info = listen_for_treasure_info(player)
            else:
                print("You've already heard about the treasure.")
        elif choice == "5":
            if player.heard_info:
                print(f"\n{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.name}{Style.RESET_ALL} decides to head for {Fore.CYAN}{Style.BRIGHT}The Castle{Style.RESET_ALL}!")
                press_enter_to_continue()
                guard_interaction(player)
                break  # Loop ends here to move onto next phase
            else:
                print("\nYou need to gather information about the treasure first.")
                press_enter_to_continue()
        else:
            print("Invalid option, please choose 1-5.")

def drink_ale(player, min_bet):
    """
    Drink ale and increase minimum bet.
    """
    print(f"\n{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.name}{Style.RESET_ALL} drinks a frothy ale. The room spins slightly.\n")
    min_bet *= 2
    player.ales_drank += 1
    print(f"Your new {Fore.LIGHTBLUE_EX}{Style.BRIGHT}minimum bet{Style.RESET_ALL} is now {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{min_bet}{Style.RESET_ALL} gold.")
    press_enter_to_continue()
    return min_bet

def bet_game(player, min_bet, game):
    """
    Handle betting on dice or coin flip, allowing the player to choose their bet.
    """
    print("\nIn each game, if you win you earn what you staked. If not, you lose it.\n")

    if player.gold <= 0 | player.gold < min_bet:
        print(f"You don't have enough gold ({Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.gold}{Style.RESET_ALL}) left to cover your {Fore.LIGHTBLUE_EX}{Style.BRIGHT}minimum bet{Style.RESET_ALL} ({Fore.LIGHTBLUE_EX}{Style.BRIGHT}{min_bet}{Style.RESET_ALL}). You can't place any bets.")
        return

    bet = get_bet(player, min_bet)

    if game == "dice":
        dice_game(player, bet)
    elif game == "coin flip":
        coin_flip_game(player, bet)

def get_bet(player, min_bet):
    """Prompts player to choose bet, greater than or equal to min bet,
    less than or equal to total gold"""
    while True:
        try:
            bet = int(get_input_with_length(f"How much would you like to bet? (min: {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{min_bet}{Style.RESET_ALL}{Fore.YELLOW}, max:{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.gold}{Style.RESET_ALL}): \n"))
            if min_bet <= bet <= player.gold:
                return bet
            else:
                print(f"Invalid bet. You must bet at least {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{min_bet}{Style.RESET_ALL} and no more than {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.gold}{Style.RESET_ALL}.")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid number.")

def dice_game(player, bet):
    """
    Handle the dice game logic where the player rolls against the tavern keeper.
    """
    print(f"You challenge the {Fore.LIGHTGREEN_EX}Tavern Keeper{Style.RESET_ALL} to a game of {Fore.CYAN}{Style.BRIGHT}dice{Style.RESET_ALL}.") 
    print("If you roll higher you win.")
    player_roll = random.randint(1, 6)
    keeper_roll = random.randint(1, 6)
    print(f'You rolled {player_roll}, the {Fore.LIGHTGREEN_EX}Tavern Keeper{Style.RESET_ALL} rolled {keeper_roll}.')
    
    if player_roll > keeper_roll:
        player.gold += bet
        player.dice_wins += 1
        print(f'\n{Fore.GREEN}{Style.BRIGHT}You win {bet} gold!{Style.RESET_ALL} You now have {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.gold}{Style.RESET_ALL} gold pieces.')
        press_enter_to_continue()
    else:
        player.gold -= bet
        player.dice_losses += 1
        print(f'\n{Fore.RED}You lose {bet} gold!{Style.RESET_ALL} You now have {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.gold}{Style.RESET_ALL} gold pieces.')
        press_enter_to_continue()

def coin_flip_game(player, bet):
    """
    Handle the coin flip game where the player calls heads or tails.
    """
    print(f"\nYou make a bet with the {Fore.LIGHTGREEN_EX}Tavern Keeper{Style.RESET_ALL} that you can call a coin toss.\n")
    
    while True:
        call = get_input_with_length(f"Call the {Fore.CYAN}{Style.BRIGHT}coin flip{Style.RESET_ALL}! (heads or tails): \n").lower()
        if call not in ["heads", "tails"]:
            print(f"\n{Fore.RED}Invalid selection. Please input 'heads' or 'tails'.")
        else:
            break

    coin = random.choice(["heads", "tails"])
    print(f"\nThe coin landed on {coin}.")

    if call == coin:
        player.gold += bet
        player.coin_wins += 1
        print(f'\n{Fore.GREEN}{Style.BRIGHT}You win {bet} gold!{Style.RESET_ALL} You now have {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.gold}{Style.RESET_ALL} gold pieces.')
        press_enter_to_continue()
    else:
        player.gold -= bet
        player.coin_losses += 1
        print(f'\n{Fore.RED}You lose {bet} gold!{Style.RESET_ALL} You now have {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.gold}{Style.RESET_ALL} gold pieces.')
        press_enter_to_continue()

def listen_for_treasure_info(player):
    """
    Player listens out for treasure information.
    """
    print(f"\n{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.name}{Style.RESET_ALL} overhears a {Fore.LIGHTYELLOW_EX}Drunken Smuggler{Style.RESET_ALL} talking about {Fore.RED}{Style.BRIGHT}The Beast Lord{Style.RESET_ALL}'s {Fore.CYAN}{Style.BRIGHT}Castle{Style.RESET_ALL}.")
    print(f"\n{Fore.LIGHTYELLOW_EX}*Hiccup* 'That bloody{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX}!' *Hiccup* 'I tell ya, he's got some bloody gaul!'")
    print(f"{Fore.LIGHTYELLOW_EX}'Trying to take me for 30 pieces!? Pah!'")
    print(f"{Fore.LIGHTYELLOW_EX}'Doesn't he know that I know... which he don't know... but I do that there's...'")
    print("\nThe smuggler takes a moment to belch loudly.\n")
    print(f"{Fore.LIGHTYELLOW_EX}'A bloody{Style.RESET_ALL} {Fore.CYAN}{Style.BRIGHT}Secret Passageway{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX}! In the shadows to the east side of{Style.RESET_ALL} {Fore.CYAN}{Style.BRIGHT}The Castle{Style.RESET_ALL}{Fore.LIGHTYELLOW_EX}!'")
    print(f"{Fore.LIGHTYELLOW_EX}'Shhhh!' *Hiccup* 'Trade secret that is!'{Style.RESET_ALL} He shouts, seemingly to himself.")
    print("His eyes droop closed, and the smuggler begins to snore loudly.")
    press_enter_to_continue()
    return True

# Entering the castle
def guard_interaction(player):
    """
    Player approaches castle gate and is pestered for a bribe.
    If they can afford to pay the guard they enter the main gate,
    else they have to search for the secret entry
    """
    bribe_required = 30
    initial_dialogue_guard(player)
    if player.gold >= bribe_required:
        give_bribe = get_input_with_length(f"You have {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.gold}{Style.RESET_ALL} gold. Bribe {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL}? (yes / no): \n").lower()
        if give_bribe == "yes":
            player.guard_bribed += 1
            print(f"\n{Fore.LIGHTMAGENTA_EX}'Pleasure doing business wif ya. Now move along. Before I change my mind.'")
            print(f"\nYou enter {Fore.CYAN}{Style.BRIGHT}The Castle...{Style.RESET_ALL}")
            press_enter_to_continue()
            final_showdown(player)
        elif give_bribe == "no":
            print(f"\n{Fore.LIGHTMAGENTA_EX}'Watchu wasting my time for then pillock. Sling yer hook.'")
            print("\nHead held high and moral superiority assured,")
            print("you slink off in search of the passageway")
            press_enter_to_continue()
            secret_entry_full_sequence(player)
        else:
            print(f"{Fore.RED}Invalid input, please write yes or no.")
    else:
        print("You empty your pockets.")
        print("\nYou pick a handful of buttons from one, and a moth flies from the other.") 
        print(f"\nYou have {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.gold}{Style.RESET_ALL} gold and can't afford to bribe the {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL}.\n")
        print(f"{Fore.LIGHTMAGENTA_EX}'Watchu wasting my time for then pillock. Sling yer hook.'\n")
        if player.gold > 0:
            earn_more_gold = get_input_with_length(f"Return to {Fore.CYAN}{Style.BRIGHT}The Tavern{Style.RESET_ALL} {Fore.YELLOW}to try and win more gold? (yes/no): \n").lower()
            if earn_more_gold == "yes":
                print(f"\nReturning to {Fore.CYAN}{Style.BRIGHT}The Tavern{Style.RESET_ALL} to make enough gold to bribe the {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL}...")
                press_enter_to_continue()
                player.heard_info = True
                tavern_options(player)
            elif earn_more_gold == "no":
                print(f"\nYou get out of the {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL}'s sight to search for {Fore.CYAN}{Style.BRIGHT}The Secret Passageway{Style.RESET_ALL}.")
                press_enter_to_continue()
                secret_entry_full_sequence(player)
            else:
                print(f"{Fore.RED}Invalid input, please write 'y' or 'n'")
        else:
            print(f"You nod curtly to the {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL} and get out of his sight to search for {Fore.CYAN}{Style.BRIGHT}The Secret Passageway{Style.RESET_ALL}.\n")
            press_enter_to_continue()
            secret_entry_full_sequence(player)

def initial_dialogue_guard(player):
    """
    Starting dialogue with guard
    """
    print(f"As you approach you spot a {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL} posted at the front gate.") 
    print("His head droops as he appears on the verge of nodding off.")
    print(f"A branch breaks under your foot and the {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL} jolts awake.")
    if player.sex == "woman":
        print(f"""
        The {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL} lets out a long wolf whistle. 
        
        {Fore.LIGHTMAGENTA_EX}'Well, well, well. It must be my lucky day! Not often fine young ladies 
        like yourself be approaching MY turf. You 'ere to keep me company?'{Style.RESET_ALL}

        Through browned and blackened teeth the {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL} gives you his best
        smile.
        
        You try your best to hide your anger and disgust but the {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL}
        must spot it on your face as his own expression hardens.
        
        {Fore.LIGHTMAGENTA_EX}'You want in, it'll cost ya like everyone else. 30 pieces.
        Otherwise, clear off!'""")
        press_enter_to_continue()
    else:
        print(f"""
        {Fore.LIGHTMAGENTA_EX}'Well, well, well. It must be my lucky day!
        You 'ere to keep me company?'{Style.RESET_ALL}

        Through browned and blackened teeth the {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL} gives you 
        a sinister smile.
        
        {Fore.LIGHTMAGENTA_EX}'You want in, it'll cost ya. 30 pieces. Otherwise, clear 
        off!'""")
        press_enter_to_continue()

# The secret entrance
def secret_entry_full_sequence(player):
    secret_passageway(player)
    troll_encounter(player)
    riddles_game(player)

def secret_passageway(player):
    """
    Describes the player's journey into the secret passageway
    leading to a confrontation with a troll.
    """
    print(f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.name}{Style.RESET_ALL} sneaks into the shadows and locates {Fore.CYAN}{Style.BRIGHT}{Style.BRIGHT}The Secret Passageway{Style.RESET_ALL} on the east side.")
    print("You find a narrow, dark passageway that seems to spiral downward into the earth.")
    print("The air grows colder and damper as you descend.")
    print("Suddenly, a booming voice echoes in the darkness...\n")
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}'WHO DARES TO ENTER MY DOMAIN?!'{Style.RESET_ALL}")
    press_enter_to_continue()
    troll_encounter(player)

def troll_encounter(player):
    """
    Initiates the troll encounter with a riddle game.
    """
    print("A massive, hulking figure steps out of the shadows.") 
    print(f"It's a {Fore.LIGHTGREEN_EX}{Style.BRIGHT}Troll{Style.RESET_ALL}! He blocks your path.")
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}'If you want to pass, you must answer my riddles!'{Style.RESET_ALL} the {Fore.LIGHTGREEN_EX}{Style.BRIGHT}Troll{Style.RESET_ALL} growls.")
    print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}'Or else... you'll be my dinner.'")
    press_enter_to_continue()
    riddles_game(player)

def riddles_game(player):
    """
    Troll asks riddles, and player must answer correctly to proceed.
    """
    riddles = [
        {"question": "What has keys but can't open locks?", "answer": "piano"},
        {"question": "The more you take, the more you leave behind. What am I?", "answer": "footsteps"},
        {"question": "What comes once in a minute, twice in a moment, but never in a thousand years?", "answer": "m"}
    ]
    
    print(f"The {Fore.LIGHTGREEN_EX}{Style.BRIGHT}Troll{Style.RESET_ALL} gives you three riddles to answer.")
    
    correct_answers = 0
    for riddle in riddles:
        print(f"\nRiddle: {Fore.LIGHTGREEN_EX}{Style.BRIGHT}{riddle['question']}{Style.RESET_ALL}")
        answer = get_input_with_length("What is your answer? \n").lower()
        if answer == riddle["answer"]:
            print(Fore.GREEN + Style.BRIGHT + "\nCorrect!")
            player.riddles_correct += 1
        else:
            player.riddles_incorrect += 1
            print(f"\n{Fore.RED}Wrong!{Style.RESET_ALL} The correct answer was: {riddle['answer']}")
    
    if player.riddles_correct >= 2:
        print(f"\nThe {Fore.LIGHTGREEN_EX}{Style.BRIGHT}Troll{Style.RESET_ALL} grunts, impressed. {Fore.LIGHTGREEN_EX}{Style.BRIGHT}'Fine, you may pass.'{Style.RESET_ALL}")
        press_enter_to_continue()
        final_showdown(player)
    else:
        print(f"\nThe {Fore.LIGHTGREEN_EX}{Style.BRIGHT}Troll{Style.RESET_ALL} roars with laughter. {Fore.LIGHTGREEN_EX}{Style.BRIGHT}'You're too foolish to proceed!'{Style.RESET_ALL}")
        print(f"{Fore.RED}The{Style.RESET_ALL} {Fore.LIGHTGREEN_EX}{Style.BRIGHT}Troll{Style.RESET_ALL} {Fore.RED}leaps, grabs, and gobbles you up whole. A belch echoes through the catacombs.\n")
        game_over(player)

# Final Showdown in the castle
def final_showdown(player):
    beast_lord_speech()
    rps_battle(player)

def beast_lord_speech():
    """
    The Beast Lord delivers a dramatic speech before the final challenge.
    """
    print(f"You make your way into the heart of {Fore.CYAN}{Style.BRIGHT}{Style.BRIGHT}The Castle{Style.RESET_ALL} and approach the throne room.")
    print(f"\nThe great doors creak open, and there he stands - {Fore.RED}{Style.BRIGHT}The Beast Lord{Style.RESET_ALL}.")
    print(f"""
    A towering figure of shadow and flame. 
    His eyes burn with malice and hunger for power.
    
    {Fore.RED}{Style.BRIGHT}'Ah, another brave fool comes to claim my throne. 
    Do you think you are worthy, mortal? 
    Many have come before you, but none have succeeded.'""")
    press_enter_to_continue()
    print(f"""He pauses, letting the weight of his words sink in.
    
    {Fore.RED}{Style.BRIGHT}'Know this - those who defeat me shall rule these lands, 
    taking all that is mine. But should you fail, your soul will 
    be forfeit, and you will suffer a fate worse 
    than death itself.'""")
    press_enter_to_continue()
    print(f"""He gestures toward you with a clawed hand, his grin widening.
    
    {Fore.RED}{Style.BRIGHT}'Prepare yourself. You face a challenge of wits and reflexes. 
    A simple game for a simple mind - best me in a game of 
    Rock-Paper-Scissors, and your destiny will be yours to 
    shape...'{Style.RESET_ALL}
    
    The final battle begins now!""")
    press_enter_to_continue()

def rps_battle(player):
    """
    Best of three Rock-Paper-Scissors game against the Beast Lord.
    """
    moves = ["rock", "paper", "scissors"]
    player.rps_won = 0
    player.rps_lost = 0

    print(f"{Fore.RED}{Style.BRIGHT}The Beast Lord{Style.RESET_ALL} readies himself for the challenge...\n")

    while player.rps_won < 2 and player.rps_lost < 2:
        player_move = get_input_with_length("Choose your move (rock, paper, scissors): \n").lower()
        if player_move not in moves:
            print(Fore.RED + "Invalid move! Please choose rock, paper, or scissors.")
            continue

        beast_move = random.choice(moves)
        print(f"\n{Fore.RED}{Style.BRIGHT}The Beast Lord{Style.RESET_ALL} chooses {beast_move}.\n")

        # Determine winner
        if player_move == beast_move:
            print("It's a tie!")
        elif (player_move == "rock" and beast_move == "scissors") or \
             (player_move == "paper" and beast_move == "rock") or \
             (player_move == "scissors" and beast_move == "paper"):
            print(Fore.GREEN + Style.BRIGHT +"You win this round!")
            player.rps_won += 1
        else:
            print(f"{Fore.RED}{Style.BRIGHT}The Beast Lord{Style.RESET_ALL} {Fore.RED}wins this round!")
            player.rps_lost += 1

        print(f"\nScore - You: {player.rps_won}, {Fore.RED}{Style.BRIGHT}Beast Lord{Style.RESET_ALL}: {player.rps_lost}\n")

    # Determine final outcome
    if player.rps_won == 2:
        print(f"{Fore.GREEN}{Style.BRIGHT}You've done it!{Style.RESET_ALL} {Fore.RED}{Style.BRIGHT}The Beast Lord{Style.RESET_ALL} {Fore.GREEN}{Style.BRIGHT}has fallen. You are victorious!")
        press_enter_to_continue()
        concluding_dialogue(player)
        game_over(player)
    else:
        print(f"\n{Fore.RED}{Style.BRIGHT}The Beast Lord{Style.RESET_ALL} cackles triumphantly. {Fore.RED}You have been defeated.")
        press_enter_to_continue()
        print(f"{Fore.RED}A chill creeps up your spine as your soul is severed from your body.\n")
        game_over(player)

def concluding_dialogue(player):
    """
    Story Conclusion
    """
    print("Countless treasures are yours. The prophecy is fulfilled.") 
    print(f"A brave, {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.height}{Style.RESET_ALL}, {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.sex}{Style.RESET_ALL} sits upon the throne as Lord of {Fore.MAGENTA}Pythonia{Style.RESET_ALL}.")
    press_enter_to_continue()
    print(f"""Years pass in relative peace. 

    Initially you rule fairly, but you feel unexplainable change over time.
    
    {Fore.RED}{Style.BRIGHT}'The people must know their place'{Style.RESET_ALL} you hear as a whisper in the air.""")
    press_enter_to_continue()
    print("""As Lord:

    You raise taxes, ban public gatherings, apart from executions, and violently
    crush any threats to your rule, perceived or otherwise.""")
    press_enter_to_continue()
    print(f"How long has it been since you took {Fore.CYAN}{Style.BRIGHT}The Castle{Style.RESET_ALL}? Decades? You can't remember.")
    press_enter_to_continue()
    print(f"A spike of terror runs through you as you catch a glimpse of {Fore.RED}{Style.BRIGHT}The Beast Lord{Style.RESET_ALL}.")
    print("You leap with teeth bared toward the spot where you saw your old enemy.")
    print("\nIt's a broken mirror.\n")
    print("You see the beastly reflection of your jagged teeth and knifelike fingernails.")
    print("\nYou realise what you have become...")
    press_enter_to_continue()
    print("The doors of your throne room burst open.")
    print(f"""A brave, {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.height}{Style.RESET_ALL}, {Fore.LIGHTBLUE_EX}{Style.BRIGHT}{player.sex}{Style.RESET_ALL} rushes in and exclaims:
    
    {Fore.LIGHTWHITE_EX}{Style.BRIGHT}'Your reign of evil ends now{Style.RESET_ALL} {Fore.RED}{Style.BRIGHT}Beast Lord{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{Style.BRIGHT}!'""")
    print("\nA more human part of you deep down almost starts to laugh.")
    print("But the influence of the beast drowns that out.")
    print("Involuntarily you begin the speech.")
    print(f"""
    {Fore.RED}{Style.BRIGHT}'A brave fool comes to claim my throne?!
    Do you think you are worthy, mortal?'""")
    print("\n...")
    press_enter_to_continue()

#main
def main():
    """
    Main function where all other required functions will be called
    """
    player = intro()
    tavern(player)
    guard_interaction(player)

#Call main and play the game
main()