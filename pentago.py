import numpy as np
import random

ROW = 6
COL = 6
WIN = 5
#creating gameboard, and filling (row, column) with 0 by default 
game_board = np.zeros((ROW, COL), dtype=int)

#returns True if board is fully filled up
def check_board_full(board):
        for r in range(ROW):
            for c in range(COL):
                if board[r, c] == 0:
                    return False
        return True

#check if winning conditions are met, assuming rotation is already done
def check_victory(board, turn, rot):
#return 0 for no outcome, 1 for player 1's victory, 2 for player 2's victory, and 3 for draw

    def check_win(board_check):
        #boolean for whether player 1 and 2 have met winning condition
        #False means no win, True means win
        current_player = False
        other_player = False
        for r in range(ROW):
            #only checking from col 0 & 1 since 5 consecutive marbles can only start from col 1 & 2
            for c in range(2):
                x = board_check[r, c]
                #only check for 5 in a row if the first space is filled with a marble
                if x != 0:
                    #x is the first marble, hence counter 1
                    counter = 1
                    #check for 5 consecutive same marbles
                    for i in range(1, WIN):
                        if board_check[r, c + i] != x:
                            break
                        else:
                            counter += 1
                    #counter should be 5 if 5 consecutive marbles are detected
                    if counter == WIN:
                        if x == turn:
                            current_player = True
                        else:
                            other_player = True
        
        #check for vertical
        for c in range(COL):
            #only checking from col 0 & 1 since 5 consecutive marbles can only start from col 1 & 2
            for r in range(2):
                x = board_check[r, c]
                if x != 0:
                    counter = 1
                    for i in range(1, WIN):
                        if board_check[r + i, c] != x:
                            break
                        else:
                            counter += 1
                    if counter == WIN:
                        if x == turn:
                            current_player = True
                        else:
                            other_player = True
        
        #check for diagonals from top left  
        for r in range(2):
            for c in range(2):
                x = board_check[r, c]
                if x != 0:
                    counter = 1
                    for i in range(1, WIN):
                        if board_check[r + i, c + i] != x:
                            break
                        else:
                            counter += 1
                    if counter == WIN:
                        if x == turn:
                            current_player = True
                        else:
                            other_player = True

        #check for diagonals from top right 
        for r in range(2):
            for c in range(4, COL):
                x = board_check[r, c]
                if x != 0:
                    counter = 1
                    for i in range(1, WIN):
                        if board_check[r + i, c - i] != x:
                            break
                        else:
                            counter += 1
                    if counter == WIN:
                        if x == turn:
                            current_player = True
                        else:
                            other_player = True

        #both players have not won and board is not yet full
        if (current_player == False and other_player == False) and check_board_full(board) == False:
            return 0
        #current player has won
        elif current_player == True and other_player == False:
            return turn
        #other player has won
        elif other_player == True and current_player == False:
            return (3 - turn)
        #situation 1: none of the players have won and the board is full
        #situation 2: both players have won at the same time
        #both situations result in a draw
        else:
            return 3

    #check for winning condition after move(placement + rotation) applied
    second_check = check_win(board)

    #can input parameter rot as 0 to only check for board after rotation 
    if rot == 0:
        return second_check 

    board_copy = board.copy()
    #reversing rotation 
    if rot in [1, 3, 5, 7]:
        rotate(board_copy, rot+1)
    if rot in [2, 4, 6, 8]:
        rotate(board_copy, rot-1)

    #check for winning condition before rotation approved
    first_check = check_win(board_copy)

    #if win is reached before rotation, rotation is not applied hence first check is returned instead
    if (first_check == 1 or first_check == 2):
        return first_check
    
    return second_check
       

#top left row and col refers to that of the quadrant that the rotation is being applied to
def rotation(board, rot, top_left_row, top_left_col):
    
    #make a copy of current gameboard
    board_copy = board.copy()

    #make list of row and col indexes of the perimeter of each quadrant in a clockwise manner starting from the top left space
    row_list = [top_left_row]*3 + [top_left_row + 1] + [top_left_row + 2]*3 + [top_left_row + 1]
    col_list = [top_left_col, top_left_col + 1] + [top_left_col + 2]*3 + [top_left_col + 1] + [top_left_col]*2

    #make copies of row and col lists to apply rotation to 
    row_list_copy = row_list.copy()
    col_list_copy = col_list.copy()

    def swap_values(insert_index, remove_index):
        for x in range(2):
            row_list_copy.insert(insert_index, row_list_copy.pop(remove_index))
            col_list_copy.insert(insert_index, col_list_copy.pop(remove_index))
        #swapping gameboard values with previous values at the same spots
        for ori_row, new_row, ori_col, new_col in zip(row_list, row_list_copy, col_list, col_list_copy):
            board[ori_row, ori_col] = board_copy[new_row, new_col]

    #clockwise rotation, last element in list is moved to the front twice
    if rot in (1, 3, 5, 7):
        swap_values(0, 7)
    #anticlockwise rotation, first element in list is moved to the back twice
    if rot in (2, 4, 6, 8):
        swap_values(8, 0)


