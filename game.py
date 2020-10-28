"""
    This module is used to start the game and control the user actions
"""
import board as Board

if __name__ == '__main__':
    print("Play American Checkers")
    print("Select the board configuration you want to play")
    try:
        board_created = False
        while(not board_created):
            numOfSquares = int(input("1. 6x6 \t2. 8x8 \t3.10x10 \n"))
            if(numOfSquares == 1):
                board = Board.Board(6)
                break
            elif(numOfSquares == 2):
                board = Board.Board(8)
                break
            elif(numOfSquares == 3):
                board = Board.Board(10)
                break
        print(board)
    except Exception as e:
        print(f"Error Occurred: {e}")