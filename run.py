import gspread
from google.oauth2.service_account import Credentials
import sys
import random
import colorama
from colorama import Fore, Style, Back
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


# Methods for initial set-up and player creation
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
        self.rid_won = 0
        self.rid_lost = 0
        self.rps_won = 0
        self.rps_lost = 0
        self.restarts = 0

# Player data manipulation
    def show_stats(self):
        """
        Display user inputs and amount of gold
        """
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"\nName: {self.name}")
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Height: {self.height}")
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Sex: {self.sex}")
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Gold: {self.gold} pieces")

    def get_name(self):
        """
        Name validation to ensure only letters are input
        """
        while True:
            name = get_input_with_length("Enter name: \n").capitalize()
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
            height = get_input_with_length("""Enter height
(short, average, tall):\n""").lower()
            if height in valid_heights:
                return height
            else:
                print(Fore.RED + "Either short, average or tall.")

    def get_sex(self):
        """
        Sex validation to ensure users input only from the three options
        """
        while True:
            sexes = ["man", "woman", "other"]
            sex = get_input_with_length("""Enter sex
(man, woman, other):\n""").lower()
            if sex in sexes:
                return sex
            else:
                print(Fore.RED + "Please input man, woman or other.")

    @staticmethod
    def create_player():
        player = Player("", "", "")
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
    doc = f"""
    https://docs.google.com/spreadsheets/d/1_
    FmMhmWtP10EMdpJXYXwIjeL_j1A50UksDBUsE7np2w/edit?
    gid=0#gid=0{Style.RESET_ALL}
    """
    print(Fore.RED + Style.BRIGHT + "GAME OVER!\n")
    save_player_stats(player)  # Sends player stats to the Google sheet via API
    game_over_stats(player)  # Prints player stats in the terminal
    print("\nSee historic stats at:")
    print(Back.WHITE + Fore.BLACK + doc)

    while True:
        play_again = get_input_with_length("Play again? (yes/no): \n").lower()
        if play_again == "yes":
            restart_game(player)
        elif play_again == "no":
            print("\nThanks for playing!\n")
            sys.exit()
        else:
            print(Fore.RED + "Invalid input, please type 'yes' or 'no'.")


def restart_game(player=None):
    """
    Handle restarting the game with the same or new character
    """
    while True:
        restart_choice = get_input_with_length("""Restart with same character?
(yes/new): \n""").lower()
        if restart_choice == "yes":
            player.restarts += 1
            player_reset(player)  # Resets player properties
            print(f"""
Returning with {Fore.LIGHTBLUE_EX}{player.name}{Style.RESET_ALL}.
            """)
            print(f"""
Proceeding to {Fore.CYAN}The Tavern...{Style.RESET_ALL}""")
            press_enter_to_continue()
            tavern(player)  # Goes to Tavern for fluidity
            break
        elif restart_choice == "new":
            player = intro()
            tavern(player)
            break
        else:
            print(Fore.RED + "Invalid input, please type 'yes' or 'new'.")


def player_reset(player):
    """
    Resets the player stats that effect game progression upon restart
    """
    player.gold = 10
    player.heard_info = False
    player.riddles_correct = 0
    player.guard_bribed = 0
    player.rps_won = 0


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
        player.rid_won,
        player.rid_lost,
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
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Ale Drank: {player.ales_drank}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Dice W: {player.dice_wins}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Dice L: {player.dice_losses}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Coin W: {player.coin_wins}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Coin L: {player.coin_losses}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Bribes: {player.guard_bribed}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Riddles W: {player.rid_won}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Riddles L: {player.rid_lost}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"RPS W: {player.rps_won}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"RPS L: {player.rps_lost}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Restarts: {player.restarts}")
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "---------------------")


# Simple pacing function to improve the user experience
def press_enter_to_continue():
    get_input_with_length("\nPress Enter to continue...\n")