#decides how to rotate board based on rotation value
def rotate(board, rot):
    #rotates top right sub-board
    if rot == 1 or rot == 2:
        rotation(board, rot, 0, 3)
    #rotates bottom right sub-board
    if rot == 3 or rot == 4:
        rotation(board, rot, 3, 3)
    #rotates bottom left sub-board
    if rot == 5 or rot == 6:
        rotation(board, rot, 3, 0)
    #rotates top left sub-board
    if rot == 7 or rot == 8:
        rotation(board, rot, 0, 0)
    

def apply_move(board, turn, row, col, rot):

    if check_move(board, row, col) == True:
        #create new output board
        board_new = board.copy()
        #placement of marble
        board_new[row, col] = turn

        #checking for win before rotation
        if (check_victory(board_new, turn, 0) == 1 or check_victory(board_new, turn, 0) == 2):
            print("Rotation not applied as game is decided before rotation")
        else:
            #rotation of sub-board only if there was no win before rotation
            rotate(board_new, rot)
    
    #returns updated board with move applied
    return board_new


def check_move(board, row, col):
    #check if space is empty and it is on the board, return True if it is
    if (board[row, col] == 0 and (row >= 0 and row <= 5) and (col >= 0 and col <= 5)):
        return True
    return False


def computer_move(board, turn, level):
    '''
    Level 1: random computer player. To start, program a trivial strategy: each time he will have to play, the
    computer player will randomly choose a move among all the possible random moves (row, column and rotation
    choices). You can test that this player is easy to beat.
    '''
    def random_move():
        while True:
            #generates random integer for row, col and rot respectively and return it if the space is empty
            r = random.randint(0, 5)
            c = random.randint(0, 5)
            rot = random.randint(1, 8)
            if board[r, c] == 0:
                return [r, c, rot]
            #re-generate integers if space is filled
            else:
                continue

    if level == 1:
        #returns random move
        return random_move()

    '''
    Level 2: medium computer player. Program a computer player that will necessarily play a move that leads
    to a direct win for him if such a move exists. If no such move exist, it will avoid to play a move that leads to a
    direct win for his adversary in the next round (if such a move exist for the adversary). If again no such move
    exist, the computer player will simply pick a random valid move
    '''

    if level == 2:
        all_options = []

        #add all possible moves to list all_options
        def find_options():
            for r in range(ROW):
                for c in range(COL):
                    for rot in range (1, 9):
                        if board[r, c] == 0:
                            all_options.append([r, c , rot])

        find_options()

        #list of offennsive moves computer can make
        attack_options = []
        #list of defensive moves computer can make 
        defend_options = []
        for option in all_options:
            #creates a copy of the board to try every move in all_options for computer
            copy1 = board.copy()
            #creates a copy of the board to try every move in all_options for player
            copy2 = board.copy()

            #applies move on computer's board copy
            copy1[option[0], option[1]] = turn
            rotate(copy1, option[2])

            #applies move on player's board copy
            copy2[option[0], option[1]] = abs(turn - 1)
            rotate(copy2, option[2])
            
            #once a move is found that leads to a victory for the computer, add it to attack_options and break
            if check_victory(copy1, turn, option[2]) == turn:
                attack_options.append(option)
                break
            #once a move is found that leads to a victory for the player, add it to defend_options and break
            elif check_victory(copy2, abs(turn - 3), option[2]) == abs(turn - 3):
                defend_options.append(option)
                break
        
        #execute offensive moves if any 
        if len(attack_options) > 0:
            x = attack_options[0]
            return [x[0], x[1], x[2]]
        #execute any defensive moves if no offensive moves, flipping the rotation in respective sub-boards
        elif len(defend_options) > 0:
            x = defend_options[0]
            if x[2] in [1, 3, 5, 7]:
                x[2] += 1
            if x[2] in [2, 4, 6, 8]:
                x[2] -= 1
            return [x[0], x[1], x[2]]
        #if no offensive or defensive moves, play a random move
        else:
            return random_move()

def display_board(board):
    for row in range(ROW):
        for col in range(COL):
           print(board[row, col], end = '    ')
        #to seperate the rows 
        print("\n")
    #just to seperate gameboards after moves are played
    print("--------------------------")

#include values x to y, z is the string
def input_number (x, y, z):

    while True:

        try:
            number = int(input(z))
            
            #if integer out of range, re-prompt
            if (number < x or number > y):
                    raise ValueError

            #if integer is inputted, and its range, return number and exit loop
            return number
        
        #if user does not input an integer
        except ValueError:
           print("Please enter a valid integer within the range!")
           continue

