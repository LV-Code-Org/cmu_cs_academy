from cmu_graphics import *

app.currentSelectedPiece = None

def createGrid():
    letters = 'A B C D E F G H'.split(" ")
    currentCoords = [40,40]
    grid = {}
    colorWhite = True
    for row in [8,7,6,5,4,3,2,1]:
        for letter in letters:
            cellFill = ""
            if colorWhite:
                cellFill = "red"
            else:
                cellFill = "black"
            grid['%s%d'%(letter,row)] = Rect(currentCoords[0],currentCoords[1],40,40,fill=cellFill)
            currentCoords[0] += 40
            colorWhite = not colorWhite
        currentCoords[1] += 40
        currentCoords[0] = 40
        colorWhite = not colorWhite
    return grid

def calculateAvailableMoves(currentPieceGridPosition, color):

    positionBreakdown = list(currentPieceGridPosition)
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    constant = 0
    if color == 'white':
        constant = str(int(positionBreakdown[1]) - 1)
    elif color == 'red':
        constant = str(int(positionBreakdown[1]) + 1)
    leftward = [letters[letters.index(positionBreakdown[0]) - 1], constant]
    rightward = []
    kill = []
    try:
        rightward = [letters[letters.index(positionBreakdown[0]) + 1], constant]
        if color == 'red':
            for w in whitePieces:
                if grid["".join(leftward)].contains(w.centerX, w.centerY):
                    print("FOUND KILL")
                    kill.append("".join([letters[letters.index(positionBreakdown[0]) - 2], str(int(constant) + 1)]))
                if grid["".join(rightward)].contains(w.centerX, w.centerY):
                    print("FOUND KILL")
                    kill.append("".join([letters[letters.index(positionBreakdown[0]) + 2], str(int(constant) + 1)]))
        elif color == 'white':
            for b in blackPieces:
                print("WORKING")
                if grid["".join(leftward)].contains(b.centerX, b.centerY):
                    print("FOUND KILL")
                    kill.append("".join([letters[letters.index(positionBreakdown[0]) - 2], str(int(constant) - 1)]))
                if grid["".join(rightward)].contains(b.centerX, b.centerY):
                    print("FOUND KILL")
                    kill.append("".join([letters[letters.index(positionBreakdown[0]) + 2], str(int(constant) - 1)]))
    except IndexError:
        return [["".join(leftward)] + kill]
    print("---------")
    print(kill)
    print("---------")
    if positionBreakdown[0] == "A":
        return [["".join(rightward)] + kill]
    else:
        return[ ["".join(leftward), "".join(rightward)] + kill]

grid = createGrid()
whitePieces = []
whitePieceSquareList = []
blackPieces = []
blackPieceSquareList = []
squareGuide = Group()
for square in list(grid.keys()):
    if grid[square].fill == "black" and (int(list(square)[1]) <= 8 and int(list(square)[1]) >= 6):
        whitePieces.append(Circle(grid[square].centerX, grid[square].centerY, 10, fill="white"))
        whitePieceSquareList.append(square)
    elif grid[square].fill == "black" and (int(list(square)[1]) <= 3 and int(list(square)[1]) >= 1):
        blackPieces.append(Circle(grid[square].centerX, grid[square].centerY, 10, fill="red"))
        blackPieceSquareList.append(square)
        
def onMousePress(mouseX, mouseY):
    alreadySelected = app.currentSelectedPiece is not None
    if not alreadySelected:
        squareGuide.clear()
    clickedPiece = False
    pieceClicked = None
    pieceClickedName = None
    for piece in whitePieces:
        if piece.contains(mouseX,mouseY):
            print("clicked white piece")
            pieceClicked = piece
            app.currentSelectedPiece = piece
            clickedPiece = True
    for piece in blackPieces:
        if piece.contains(mouseX,mouseY):
            print("clicked black piece")
            pieceClicked = piece
            app.currentSelectedPiece = piece
            clickedPiece = True
    if alreadySelected:
        for avail in squareGuide:
            if avail.contains(mouseX, mouseY):
                app.currentSelectedPiece.centerX = avail.centerX
                app.currentSelectedPiece.centerY = avail.centerY
        squareGuide.clear()

    if clickedPiece:
        for gsquare in list(grid.keys()):
            if grid[gsquare].contains(pieceClicked.centerX, pieceClicked.centerY):
                pieceClickedName = gsquare
        for availableSquare in calculateAvailableMoves(pieceClickedName, pieceClicked.fill)[0]:
            squareGuide.add(
                Circle(grid[availableSquare].centerX, grid[availableSquare].centerY, 10, fill="white", opacity=40)
            )

    print(pieceClicked, pieceClickedName)
    

cmu_graphics.run()