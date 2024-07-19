import time
import random
import numpy as np

# Setup core variables
Rows = 6
Columns = 7
Grid = np.zeros((Rows,Columns), dtype=int)

def PrintGrid(Grid):
    # Function to print game state
    # Easy Print
    #print(Grid)
    # Right Side Up Print
    for Row in range(Rows):
        print(Grid[Rows-Row-1])
    print("")
    return 0

def OpposingPlayer(Player):
    # Finds opposing player
    if Player == 1:
        return 2
    else:
        return 1

def Turn(Column, Player):
    # Function to verify that move is valid and updates game state
    # Returns 1 for valid move, 0 for invalid
    if Column < 7 and Column >= 0:
        for Row in range(Rows):
            if Grid[Row, Column] == 0:
                Grid[Row, Column] = Player
                return 1
    return 0

def UndoTurn(Column):
    # Takes in the column last played and removes the top piece
    for Row in range(Rows-1, -1, -1):
        if Grid[Row, Column] != 0:
            Grid[Row, Column] = 0
            return 1
    return 0
   
def CheckForWinner(Grid, Player):
    #Function to check if there is a winner
    # Inputs: Grid: the game in its current state, Player: the player being evaluated for a win
    # Output: 1 for winner, 0 for no winning combination
    for Row in range(Rows):
        for Column in range(Columns):
            if Grid[Row, Column] == Player:
                if Column + 3 < Columns:
                    #print("Found" + str(Row) + str(Column))
                    # Right
                    if ((Grid[Row, Column + 1] == Player) and (Grid[Row, Column + 2] == Player) and (Grid[Row, Column + 3] == Player)):
                        return 1
                if Row + 3 < Rows:
                    # Up
                    if ((Grid[Row + 1, Column] == Player) and (Grid[Row + 2, Column] == Player) and (Grid[Row + 3, Column] == Player)):
                        return 1
                if Column + 3 < Columns and Row + 3 < Rows:
                    # Up and Right
                    if ((Grid[Row + 1, Column + 1] == Player) and (Grid[Row + 2, Column + 2] == Player) and (Grid[Row + 3, Column + 3] == Player)):
                        #print("Up and Right")
                        return 1
                if Column - 3 >= 0 and Row + 3 < Rows:
                    # Up and Left
                    if ((Grid[Row + 1, Column - 1] == Player) and (Grid[Row + 2, Column - 2] == Player) and (Grid[Row + 3, Column - 3] == Player)):
                        #print("Up and Left")
                        return 1
    return 0

def PlayGameTwoPlayer():
    # Main loop for 2 player game
    while True:
        print("Player 1 select a column 1-7")
        Turn(int(input())-1, 1)
        PrintGrid(Grid)
        if CheckForWinner(Grid, 1):
            print("Player 1 wins!!!")
            return 1
       
        print("Player 2 select a column 1-7")
        Turn(int(input())-1, 2)
        PrintGrid(Grid)
        if CheckForWinner(Grid, 2):
            print("Player 2 wins!!!")
            return 2
    return 1

def RandomAI(Grid, Player):
    # Randomly selects a column which is not full (checks that the top row is empty)
    while True:
        choice = random.randint(0, Columns-1)
        if Grid[Rows-1, choice] == 0:
            return choice

def Defense(Grid, Player):
    #Player is the one who is defending
    #Function looks for 3 in a row of opposing player and if there is a opportunity to block
    #returns blocking position
    target = OpposingPlayer(Player)
    for column in range(Columns):
        if Turn(column, target):
            if CheckForWinner(Grid, target):
                UndoTurn(column)
                print("Threat identified on " + str(column+1))
                return column
            UndoTurn(column)
    return 0

def Offense(Grid, Player):
    #Player is the one who is defending
    #Function looks for 3 in a row of opposing player and if there is a opportunity to block
    #returns blocking position
    for column in range(Columns):
        if Turn(column, Player):
            if CheckForWinner(Grid, Player):
                UndoTurn(column)
                print("Win opportunity identified on " + str(column+1))
                return column
            UndoTurn(column)
    return 0

def RandomAIwithDefense(Grid, Player):
    # Strategy using only defense
    choice = Defense(Grid, Player)
    if choice:
        return choice
    else:
        return RandomAI(Grid, Player)