def menu():
    global game_board
    print("Welcome to Pentago!")

    while True:
        #prompt for whether player wants to go against another player or computer
        choice = (input("PvP or Computer: ")).upper()
        
        if choice == "PVP":
        
            print("Player 1 will go first")
        
            player_1 = input("Player 1, please input your name: ")
            player_2 = input("Player 2, please input your name: ")
        
            print("This is the empty starting game board!")
            display_board(game_board)
        
            #equals true and ends program if an endgame is reached
            end_game = False

            while end_game == False:
                for turn in range (1, 3):
                    if turn == 1: 
                        print("It is now " + player_1 + "'s turn!")
                    if turn == 2: 
                        print("It is now " + player_2 + "'s turn!")
                    while True:
                        row = input_number(0, 5, "Input a row from 0 to 5: ")
                        col = input_number(0, 5, "Input a column from 0 to 5: ")
                        rot = input_number(1, 8, "Input a rotation value from 1 to 8: ")
                        #checks if space is empty, and re-prompts if not
                        if check_move(game_board, row, col) == True:
                            if turn == 1: 
                                print(f"{player_1} placed a marble at row {row}, column {col} and did rotation {rot}")
                            if turn == 2: 
                                print(f"{player_2} placed a marble at row {row}, column {col} and did rotation {rot}")
                            break
                        else:
                            print("That space is already taken! Please choose another row and column!")
                            continue
                    
                    #saves updated board after move is applied
                    updated_gameboard = apply_move(game_board, turn, row, col, rot)      
                    #changes current board to updated one
                    game_board = updated_gameboard

                    display_board(game_board)

                    #continue with loop as long as endgame is not reached 
                    if check_victory(game_board, turn, rot) == 0:
                        continue
                    else:
                        if check_victory(game_board, turn, rot) == 1:
                            print(player_1 + " has won!")
                        elif check_victory(game_board, turn, rot) == 2:
                            print(player_2 + " has won!")
                        #check_victory returns 3
                        else:
                            print("Game has ended in a draw")
                        end_game = True
                    
                    #to exit loop if endgame is reached after first turn
                    if end_game == True:
                        break
            
            #to exit loop prompting for choice since a valid choice has been selected
            break

        elif choice == "COMPUTER":
            player = input("Player, please input your name: ")
            level = int(input("Please choose ur difficulty level, 1 or 2: "))
            #generating whether player or computer will go first
            player_turn = random.randint(1, 2)
            com_turn = (3 - player_turn)
            
            if player_turn == 1:
                print(player + " will be going first and computer will be going second.")
            else:
                print("computer will be going first and " + player + " will be going second.")
            
            print("This is the empty starting game board!")
            display_board(game_board)
    
            end_game = False
            
            while end_game == False:
                for turn in range (1, 3):
                    if player_turn == turn: 
                        print("It is now " + player + "'s turn!")
                        while True:
                            row = input_number(0, 5, "Input a row from 0 to 5: ")
                            col = input_number(0, 5, "Input a column from 0 to 5: ")
                            rot = input_number(1, 8, "Input a rotation value from 1 to 8: ")
                            if check_move(game_board, row, col) == True:
                                print(f"{player} placed a marble at row {row}, column {col} and did rotation {rot}")
                                break
                            else:
                                print("That space is already taken! Please choose another row and column!")
                                continue

                        updated_gameboard = apply_move(game_board, turn, row, col, rot)      
                        game_board = updated_gameboard

                        display_board(game_board)
                    
                        if check_victory(game_board, turn, rot) == 0:
                            continue
                        else:
                            if check_victory(game_board, turn, rot) == player_turn:
                                print(player + " has won!")
                            elif check_victory(game_board, turn, rot) == com_turn:
                                print("The computer has won!")
                            #check_victory returns 3
                            else:
                                print("Game has ended in a draw")
                            end_game = True

                        if end_game == True:
                            break

                    if com_turn == turn:
                        
                        print("It is now the computer's turn!")
                        
                        #saves the computer's move under variable move
                        move = computer_move(game_board, com_turn, level)
                        
                        print(f"The computer placed a marble at row {move[0]}, column {move[1]} and did rotation {move[2]}")

                        updated_gameboard = apply_move(game_board, turn, move[0], move[1], move[2])      
                        game_board = updated_gameboard

                        display_board(game_board)
                    
                        if check_victory(game_board, turn, move[2]) == 0:
                            continue
                        else:
                            if check_victory(game_board, turn, move[2]) == com_turn:
                                print("The computer has won!")
                            elif check_victory(game_board, turn, move[2]) == player_turn:
                                print(player + " has won!")
                            #check_victory returns 3
                            else:
                                print("Game has ended in a draw")
                            end_game = True
                        
                        if end_game == True:
                            break
                        
            break    
    
        else:
            print("Invalid Input! Type either Pvp or Computer!")
            #in order to keep prompting as long as input is not pvp or computer
            continue

if __name__ == "__main__":
    menu()