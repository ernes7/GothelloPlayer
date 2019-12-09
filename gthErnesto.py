#!/usr/bin/python3

# Ernesto Martinez
# Minimax Search Alpha-Beta Prunning
# To play vs Gothello client.
import random
import sys

import gthclient

me = sys.argv[1]
opp = gthclient.opponent(me)

client = gthclient.GthClient(me, "barton.cs.pdx.edu", 0)


def letter_range(letter):
    for i in range(5):
        yield chr(ord(letter) + i)

board = {letter + digit
         for letter in letter_range('a')
         for digit in letter_range('1')}

grid = {"white": set(), "black": set()}

def show_position():
    for digit in letter_range('1'):
        for letter in letter_range('a'):
            pos = letter + digit
            if pos in grid["white"]:
                piece = "O"
            elif pos in grid["black"]:
                piece = "*"
            else:
                piece = "."
            print(piece, end="")
        print()

side = "black"


#positions to move around:
posDigit = 0
posLetter = 0
# Function to maximize score our score (playing black = *)
def max():
    # values for the maxScore
    # -1 worst score
    # 1 Best Score
    # 0 in case there is tie

    maxScore = -1 # set to worst case first

    for digit in letter_range('1'):
        for letter in letter_range('a'):
            if grid[digit][letter] == '.':
                #if nothing we play black and call min()
                grid[digit][letter] = '*' #black
                (move, minDigit, minLetter) = min()

                # Adjusting max score after return
                if move > maxScore:
                    maxScore = move
                    posDigit = minDigit
                    posLetter = minLetter

                # After we know the max score for the move, 
                # the location is set back to what it was
                grid[digit][letter] = '.'
    return (maxScore,posDigit,posLetter)

       

# Function to minimize opponent's score ( playing white = O) 
def min():

    # the logic for minimum score is reversed
    minScore = 1 # its the worst score for the other player.
    # Since it will means the best score for us.

    #positions for the client moving:
    ClientDigit = 0
    ClientLetter = 0

    for digit in letter_range('1'):
        for letter in letter_range('a'):
            if grid[digit][letter] == '.':
                # simulates client move to get score
                grid[digit][letter] = 'O' #white
                (move, maxDigit, maxLetter) = max()

                # Adjusting max score after return
                if move < minScore:
                    minScore = move
                    ClientDigit = maxDigit
                    ClientLetter = maxLetter

            # After we know the min score for the move, 
            # the location is set back to what it was
                grid[digit][letter] = '.'
    return (minScore,ClientDigit,ClientLetter)


while True:
    show_position()
    if side == me:
        #move = random.choice(list(board))
        (move, posDigit,posLetter) = max() # get max possible score
        grid[posDigit][posLetter] = '*' # black move in the position

        print("me:", move)
        try:
            client.make_move(move)
            grid[me].add(move)
            board.remove(move)
        except gthclient.MoveError as e:
            if e.cause == e.ILLEGAL:
                print("me: made illegal move, passing")
                client.make_move("pass")
    else:
        cont, move = client.get_move()
        print("opp:", move)
        if cont and move == "pass":
            print("me: pass to end game")
            client.make_move("pass")
            break
        else:
            if not cont:
                break
            board.remove(move)
            grid[opp].add(move)

    side = gthclient.opponent(side)