def RandomAIOffenseDefense(Grid, Player):
    # Strategy first check for a winning combo, then a blocking move, and if not uses a random choice
    choice = Offense(Grid, Player)
    if choice:
        return choice
    choice = Defense(Grid, Player)
    if choice:
        return choice    
    else:
        return RandomAI(Grid, Player)
    
def EvalPos(Grid, Player):
    # Method evaluates position and returns score
    score = 0
    for row in range(Rows):
        for column in range(Columns):
            if Grid[row, column] == Player:
                score += 4 - abs(3- column)
                if row <= 2:
                    score += row+1
                else:
                    score += 6-row
                # Trap Checker
            if row < 5:
                if Grid[row, column] == 0:
                    Grid[row, column] = OpposingPlayer(Player)
                    if CheckForWinner(Grid, OpposingPlayer(Player)):
                        score -= 1000
                        # print("Worry on:" + str(row) + ", " + str(column))
                        Grid[row+1, column] = OpposingPlayer(Player)
                        if CheckForWinner(Grid, OpposingPlayer(Player)):
                            score -= 10000
                            # print("Trap on:" + str(row) + ", " + str(column))
                        Grid[row+1, column] = 0
                    Grid[row, column] = 0
                        


    if CheckForWinner(Grid, Player):
        score += 1000000
    if CheckForWinner(Grid, OpposingPlayer(Player)):
        score -= 1000000
    
    return score

BestChoice = 0
WorstChoice = 0
BestScore = 0
WorstScore = 0
def MiniMaxRecursion(Grid, Player, Depth):
    # 
    # 
    #print(Depth)
    if Depth ==  0:
        return None, (EvalPos(Grid, 2))
    if Player == 2:
        BestScore = -np.inf
        Depth -= 1
        for column in range(Columns):
            if Turn(column, Player):
                choice, score = MiniMaxRecursion(Grid, 1, Depth)
                if score > BestScore:
                    BestScore = score
                    BestChoice = column
                UndoTurn(column)
        #         print(score)
        # print("Maximizer chooses " + str(BestChoice))
        return BestChoice, BestScore
    
    if Player == 1:
        WorstScore = np.inf
        Depth -= 1
        for column in range(Columns):
            if Turn(column, Player):
                choice, score = MiniMaxRecursion(Grid, 2, Depth)
                if score < WorstScore:
                    WorstScore = score
                    WorstChoice = column
                UndoTurn(column)
        #         print(score)
        # print("Minimizer chooses " + str(WorstChoice))
        return WorstChoice, WorstScore
    


def MiniMaxAI(Grid, Player):
    # Strategy first check for a winning combo, then a blocking move, and if not uses Minimax
    MaxDepth = 0
    for row in range(Rows):
        for column in range(Columns):
            if Grid[row, column] == 0:
                MaxDepth += 1
    Depth = 5
    if MaxDepth < Depth:
        Depth = MaxDepth
    choice = Offense(Grid, Player)
    if choice:
        return choice
    choice = Defense(Grid, Player)
    if choice:
        return choice    
    choice, score = MiniMaxRecursion(Grid, Player, Depth)
    return choice
    

def PlayGameAI(AIStrategy):
    # Main loop for game against computer
    # Input: Choose a startegy to use
    while True:
        print("Player 1 select a column 1-7")
        # Verify user has input a valid column
        while not Turn(int(input())-1, 1):
            print("Invalid move, try again")
        PrintGrid(Grid)
        if CheckForWinner(Grid, 1):
            print("Player 1 wins!!!")
            return 1
        
        start = time.time()
        choice = AIStrategy(Grid, 2)
        end = time.time()
        print("AI chose: " + str(choice+1) + " in " + str(round((end - start),2)) + " seconds.")
        Turn(choice, 2)
        PrintGrid(Grid)
        if CheckForWinner(Grid, 2):
            print("Player 2 wins!!!")
            return 2
    return 1

# PlayGameTwoPlayer()

# PlayGameAI(RandomAI)

#Options: RandomAI  RandomAIwithDefense     RandomAIOffenseDefense      MiniMaxAI

PlayGameAI(MiniMaxAI)