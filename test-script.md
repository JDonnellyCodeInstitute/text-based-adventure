Text Based Adventure Test Script

Tests:

Action | Expectation | Pass/Fail
----- | ----- | -----
Introduction Tests |  | 
Run Program | User should see the introductory exposition as per intro() method | Pass
User is asked to input name | User can input their name and continue to the next question | Pass
User name input should be letters only | User will receive a notification advising them to only use letters in their name if they try to include non-letters | Pass
User is asked to input sex | Player is given 3 options, if they input one they proceed, if they input anything else they'll receive a validation notification | Pass
User is asked to input height | Player is given 3 options, if they input one they proceed, if they input anything else they'll receive a validation notification | Pass
The Player is created using the user's inputs | Player basic stats are displayed along with the call to adventure proving the player variable has been created and passed between the functions as required | Pass
User is asked to answer the Call to Adventure and responds 'yes' | The player adventure begins and the program continues toward the tavern | Pass
User is asked to answer the Call to Adventure and responds 'no' | The program proceeds toward Game Over functions | Pass
User is asked to answer the Call to Adventure and responds anything other than 'yes' or 'no' | User receives a validation error message | Pass
Game Over Tests |  | 
User incurs a Game Over | Page should display 'GAME OVER!', should list player stats, and should point users to the URL for the Adventure google sheets page | Pass
User incurs a Game Over | The adventurer google sheet connected to the project via API is updated with all the relevant player stats | Pass
User is asked if they want to Play again and says 'no' | Program should end along with a thanks for playing message | Pass
User is asked if they want to Play again and says 'yes' | Player should be asked if they want to restart with the same character | Pass
User is asked if they want to Play again and says neither 'yes' or 'no' | Player receives validation error message | Pass
User is asked if they want to Restart with same character and says 'yes' | Program should continue from the tavern section with the player object already created | Pass
User is asked if they want to Restart with same character and says 'new' | Program should continue from the intro section | Pass
User is asked if they want to Restart with same character and says neither 'yes' or 'new' | Player receives validation error message | Pass
Player properties relevant to game progression are reset when user restarts | Gold reverts to 10, heard_info to false, riddles and rps won to 0 | Pass
Input Length Validation |  | 
User should not be able to do inputs over 10 Characters | The get_input_with_length() was created to be used instead of standard inputs, it takes a parameter for number of characters which is set to ten. If user inputs more than 10 characters they will be notified that they are over the limit | Pass
Colorama Tests | |
User comes across coloured section of text | Colours should match those input in the source code | Pass
Tavern Tests |  | 
Tavern section begins and player height is short | User sees interaction with tavern keeper and is insulted for their height | Pass
Tavern section begins and player height is tall | User sees interaction with tavern keeper and is insulted for their height | Pass
Tavern section begins and player height is average | User sees interaction with tavern keeper and is insulted for their height | Pass
User should be given 5 options | Drink ale, bet on dice, bet on coin flip, listen for info, head for castle | Pass
User picks option 1 to drink ale | User minimum bet is doubled due to their dutch courage and they are returned to the option selection | Pass
User picks option 2 or 3 when they have zero gold | Player informed they can't place any bets | Pass
User picks option 2 or 3 when they have less gold than their minimum bet | Player informed they can't place any bets | Pass
User picks option 2 or 3 and tries to bet more than their total gold | Player is informed of their max and min bets and is prompted for their input again | Pass
User picks option 2 or 3 and inputs a non-number for their bet | Player receives validation error message | Pass
User picks option 2 and wins | Amount equal to their bet is added to their total gold | Pass
User picks option 2 and loses | Amount equal to their bet is subtracted from their total gold | Pass
User picks option 3 and wins | Amount equal to their bet is added to their total gold | Pass
User picks option 3 and loses | Amount equal to their bet is subtracted from their total gold | Pass
User picks option 3 and inputs anything other than 'heads' or 'tails' | Player receives validation error message | Pass
User picks option 4 for the first time | User hears info from a drunken smuggler | Pass
User picks option 4 any time after the first time | User notified that they've already heard about the treasure | Pass
User picks option 5 to head to the castle before they have completed option 4 | User informed they need to gather info first | Pass
User picks option 5 to head to the castle after they have completed option 4 | User proceeds to the castle | Pass
User inputs anything other than 1-5 | Player receives validation error message | Pass
Guard Interaction Tests |  |
User proceeds to the castle and is met by the guard as a woman | Terminal output is the guard creeping on the player | Pass
User proceeds to the castle and is met by the guard as a sex other than woman | Terminal output is the guard being sinister to the player | Pass
Player has 30 gold or more to bribe the guard | They are offered the choice to bribe the guard or not | Pass
When prompted to bribe the guard the user inputs 'yes' | Player is informed of their new gold amount, receives blunt farewell from the guard, and is prompted to proceed to the castle | Pass
When prompted to bribe the guard the user inputs 'no' | Player receives blunt response from the guard and goes in search of the secret passageway | Pass
When prompted to bribe the guard the user inputs anything other than 'yes' or 'no' | Player receives validation error message | Pass
User initiates the guard interaction without enough gold for the bribe but more than zero | Player receives a blunt dismissal from the guard then is offered the option to return to the tavern to win more gold | Pass
Player is asked if they want to return to the Tavern and says 'no' | Player proceeds to Secret Passageway | Pass
Player is asked if they want to return to the Tavern and says 'yes' | Player proceeds to tavern - they should not need to do the introductory dialogue nor listen for info again | Pass
Player is asked if they want to return to the Tavern and says anything other than 'yes' or 'no' | Player receives validation error message | Pass
User initiates the guard interaction with 0 gold | Player receives a blunt dismissal from the guard and proceeds to the secret passageway | Pass
Secret Passageway Tests |  |
Secret Passageway Section initiated | Terminal displays passageway introduction | Pass
The troll asks his riddle and user responds with correct answer | Player informed they were correct | Pass
The troll asks his riddle and user responds with incorrect answer | Player informed they were wrong and of the correct answer | Pass
The troll asks his riddle and user responds with anything other than letters | Validation error message | Pass
User gets at least two riddles correct | Troll lets them pass and they move on to the final boss | Pass
User gets at least two riddles incorrect | Troll eats the player and the user proceeds to the game over sequence | Pass
The Beast Lord Sequence Tests | |
Beast Lord Sequence begins | Beast Lord's speech is printed to the terminal | Pass
Rock Paper Scissors (RPS) begins - User inputs anything other than 'rock' 'paper' or 'scissors' | Validation error prints and they're asked again for input - Turn counter remains unchanged in the terminal | Pass
RPS user makes a valid input | Turn counter increases by 1 next turn | Pass
RPS user makes a valid input and wins | Notified in console they win the round, scores displayed | Pass
RPS user makes a valid input and loses | Notified in console they lose the round, scores displayed | Pass
RPS user makes a valid input and ties | Notified in console they draw the round, scores displayed | Pass
User wins two games of RPS | The console is populated with the closing sequence of text followed by a game over | Pass
User loses two games of RPS | Player gets a game over | Pass
PEP8 Validation Corrections | |
I run flake8 . in the terminal | Wide range of code smell issues appear. Line length, additional white space, unused variables, over-indentation. ALL CORRECTED | Pass

Browsers: 

Action | Expectation | Pass/Fail
----- | ----- | -----
Action all of the above tests in Google Chrome | All tests should pass | Pass
Action all of the above tests in Microsoft Edge | All tests should pass | Pass
Action all of the above tests in Firefox | All tests should pass | Pass