from cmu_graphics import *

# Set global variables for background of the app, player turn, game over, and what column of the board the player is currently on.

app.background = 'lightGreen'
app.playerTurn = "red"
app.playerCurrentlySelectedCol = "A"
app.isGameOver = False

board = Rect(60, 80, 280, 240, fill='darkBlue')
rearrangement = {"white": "0", "red": "1", "yellow": "2"}

# Create a structure to store the holes on the board. From left to right, each column of the board is letterd A-G.

holes = {"A": [], "B": [], "C": [], "D": [], "E": [], "F": [], "G": []}

# Populate the holes structure with circles. The bottom left corner of the board is accessible at holes["A"][0], and the top right corner of the board can be reached with holes["G"][5].
x = 80
for letter in list("ABCDEFG"):
    y = 100
    for i in range(6):
        holes[letter].append( Circle(x, y, 15, fill="white") )
        y += 40
    holes[letter].reverse()
    x += 40

# Define a chip above the board for a player to visualize which column they would be sliding their chip into.
chipPlaceholder = Circle(80,60,15,opacity=90,fill=app.playerTurn)

# Given a selected column, findAvailableSpaceForColumn returns the exact hole that the chip would slide into. It accounts for already filled holes in that column.
def findAvailableSpaceForColumn(col):
    for circle in holes[col]:
        if circle.fill == "white":
            # Found the first available empty circle
            return circle
    # If function reaches this point, then there isn't an available circle in the specified column.
    return None

# Switches the player turn. This function will be called after every chip is placed.
def switchPlayerTurn():
    if app.playerTurn == "red":
        app.playerTurn = "yellow"
        chipPlaceholder.fill = "yellow"
    else:
        app.playerTurn = "red"
        chipPlaceholder.fill = "red"

# This function is called whenever the player presses a key. It dictates how the program responds to user inputs.
def onKeyPress(key):
    
    if not app.isGameOver:
        
        # Move the placeholder visualization chip one column left or right depending on which arrow the user presses.
        if key == "right" and chipPlaceholder.centerX <= 300:
            chipPlaceholder.centerX += 40
            # Finds which column letter the placeholder chip is currently above.
            app.playerCurrentlySelectedCol = list(holes.keys())[chipPlaceholder.centerX // 40 - 2]  
            
        elif key == "left" and chipPlaceholder.centerX >= 120:
            chipPlaceholder.centerX -= 40
            app.playerCurrentlySelectedCol = list(holes.keys())[chipPlaceholder.centerX // 40 - 2]
            
        # When the player presses "Enter", the chip will be slotted into the available empty circle on the column that the placeholder chip is currently above. 
        elif key == "enter":
            
            # Find the first empty circle/hole on the column that the player is currently on.
            availableCircleFound = findAvailableSpaceForColumn(app.playerCurrentlySelectedCol)
            
            if availableCircleFound is not None:
                availableCircleFound.fill = app.playerTurn # Fill the hole.
                switchPlayerTurn() # Switch the player's turn.
                checkGameOver()  # Check whether the game is over.

# Checks whether the game has ended.
def checkGameOver():
    
    # Converts the board to a 2-D list ("app.parsed") that represents each row as a collection of 0s, 1s, and 2s. 
    # 0 represents an unfilled space, a 1 represents a red-filled space, and a 2 represents a yellow-filled space.
    app.parsed = []
    for i in range(5, -1, -1):
        # Use Python list comprehension to convert an individual row such as ["red", "yellow", "white", ...] to [1, 2, 0, ...]
        # Add the numeric list to app.parsed.
        app.parsed.append([ rearrangement[ holes[l][i].fill ] for l in list("ABCDEFG") ])

    # Checks if player 1 won the game.
    if checkHorizontal() == 1 or checkVertical() == 1 or checkDiagonals() == 1:
        # Finish the game with player 1 (red) declared as the winner.
        finishGame(1)
    # Checks if player 2 won the game.
    elif checkHorizontal() == 2 or checkVertical() == 2 or checkDiagonals() == 2:
        # Finish the game with player 2 (yellow) declared as the winner.
        finishGame(2)


# Uses the app.parsed 2-D list to determine if there are four adjacent chips of the same color in a (horizontal) row.
def checkHorizontal():
    for row in app.parsed:
        # Four adjacent red chips in a horizontal row
        if "1111" in "".join(row):  
            return 1
        # Four adjacent yellow chips in a horizontal row
        elif "2222" in "".join(row):  
            return 2
    # No horizontal win detected
    return 0  


# Uses the app.parsed 2-D list to determine if there are four adjacent chips of the same color in a (vertical) column.
def checkVertical():
    
    # Uses Python list comprehension to map the vertical columns into 0s, 1s, and 2s following the same schema defined earlier.
    parse = ["".join([rearrangement[y.fill] for y in holes[x]][::-1]) for x in holes.keys()]
    
    for col in parse:
        # Four adjacent red chips in a vertical column
        if "1111" in col:  
            return 1
        # Four adjacent yellow chips in a vertical column
        elif "2222" in col:  
            return 2
    # No vertical win detected
    return 0


# Checks for four adjacent chips of the same color in the diagonals of the board.
def checkDiagonals():
    
    # Check the diagonals starting in the bottom left and reaching to the top right.
    def extract_diagonals(board):
        row, col = len(board), len(board[0])  # Gets the dimensions of the board
        diagonals = []  # Defines an empty array to store the diagonals
        for i in range(row): # Loop over each row and column
            for j in range(col):
                if i >= 3 and j <= 3:  # A diagonal that contains at least four items must start under the constraints that the row number is at least four and the column number is at most four. The conditions use seen in the if-conditional use 3 instead of 4 because Python uses 0-based indexing. 
                    
                    z = [board[i][j]]  # Stores the holes in the diagonal.
                    current_position = [j, i]
                    
                    # Develop the full diagonal, starting at the current position. Every iteration of the for-loop goes one step up and to the right to create the diagonal.
                    for k in range(i):
                        current_position[0] += 1
                        current_position[1] -= 1
                        a, b = current_position
                        try:
                            z.append(board[b][a])
                        except IndexError:  # If the position does not exist, move on.
                            pass
                        
                    diagonals.append(z)  # Add the current diagonal to the list containing all bottom-left to top-right diagonals.
        return diagonals
    
    # extract_diagonals can be called on a reversed board to extract all of the bottom-right to top-left diagonals in addition. These are combined with the existing bottom-left to top-right diagonals to generate a full list of every diagonal that a Connect 4 can exist.
    completeDiagonals = [*extract_diagonals(app.parsed), *extract_diagonals([row[::-1] for row in app.parsed])]
    
    # Return the winner if there is one.
    for row in completeDiagonals:
        if "1111" in "".join(row):  
            return 1
        elif "2222" in "".join(row):  
            return 2
    return 0 


# Officially finish the game.
def finishGame(winner):
    # The game is over! Remove the placeholder chip and set isGameOver to True.
    app.isGameOver = True
    chipPlaceholder.visible = False
    
    # Move the entire board up 40 pixels to make some room for the winner announcement.
    board.centerY -= 40
    for col in holes.keys():
        for item in holes[col]:
            item.centerY -= 40
            
    # Declare the winner.
    Label(f"{'Red' if winner == 1 else 'Yellow'} Wins!", 200, 333, size=30, bold=True)


cmu_graphics.run()