# Control to stop inputs that are too long
def get_input_with_length(prompt, max_length=10):
    """
    Prompts user for input and ensures the input does not exceed the max length
    """
    while True:
        user_input = input(Fore.YELLOW + prompt + Style.RESET_ALL)
        if len(user_input) <= max_length:
            return user_input
        else:
            print(Fore.RED + f"Must be {max_length} characters or less.")


# Intro and call to adventure
def intro():
    """
    Method that combines player creation, stat-display and call to
    adventure to start the game
    """
    print(f"""
Welcome intrepid adventurer! And say

    '{Fore.LIGHTGREEN_EX}Hello World!{Style.RESET_ALL}'

to the world of {Fore.MAGENTA}{Style.BRIGHT}Pythonia{Style.RESET_ALL}!
You, a daring youth in search of fortune,
may one day soon be asked to answer
{Fore.CYAN}The Call to Adventure{Style.RESET_ALL}.

Off in distant lands riches and danger await.
In {Fore.MAGENTA}{Style.BRIGHT}Pythonia{Style.RESET_ALL}, bravery, wit, and a
little bit of luck will determine your fate.

A treasure lies hidden in the depths of a
{Fore.CYAN}Haunted Castle{Style.RESET_ALL},
but only those strong enough to overcome the challenges may claim it.

First, let's get to know who are you, and what you look like?
    """)
    player = Player.create_player()
    player.show_stats()
    if call_to_adventure(player):
        print(f"""
        Proceed to {Fore.CYAN}The Tavern...{Style.RESET_ALL}""")
        press_enter_to_continue()
    else:
        press_enter_to_continue()
        game_over(player)

    return player


def call_to_adventure(player):
    """
    Presents the player with the call to adventure.
    """
    print(f"""
A {Fore.LIGHTCYAN_EX}Stranger{Style.RESET_ALL}
approaches you as you rest by the fire.
{Fore.LIGHTCYAN_EX}"{Style.RESET_ALL}{Fore.LIGHTBLUE_EX}{player.name}{Style.RESET_ALL}{Fore.LIGHTCYAN_EX},
I have been watching you. You seem like someone
destined for great things.

It is prophecied that a brave,{Style.RESET_ALL}
{Fore.LIGHTBLUE_EX}{player.height}{Style.RESET_ALL}{Fore.LIGHTCYAN_EX},
{Style.RESET_ALL} {Fore.LIGHTBLUE_EX}{player.sex}{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}like you will some day make it to the{Style.RESET_ALL}
{Fore.RED}{Style.BRIGHT}Beast Lord's Castle{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}and end his tyrannous reign.

I can guide you to a{Style.RESET_ALL} {Fore.CYAN}Tavern{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}frequented by smugglers and mercenaries
who know ways of entering{Style.RESET_ALL}
{Fore.CYAN}The Castle{Style.RESET_ALL}{Fore.LIGHTCYAN_EX}.

However, you first must make the choice. Will you answer{Style.RESET_ALL}
{Fore.CYAN}The Call To Adventure{Style.RESET_ALL}{Fore.LIGHTCYAN_EX},
claim untold riches, and liberate the people of{Style.RESET_ALL}
{Fore.MAGENTA}{Style.BRIGHT}Pythonia{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}or will you sit here by the fire and live a quiet life?"
    """)

    while True:
        choice = get_input_with_length("""
        Do you accept The Call to Adventure?
        (yes/no):\n""").lower()
        if choice == "yes":
            print(f"""
            Brave {Fore.LIGHTBLUE_EX}{player.name}{Style.RESET_ALL},
            you will now begin your adventure!\n""")
            return True
        elif choice == "no":
            print(f"""
{Fore.LIGHTBLUE_EX}{player.name}{Style.RESET_ALL} chooses a quiet life.""")
            return False  # Incurs first Game Over
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
    print(f"""
    The {Fore.LIGHTCYAN_EX}Stranger{Style.RESET_ALL} leads
    you to a murky {Fore.CYAN}Tavern{Style.RESET_ALL}.\n
    As you approach you hear raucous laughter and the door swings open.
    A rotten drunk, mostly toothless, sailor is being dragged by
    the scruff of the neck and thrown out the door.

    {Fore.LIGHTGREEN_EX}'And STAY OUT!' shouts the Innkeeper{Style.RESET_ALL}
    as he spots you and the {Fore.LIGHTCYAN_EX}Stranger{Style.RESET_ALL}.\n""")
    if player.height == "short":
        print(f"""{Fore.LIGHTGREEN_EX}
'Awoite shortarse, in or out. Same goes for your creepy mate.'""")
    elif player.height == "tall":
        print(f"""{Fore.LIGHTGREEN_EX}
'Awoite lanky, in or out. Same goes for your creepy mate.'""")
    elif player.height == "average":
        print(f"""{Fore.LIGHTGREEN_EX}
'Awoite average Joe, in or out. Same goes for your creepy mate.'""")

    print(f"""
The {Fore.LIGHTCYAN_EX}Stranger{Style.RESET_ALL} bows,
wishes you luck, and takes his leave.
""")
    print(f"You enter {Fore.CYAN}The Tavern...{Style.RESET_ALL}")
    press_enter_to_continue()


