board = [ ["-", "-", "-"],
          ["-", "-", "-"],
          ["-", "-", "-"] ]
 
#printing the board
def printBoard(board):
    print("\n")
    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(board[0][0], board[0][1], board[0][2]))
    print('\t_____|_____|_____')
 
    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(board[1][0], board[1][1], board[1][2]))
    print('\t_____|_____|_____')
 
    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(board[2][0], board[2][1], board[2][2]))
    print("\t     |     |")
    print("\n")
 
def checkWinner(currPlayer, board):
  #Checking for the winner in the row
  for row in range(0,3):
    if board[row][0]==board[row][1]==board[row][2] and board[row][0] != '-':
      if board[row][0]==currPlayer:
        print("{} is winner".format(currPlayer))
        return True
  #used to check the winner in column
  for col in range(0,3):
    if board[0][col]==board[1][col]==board[2][col] and board[0][col] != '-':
      if board[0][col]==currPlayer:
        print("{} is winner".format(currPlayer))
        return True
  #used to check winner in one diagonal
  if board[0][0]==board[1][1]==board[2][2] and board[0][0] !='-':
    if board[0][0]==currPlayer:
      print("{} is winner".format(currPlayer))
      return True
  #used to check winner in another diagonal
  if board[0][2]==board[1][1]==board[2][0] and board[0][2]!='-':
    if board[0][2]==currPlayer:
      print("{} is winner".format(currPlayer))
      return True
  return False
 
printBoard(board)
col=0
row=0
playerTurn = "X"
 
for counter in range(1,10):
    validMove = False
    while (validMove == False):
      col=0
      row=0
      while (col < 1 or col > 3):
        col = int(input(playerTurn + " player, select a column 1-3: "))
        if (col < 1 or col > 3):
          print("The column must be between 1 and 3.")
      while (row < 1 or row > 3):
        row = int(input(playerTurn + " player, select a row 1-3: "))
        if (row < 1 or row > 3):
          print("The row must be between 1 and 3.")
      col -= 1
      row -= 1
      if board[row][col] == '-':
        board[row][col] = playerTurn
        validMove=True;
      else:
        print("Oops, that spot was already taken. Please select another spot.")
        validMove=False
        row=0
        col=0
 
    printBoard(board)
    if (checkWinner(playerTurn,board)):
      break
 
    if playerTurn =="X":
      playerTurn="O"
    else:
      playerTurn="X"