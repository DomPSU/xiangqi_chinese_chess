# Xiangqi Chinese Chess

This portfolio project was completed while taking Introduction to Computer Science II at Oregon State University.

The goal of the assignment was to create the logic and error handling for Xiangqi or Chinese Chess (https://en.wikipedia.org/wiki/Xiangqi). 

I fully tested functionality using the XiangiqiGameTester file and received a 100% on the assignment.

# Required Methods

An init method that initializes any data members.

A method called get_game_state that just returns 'UNFINISHED', 'RED_WON' or 'BLACK_WON'.

A method called is_in_check that takes as a parameter either 'red' or 'black' and returns True if that player is in check, but returns False otherwise.

A method called make_move that takes two parameters - strings that represent the square moved from and the square moved to. For example, make_move('b3', 'b10'). If the square being moved from does not contain a piece belonging to the player whose turn it is, or if the indicated move is not legal, or if the game has already been won, then it should just return False. Otherwise it should make the indicated move, remove any captured piece, update the game state if necessary, update whose turn it is, and return True.

# Example

game = XiangqiGame()  
move_result = game.make_move('c1', 'e3')  
black_in_check = game.is_in_check('black')  
game.make_move('e7', 'e6')  
state = game.get_game_state()  