def tavern_options(player):
    """
    Includes all choices user can make in the tavern
    """
    min_bet = 1

    while True:
        print("What would you like to do?")
        print(f"""
1. Drink ale (increases minimum bet)
2. Bet on a game of {Fore.CYAN}dice{Style.RESET_ALL}
3. Bet on a {Fore.CYAN}coin flip{Style.RESET_ALL}
4. Listen out for info on treasure
5. Head for {Fore.CYAN}The Castle{Style.RESET_ALL} (available after 4.)
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
                print("\nYou've already heard about the treasure.\n")
        elif choice == "5":
            if player.heard_info:
                print(f"""
You head for {Fore.CYAN}The Castle{Style.RESET_ALL}!""")
                press_enter_to_continue()
                guard_interaction(player)
                break  # Loop ends here to move onto next phase
            else:
                print("\nYou need to gather information first.")
                press_enter_to_continue()
        else:
            print("Invalid option, please choose 1-5.")


def drink_ale(player, min_bet):
    """
    Drink ale and increase minimum bet.
    """
    print("\nYou drink a frothy ale. The room spins slightly.\n")
    min_bet *= 2
    player.ales_drank += 1
    print(f"Your new minimum bet is now {min_bet} gold.")
    press_enter_to_continue()
    return min_bet


def bet_game(player, min_bet, game):
    """
    Handle betting on dice or coin flip,
    allowing the player to choose their bet.
    """
    # Blocker so player can't attempt to bet with no gold
    if player.gold <= 0 | player.gold < min_bet:
        print(f"""
\nNot enough gold ({player.gold}) to cover your min bet ({min_bet}).""")
        print("\nYou can't place any bets.\n")
        press_enter_to_continue()
        return

    print("""
In each game, if you win, you earn what you staked. If not, you lose it.
""")

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
            bet = int(get_input_with_length(f"""
How much would you like to bet? (min: {min_bet}, max:{player.gold}): \n"""))
            if min_bet <= bet <= player.gold:
                return bet
            else:
                print(f"""
You must bet at least {min_bet} and no more than {player.gold}.""")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid number.")


def dice_game(player, bet):
    """
    Handle the dice game logic where the player rolls against the Innkeeper.
    """
    print(f"""
You challenge the {Fore.LIGHTGREEN_EX}Innkeeper{Style.RESET_ALL} to dice.
""")
    print("\nIf you roll higher you win.")
    player_roll = random.randint(1, 6)
    keeper_roll = random.randint(1, 6)
    print(f"""
You rolled {player_roll}.
The {Fore.LIGHTGREEN_EX}Innkeeper{Style.RESET_ALL} rolled {keeper_roll}.
""")

    if player_roll > keeper_roll:
        player.gold += bet
        player.dice_wins += 1
        print(f"""
{Fore.GREEN}{Style.BRIGHT}You win {bet} gold!{Style.RESET_ALL}
You now have {player.gold} gold pieces.""")
        press_enter_to_continue()
    else:
        player.gold -= bet
        player.dice_losses += 1
        print(f"""
{Fore.RED}You lose {bet} gold!{Style.RESET_ALL}
You now have {player.gold} gold pieces.""")
        press_enter_to_continue()


def coin_flip_game(player, bet):
    """
    Handle the coin flip game where the player calls heads or tails.
    """
    print(f"""
You bet the {Fore.LIGHTGREEN_EX}Innkeeper{Style.RESET_ALL}
that you can call a coin toss.
""")

    while True:
        call = get_input_with_length("""
Call the coin flip! (heads or tails):
""").lower()
        if call not in ["heads", "tails"]:
            print(f"\n{Fore.RED}Please input 'heads' or 'tails'.")
        else:
            break

    coin = random.choice(["heads", "tails"])
    print(f"\nThe coin landed on {coin}.")

    if call == coin:
        player.gold += bet
        player.coin_wins += 1
        print(f"""
{Fore.GREEN}{Style.BRIGHT}You win {bet} gold!{Style.RESET_ALL}
You now have {player.gold} gold pieces.""")
        press_enter_to_continue()
    else:
        player.gold -= bet
        player.coin_losses += 1
        print(f"""
\n{Fore.RED}You lose {bet} gold!{Style.RESET_ALL}
You now have {player.gold} gold pieces.""")
        press_enter_to_continue()


def listen_for_treasure_info(player):
    """
    Player listens out for treasure information.
    """
    print(f"""
You overhear a {Fore.LIGHTYELLOW_EX}Drunken Smuggler{Style.RESET_ALL}
talking about {Fore.RED}{Style.BRIGHT}The Beast Lord's Castle{Style.RESET_ALL}.
""")
    print(f"""
{Fore.LIGHTYELLOW_EX}*Hiccup* 'That bloody Guard!' *Hiccup*
'I tell ya, he's got some bloody gaul!'
'Trying to take me for 30 pieces!? Pah!'
'Doesn't he know...
that I know...
which he don't know...
but I do that there's...'""")
    print("\nThe smuggler takes a moment to belch loudly.\n")
    print(f"{Fore.LIGHTYELLOW_EX}")
    print(f"""
{Fore.LIGHTYELLOW_EX}""")

    print(f"""
{Fore.LIGHTYELLOW_EX}'A bloody Secret Passageway!
In the shadows to the east side of The Castle!'
'Shhhh!' *Hiccup* 'Trade secret that is!'""")
    print("He shouts, seemingly to himself.")
    print("His eyes droop closed, and the smuggler begins to snore loudly.")
    press_enter_to_continue()
    return True


# Entering the castle
def guard_interaction(player):
    """
    Player approaches castle gate and is pestered for a bribe.
    Handles whether the player can afford the bribe
    or needs to search for another way.
    """
    initial_dialogue_guard(player)
    handle_guard_bribe(player)


def handle_guard_bribe(player):
    """
    Handle the player's choice to bribe the guard if they can afford it.
    """
    bribe_required = 30
    if player.gold >= bribe_required:
        while True:  # While loop to fix Game Over logic
            give_bribe = get_input_with_length(f"""
You have {player.gold} gold.
Bribe {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL}?
(yes / no): \n""").lower()
            if give_bribe == "yes":
                process_bribe(player)
                break
            elif give_bribe == "no":
                reject_bribe()
                break
            else:
                print(f"{Fore.RED}Invalid input, please write yes or no.")
    else:
        handle_insufficient_gold(player)


def process_bribe(player):
    """
    Process the player's successful bribe of the guard.
    """
    player.guard_bribed += 1
    print(f"""
{Fore.LIGHTMAGENTA_EX}'Pleasure doing business wif ya. Now move along.
Before I change my mind.'""")
    print(f"\nYou enter {Fore.CYAN}The Castle...{Style.RESET_ALL}")
    press_enter_to_continue()
    final_showdown(player)


def reject_bribe(player):
    """
    Handle the player's rejection of the bribe offer.
    """
    print(f"""
{Fore.LIGHTMAGENTA_EX}'Watchu wasting my time for then pillock.
Sling yer hook.'""")
    print("\nHead held high and moral superiority assured,")
    print("you slink off in search of the passageway.")
    press_enter_to_continue()
    secret_entry_full_sequence(player)


def handle_insufficient_gold(player):
    """
    Handle the case where the player cannot afford the bribe.
    """
    print("You empty your pockets.")
    print("\nYou pick a button from one, and a moth flies from the other.")
    print(f"\nYou have {player.gold} gold and can't afford the bribe.")
    print(f"""
{Fore.LIGHTMAGENTA_EX}'Watchu wasting my time for then pillock.
Sling yer hook.'\n""")

    if player.gold > 0:
        # If player has gold left they can return to the tavern to make more
        offer_tavern_option(player)
    else:
        print(f"""
You get out of sight of the {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL}
to search for The Secret Passageway.""")
        press_enter_to_continue()
        secret_entry_full_sequence(player)


def offer_tavern_option(player):
    """
    Offer the player the choice to return to the tavern to earn more gold.
    """
    while True:
        earn_more_gold = get_input_with_length("""
Return to Tavern to win more gold? (yes/no): \n""").lower()
        if earn_more_gold == "yes":
            return_to_tavern(player)
            break
        elif earn_more_gold == "no":
            print(f"""
You get out of the {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL}'s sight
to search for {Fore.CYAN}The Secret Passageway{Style.RESET_ALL}.""")
            press_enter_to_continue()
            secret_entry_full_sequence(player)
            break
        else:
            print(f"{Fore.RED}Invalid input, please write yes or no.")


def return_to_tavern(player):
    """
    Handle the player's decision to return
    to the tavern to gamble for more gold.
    """
    print(f"""
Returning to {Fore.CYAN}The Tavern{Style.RESET_ALL}...""")
    press_enter_to_continue()
    player.heard_info = True  # No need to re-listen for info
    tavern_options(player)


def initial_dialogue_guard(player):
    """
    Starting dialogue with guard
    """
    print(f"""
You spot a {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL} posted at the gate.
""")
    print("His head droops as he appears on the verge of nodding off.")
    print("A branch breaks under your foot and he jolts awake.")
    if player.sex == "woman":
        print(f"""
You hear a long wolf whistle from {Fore.LIGHTMAGENTA_EX}The Guard.

'Well, well, well. It must be my lucky day! Not often fine young ladies
like yourself be approaching MY turf. You 'ere to keep me company?'
{Style.RESET_ALL}
Through browned and blackened teeth he gives you his best smile.

You try your best to hide your anger and disgust
but the {Fore.LIGHTMAGENTA_EX}Guard{Style.RESET_ALL} must spot it
on your face as his own expression hardens.
{Fore.LIGHTMAGENTA_EX}
'You want in, it'll cost ya like everyone else. 30 pieces.
Otherwise, clear off!'""")
        press_enter_to_continue()
    else:
        print(f"""
{Fore.LIGHTMAGENTA_EX}'Well, well, well. It must be my lucky day!
You 'ere to keep me company?'{Style.RESET_ALL}

Through browned and blackened teeth the {Fore.LIGHTMAGENTA_EX}Guard
{Style.RESET_ALL} gives you a sinister smile.

{Fore.LIGHTMAGENTA_EX}'You want in, it'll cost ya. 30 pieces.
Otherwise, clear off!'""")
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
    print(f"""
You sneak into the shadows and find the passageway on the east side.
You find a narrow, dark passageway that spirals downward into the earth.
The air grows colder and damper as you descend.
Suddenly, a booming voice echoes in the darkness...
{Fore.LIGHTGREEN_EX}{Style.BRIGHT}
'WHO DARES TO ENTER MY DOMAIN?!'{Style.RESET_ALL}""")
    press_enter_to_continue()
    troll_encounter(player)


def troll_encounter(player):
    """
    Initiates the troll encounter with a riddle game.
    """
    print(f"""
A massive, hulking figure steps out of the shadows.
It's a {Fore.LIGHTGREEN_EX}{Style.BRIGHT}Troll{Style.RESET_ALL}!
He blocks your path.
{Fore.LIGHTGREEN_EX}{Style.BRIGHT}
'If you want to pass, you must answer my riddles!'
{Style.RESET_ALL}
the {Fore.LIGHTGREEN_EX}{Style.BRIGHT}Troll{Style.RESET_ALL} growls.
{Fore.LIGHTGREEN_EX}{Style.BRIGHT}'Or else... you'll be my dinner.'
""")
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

    print(f"""{Fore.LIGHTGREEN_EX}{Style.BRIGHT}
The Troll{Style.RESET_ALL} asks you three riddles.""")

    for riddle in riddles:
        print(f"""
Riddle: {Fore.LIGHTGREEN_EX}{Style.BRIGHT}{riddle['question']}""")
        answer = get_input_with_length("What is your answer? \n").lower()
        if answer == riddle["answer"]:
            print(Fore.GREEN + Style.BRIGHT + "\nCorrect!")
            player.rid_won += 1
        else:
            player.rid_lost += 1
            print(f"""
{Fore.RED}Wrong!{Style.RESET_ALL}
The correct answer was: {riddle['answer']}""")
            # Simple right or wrong validation

    if player.rid_won >= 2:
        print(f"""{Fore.LIGHTGREEN_EX}{Style.BRIGHT}
The Troll{Style.RESET_ALL} grunts, impressed.
{Fore.LIGHTGREEN_EX}{Style.BRIGHT}
'Fine, you may pass.'{Style.RESET_ALL}""")
        press_enter_to_continue()
        final_showdown(player)
    else:
        print(f"""{Fore.LIGHTGREEN_EX}{Style.BRIGHT}
The Troll{Style.RESET_ALL} roars with laughter.
{Fore.LIGHTGREEN_EX}{Style.BRIGHT}'You're too foolish to proceed!'
{Style.RESET_ALL}""")
        print(f"""{Fore.RED}
The Troll leaps, grabs, and gobbles you up whole.
A belch echoes through the catacombs.""")
        press_enter_to_continue()
        game_over(player)


# Final Showdown in the castle
def final_showdown(player):
    beast_lord_speech()
    rps_battle(player)


def beast_lord_speech():
    """
    The Beast Lord delivers a dramatic
    speech before the final challenge.
    """
    print(f"""
You make your way into the heart of The Castle and approach the throne room.
The great doors creak open, and there he stands -

{Fore.RED}{Style.BRIGHT}The Beast Lord{Style.RESET_ALL}.

A towering figure of shadow and flame.
His eyes burn with malice and hunger for power.

{Fore.RED}{Style.BRIGHT}'Ah, another brave fool comes to claim my throne.
Do you think you are worthy, mortal?
Many have come before you, but none have succeeded.""")
    press_enter_to_continue()
    print(f"""
He pauses, letting the weight of his words sink in.
{Fore.RED}{Style.BRIGHT}
'Know this - those who defeat me shall rule these lands,
taking all that is mine. But should you fail, your soul will
be forfeit, and you will suffer a fate worse
than death itself.'""")
    press_enter_to_continue()
    print(f"""He gestures toward you with a clawed hand, his grin widening.
{Fore.RED}{Style.BRIGHT}
'Prepare yourself. You face a challenge of wits and reflexes.
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
    turn = 0

    print(f"""
{Fore.RED}{Style.BRIGHT}The Beast Lord{Style.RESET_ALL} readies himself...
""")

    while player.rps_won < 2 and player.rps_lost < 2:
        turn += 1
        print(f"Turn: {turn}\n")
        player_move = get_input_with_length("""
        Choose your move (rock, paper, scissors):
        """).lower()
        if player_move not in moves:
            turn -= 1  # Stops invalid entries from adding to turn count
            print(Fore.RED + "Please choose rock, paper, or scissors.")
            continue

        beast_move = random.choice(moves)
        print(f"""{Fore.RED}{Style.BRIGHT}
The Beast Lord{Style.RESET_ALL} chooses {beast_move}.\n""")

        # Determine winner
        if player_move == beast_move:
            print("It's a tie!")
        elif (player_move == "rock" and beast_move == "scissors") or \
             (player_move == "paper" and beast_move == "rock") or \
             (player_move == "scissors" and beast_move == "paper"):
            print(Fore.GREEN + Style.BRIGHT + "You win this round!")
            player.rps_won += 1
        else:
            print(f"""{Fore.RED}{Style.BRIGHT}
The Beast Lord{Style.RESET_ALL} {Fore.RED}wins this round!""")
            player.rps_lost += 1

        print(f"""
        Score - You: {player.rps_won}, {Fore.RED}{Style.BRIGHT}
        Beast Lord{Style.RESET_ALL}: {player.rps_lost}\n""")

    # Determine final outcome
    if player.rps_won == 2:
        print(f"""{Fore.GREEN}{Style.BRIGHT}You've done it!{Style.RESET_ALL}
        {Fore.RED}{Style.BRIGHT}
        The Beast Lord{Style.RESET_ALL} {Fore.GREEN}{Style.BRIGHT}has fallen.

        You are victorious!""")
        press_enter_to_continue()
        concluding_dialogue(player)
        game_over(player)
    else:
        print(f"""{Fore.RED}{Style.BRIGHT}
        The Beast Lord{Style.RESET_ALL} cackles triumphantly.
        {Fore.RED}You have been defeated.""")
        press_enter_to_continue()
        print(f"""{Fore.RED}You feel an eerie tingle.

And a chill creeps up your spine as your soul is severed from your body.""")
        press_enter_to_continue()
        game_over(player)


def concluding_dialogue(player):
    """
    Story Conclusion
    """
    print("Countless treasures are yours. The prophecy is fulfilled.")
    print(f"""
{Fore.LIGHTBLUE_EX}A brave, {player.height}, {player.sex} sits upon the
throne {Style.RESET_ALL}.""")
    press_enter_to_continue()
    print(f"""Years pass in relative peace.

    Initially you rule fairly, but you feel unexplainable change over time.

    {Fore.RED}{Style.BRIGHT}'The people must know their place'{Style.RESET_ALL}

    you hear as a whisper in the air.""")
    press_enter_to_continue()
    print("""As Lord:

    You raise taxes, ban public gatherings, except executions, and violently
    crush any threats to your rule, perceived or otherwise.""")
    press_enter_to_continue()
    print(f"""
How long has it been since you took {Fore.CYAN}The Castle{Style.RESET_ALL}?

Decades?

You can't remember.""")
    press_enter_to_continue()
    print(f"""
A spike of terror runs through you!
{Fore.RED}{Style.BRIGHT}
The Beast Lord{Style.RESET_ALL} appeared in the corner
of your eye.

You're sure of it.""")
    print("""
You leap with teeth bared toward the spot where you saw your old enemy.""")
    print("\nIt's a broken mirror.")
    print("""
You see the beastly reflection of your jagged teeth
and knifelike fingernails.""")
    print("\nYou realise what you have become...")
    press_enter_to_continue()
    print("The doors of your throne room burst open.")
    print(f"""{Fore.LIGHTBLUE_EX}
A brave, {player.height}, {player.sex}{Style.RESET_ALL} rushes in and exclaims:
{Fore.LIGHTWHITE_EX}{Style.BRIGHT}
'Your evil reign ends now {Fore.RED}{Style.BRIGHT}Beast Lord{Style.RESET_ALL}!'
""")
    print("A more human part of you deep down almost starts to laugh.")
    print("But the influence of the beast drowns that out.")
    print("Involuntarily you begin the speech.")
    print(f"""
    {Fore.RED}{Style.BRIGHT}'A brave fool comes to claim my throne?!
    Do you think you are worthy, mortal?'""")
    print("\n...")
    press_enter_to_continue()


# Main
def main():
    """
    Main function where all other required functions will be called
    """
    player = intro()
    tavern(player)
    guard_interaction(player)


# Call main and play the game
main()
