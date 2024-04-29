from cmu_graphics import *
from random import choice

# Black bars

Rect(0, 0, 80, 400)
Rect(280, 0, 120, 400)

app.stepsPerSecond = 2
app.board = [
    ["_" for _ in range(10)] for _ in range(20)
]
app.allPieces = []
app.score = 0

scoreLabel = Label(app.score, 340, 60, fill="white", size=20)
checker = Rect(80, 0, 20, 20)
checker.visible = False

# Tetronimoes


class I ():
    def __init__(self):
        self.squares = Group(
            Rect(80, 0, 20, 20, fill="cyan", border="turquoise"),
            Rect(100, 0, 20, 20, fill="cyan", border="turquoise"),
            Rect(120, 0, 20, 20, fill="cyan", border="turquoise"),
            Rect(140, 0, 20, 20, fill="cyan", border="turquoise")
        )


class J ():
    def __init__(self):
        self.squares = Group(
            Rect(80, 0, 20, 20, fill="blue", border="darkBlue"),
            Rect(80, 20, 20, 20, fill="blue", border="darkBlue"),
            Rect(100, 20, 20, 20, fill="blue", border="darkBlue"),
            Rect(120, 20, 20, 20, fill="blue", border="darkBlue"),
        )


class O ():
    def __init__(self):
        self.squares = Group(
            Rect(80, 0, 20, 20, fill="yellow", border="gold"),
            Rect(100, 0, 20, 20, fill="yellow", border="gold"),
            Rect(80, 20, 20, 20, fill="yellow", border="gold"),
            Rect(100, 20, 20, 20, fill="yellow", border="gold"),
        )


class S ():
    def __init__(self):
        self.squares = Group(
            Rect(120, 0, 20, 20, fill="lime", border="limeGreen"),
            Rect(140, 0, 20, 20, fill="lime", border="limeGreen"),
            Rect(100, 20, 20, 20, fill="lime", border="limeGreen"),
            Rect(120, 20, 20, 20, fill="lime", border="limeGreen"),
        )


class Z ():
    def __init__(self):
        self.squares = Group(
            Rect(100, 0, 20, 20, fill="red", border="fireBrick"),
            Rect(80, 0, 20, 20, fill="red", border="fireBrick"),
            Rect(100, 20, 20, 20, fill="red", border="fireBrick"),
            Rect(120, 20, 20, 20, fill="red", border="fireBrick"),
        )


class T ():
    def __init__(self):
        self.squares = Group(
            Rect(120, 0, 20, 20, fill="blueViolet", border="darkViolet"),
            Rect(140, 20, 20, 20, fill="blueViolet", border="darkViolet"),
            Rect(100, 20, 20, 20, fill="blueViolet", border="darkViolet"),
            Rect(120, 20, 20, 20, fill="blueViolet", border="darkViolet"),
        )


pieces = [I, J, O, S, Z, T]
app.currentPiece = choice(pieces)()


# Helper functions

def printBoard():
    print("================== BOARD =====================")
    for r in app.board:
        print(" ".join(r))


def updateBoard():
    for row in range(20):
        for col in range(10):
            for square in app.currentPiece.squares.children:
                if checker.centerX == square.centerX and checker.centerY == square.centerY:
                    app.board[row][col] = "X"
            checker.centerX += 20
        checker.left = 80
        checker.centerY += 20
    checker.left = 80
    checker.top = 0


def currentPieceData():
    pieceData = []
    for square in app.currentPiece.squares.children:
        x, y = (square.top - 0) // 20, (square.left - 80) // 20
        pieceData.append((x, y))
    return pieceData


def canMove(direction):
    modifier = 1 if direction == "right" else -1
    for squareX, squareY in currentPieceData():
        if app.board[squareX][squareY+modifier] == "X":
            return False
    return True


def underneathCheck():
    try:
        underneathArea = [app.board[x+1][y] for x, y in currentPieceData()]
        if "X" in underneathArea:
            updateBoard()
            app.allPieces.append(app.currentPiece)
            app.currentPiece = choice(pieces)()
    except IndexError:
        pass


def boardCheckup():

    for index, row in enumerate(app.board):

        if "X" * 10 == "".join(row):  # Row filled out

            # Manage internal board
            app.board.remove(app.board[index])
            app.board.insert(0, ["_" for _ in range(10)])

            # Manage UI
            depth = 20 * index
            for piece in app.allPieces:
                for square in piece.squares:
                    if square.top == depth:
                        square.visible = False
                    else:
                        if square.top // 20 < index:
                            square.top += 20

            # Score management
            app.score += 2000
            scoreLabel.value = app.score


# Events

def onStep():

    # Progressively move current piece downwards
    if app.currentPiece.squares.bottom < 400:

        app.currentPiece.squares.centerY += 20
        underneathCheck()

    # Piece finishes path
    if app.currentPiece.squares.bottom == 400:

        updateBoard()
        printBoard()

        app.allPieces.append(app.currentPiece)
        app.currentPiece = choice(pieces)()

        printBoard()

    boardCheckup()


def onKeyPress(key):

    # Movement
    if key == "right" and app.currentPiece.squares.right < 280:
        if canMove("right"):
            app.currentPiece.squares.centerX += 20
    if key == "left" and app.currentPiece.squares.left > 80:
        if canMove("left"):
            app.currentPiece.squares.centerX -= 20

    # Rotation
    if key == "up":
        app.currentPiece.squares.rotateAngle += 90
        if isinstance(app.currentPiece, I) or isinstance(app.currentPiece, S) or isinstance(app.currentPiece, Z):
            app.currentPiece.squares.centerX += 10
            app.currentPiece.squares.centerY += 10
        elif isinstance(app.currentPiece, J):
            if app.currentPiece.squares.rotateAngle == 90 or app.currentPiece.squares.rotateAngle == 270:
                app.currentPiece.squares.centerX += 10
            if app.currentPiece.squares.rotateAngle == 180 or app.currentPiece.squares.rotateAngle == 360:
                app.currentPiece.squares.centerY += 10
            if app.currentPiece.squares.rotateAngle == 360:
                app.currentPiece.squares.rotateAngle = 0
        elif isinstance(app.currentPiece, T):
            if app.currentPiece.squares.rotateAngle == 90:
                app.currentPiece.squares.centerX += 5
                app.currentPiece.squares.centerY += 5
            elif app.currentPiece.squares.rotateAngle == 180:
                app.currentPiece.squares.centerX -= 5
                app.currentPiece.squares.centerY += 5
            elif app.currentPiece.squares.rotateAngle == 270:
                app.currentPiece.squares.centerX -= 5
                app.currentPiece.squares.centerY -= 5
            elif app.currentPiece.squares.rotateAngle == 360:
                app.currentPiece.squares.centerX += 5
                app.currentPiece.squares.centerY -= 5
                app.currentPiece.squares.rotateAngle = 0


def onKeyHold(keys):
    if "down" in keys:
        app.stepsPerSecond = 40
        app.currentPiece.squares.centerY += 20
        underneathCheck()


def onKeyRelease(keys):
    if "down" in keys:
        app.stepsPerSecond = 2


cmu_graphics.run()
