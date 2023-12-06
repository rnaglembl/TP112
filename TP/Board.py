#PvP Chess Game
#Ryan Nagle
#rnagle@andrew.cmu.edu
#
#Chess Icons from Stux:
#https://pixabay.com/vectors/chess-chess-icons-from-persian-shah-335030/

from cmu_graphics import *
from PIL import Image

def onAppStart(app):
    app.rows = app.cols = 8
    app.boardLeft = app.boardTop = 100
    app.width = app.height = 800
    app.boardSize = 600
    app.cellBorderWidth = 2
    app.resetWidth = 85
    app.resetHeight = 25
    app.resetY = 760
    resetBoard(app)

def resetBoard(app):
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.selected = None
    app.turn = 'white'
    app.inCheck = False
    app.inCheckmate = False
    app.inStalemate = False
    app.whitePointDiff = '0'
    app.blackPointDiff = '0'
    initializePieces(app)

def initializePieces(app):
    for col in range(app.cols):
        app.board[6][col] = Pawn('white', 6, col)
        app.board[1][col] = Pawn('black', 1, col)

    app.board[0][0] = Rook('black', 0, 0)
    app.board[0][7] = Rook('black', 0, 7)
    app.board[7][0] = Rook('white', 7, 0)
    app.board[7][7] = Rook('white', 7, 7)

    app.board[0][1] = Knight('black', 0, 1)
    app.board[0][6] = Knight('black', 0, 6)
    app.board[7][1] = Knight('white', 7, 1)
    app.board[7][6] = Knight('white', 7, 6)

    app.board[0][2] = Bishop('black', 0, 2)
    app.board[0][5] = Bishop('black', 0, 5)
    app.board[7][2] = Bishop('white', 7, 2)
    app.board[7][5] = Bishop('white', 7, 5)

    app.board[0][3] = Queen('black', 0, 3)
    app.board[7][3] = Queen('white', 7, 3)

    app.board[0][4] = King('black', 0, 4)
    app.board[7][4] = King('white', 7, 4)

def redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)

    cx = app.width/2
    boardBottom = app.boardTop+app.boardSize
    if app.inCheckmate:
        oppColor = getOppColor(app.turn)
        drawLabel(oppColor + ' has won by checkmate!', cx, boardBottom+10, 
                  size = 15)
    elif app.inStalemate:
        drawLabel('Draw!', cx, boardBottom+10, size = 15)
    else:
        drawLabel(app.turn + ' to move!', cx, boardBottom+10, size = 15)
        if app.inCheck:
            drawLabel(app.turn + ' is in check!', cx, boardBottom+30, size = 15)
    
    drawRect(cx, app.resetY, app.resetWidth, app.resetHeight, fill = None, 
             border = 'black', align = 'center')
    drawLabel('reset game', cx, app.resetY, size = 15)

    drawLabel(app.whitePointDiff, app.boardLeft+5, 
              app.boardTop+app.boardSize+10, size = 15)
    drawLabel(app.blackPointDiff, app.boardLeft+5, app.boardTop-10, size = 15)

def drawBoard(app):
    light = rgb(243, 225, 194)
    dark = rgb(194, 159, 130)
    color = dark
    possibleMoves = []

    if app.selected != None:
        possibleMoves = app.selected.getKingLegalMoves(app.board)

    for row in range(app.rows):
        color = dark if color == light else light
        for col in range(app.cols):
            drawCell(app, row, col, color, app.board[row][col])
            color = dark if color == light else light

            if (row, col) in possibleMoves:
                x,y = getCellLeftTop(app, row, col) 
                cellSize = getCellSize(app)
                drawCircle(x+cellSize/2,y+cellSize/2, 10, fill = 'grey', 
                           opacity = 50)

def getOppColor(color):
    return 'white' if color == 'black' else 'black'

def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardSize, app.boardSize,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color, piece):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellSize = getCellSize(app)
    drawRect(cellLeft, cellTop, cellSize, cellSize,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)
    if piece != None:
        piece.draw(cellLeft+cellSize/2, cellTop+cellSize/2, cellSize)

        if piece == app.selected:
            drawRect(cellLeft, cellTop, cellSize, cellSize,
             fill= 'yellow', opacity = 15)
            
def getCellLeftTop(app, row, col):
    cellSize = getCellSize(app)
    cellLeft = app.boardLeft + col * cellSize
    cellTop = app.boardTop + row * cellSize
    return (cellLeft, cellTop)

def getCellSize(app):
    cellSize = app.boardSize / app.cols
    return cellSize

def getCell(app, x, y):
    cellSize = getCellSize(app)
    row = int((y - app.boardTop) // cellSize)
    col = int((x - app.boardLeft) // cellSize)

    if 0 <= row < app.rows and 0 <= col < app.cols:
        return row, col
    else:
        return None
    
def updatePointDiff(app):
    whitePoints = blackPoints = 0
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            current = app.board[row][col]
            if current != None:
                if current.getColor() == 'white':
                    whitePoints += current.getValue()
                else:
                    blackPoints += current.getValue()

    diff = whitePoints - blackPoints
    if diff > 0:
        app.whitePointDiff = f'+{diff}'
        app.blackPointDiff = f'-{diff}'
    elif diff < 0:
        app.whitePointDiff = f'-{diff}'
        app.blackPointDiff = f'+{diff}'
    else:
        app.whitePointDiff = app.blackPointDiff = '0'

def onMousePress(app, mouseX, mouseY):
    cell = getCell(app, mouseX, mouseY)

    if cell != None:
        row, col = cell
        current = app.board[row][col]

        if app.selected != None and app.selected.getColor() == app.turn and (
            current == None or current.getColor() != app.selected.getColor()):
            if not app.selected.move(app.board, row, col):  
                app.selected = current
            else:
                app.turn = getOppColor(app.turn)
                app.selected = None
                updatePointDiff(app)
        else:
            app.selected = current

        if app.selected != None and app.selected.getColor() != app.turn:
            app.selected = None

        king = getKing(app.turn, app.board)

        if king.isChecked(app.board):
            app.inCheck = True
            if king.isCheckmated(app.board):
                app.inCheckmate = True
        elif not hasAKingLegalMove(app.turn, app.board):
            app.inStalemate = True
        else:
            app.inCheck = False
    else:
        leftX = app.width/2 - app.resetWidth/2
        topY = app.resetY - app.resetHeight/2
        if (leftX < mouseX < leftX + app.resetWidth and 
            topY < mouseY < topY + app.resetHeight):
            resetBoard(app)

def getKing(color, board):
    rows, cols = len(board), len(board[0])
    for row in range(rows):
        for col in range(cols):
            if isinstance(board[row][col], King) and (
                board[row][col].getColor() == color):
                return board[row][col]

def isOnBoard(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])

def getAllLegalMoves(color, board):
    result = []
    rows, cols = len(board), len(board[0])
    for row in range(rows):
        for col in range(cols):
            current = board[row][col]
            if current != None and current.getColor() == color:
                result += current.getLegalMoves(board)
    return result

def hasAKingLegalMove(color, board):
    result = []
    rows, cols = len(board), len(board[0])
    for row in range(rows):
        for col in range(cols):
            current = board[row][col]
            if current != None and current.getColor() == color and (
                current.getKingLegalMoves(board) != []):
                return True
    return False

class Piece:
    def __init__(self, color, row, col, value, icon):
        self.color = color
        self.hasMoved = False
        self.position = row, col
        self.value = value
        self.icon = icon

    def move(self, board, row, col):
        oldRow, oldCol = self.position

        if ((row, col) in self.getLegalMoves(board) and 
            self.isKingLegalMove(board, row, col)):
            board[oldRow][oldCol] = None
            board[row][col] = self
            self.hasMoved = True
            self.position = (row, col)
            return True
        else:
            return False
    
    def getLegalMovesInDirection(self, board, dRow, dCol):
        row, col = self.position
        nRow, nCol = row+dRow, col+dCol
        result = []
        while isOnBoard(board, nRow, nCol) and board[nRow][nCol] == None:
            result.append((nRow, nCol))
            nRow+=dRow
            nCol+=dCol

        if isOnBoard(board, nRow, nCol) and board[nRow][nCol] != None and (
            board[nRow][nCol].getColor() != self.color):
            result.append((nRow, nCol))
        return result
    
    def isKingLegalMove(self, board, nRow, nCol):
        row, col = self.position
        target = board[nRow][nCol]
        board[row][col] = None
        board[nRow][nCol] = self
        self.position = nRow, nCol

        result = not getKing(self.color, board).isChecked(board)
        board[row][col] = self
        board[nRow][nCol] = target
        self.position = row, col

        return result
    
    def getKingLegalMoves(self, board):
        result = []
        for row, col in self.getLegalMoves(board):
            if self.isKingLegalMove(board, row, col):
                result.append((row, col))
        return result
        
    def getColor(self):
        return self.color
    
    def getValue(self):
        return self.value
    
    def draw(self, x, y, cellSize):
        stockWidth, stockHeight = self.icon.size
        scaleFactor = stockWidth/stockHeight
        h = cellSize//1.5
        w = h * scaleFactor

        icon = CMUImage(self.icon)
        drawImage(icon, x, y, align = 'center', width = w, height = h)

class Pawn(Piece):
    def __init__(self, color, row, col):
        icon = Image.open('images/'+ color + 'Pawn.png')
        super().__init__(color, row, col, 1, icon)
        self.firstPos = row, col
        self.lastPos = row, col

    def move(self, board, row, col):
        oldRow, oldCol = self.position

        if ((row, col) in self.getLegalMoves(board) and 
            self.isKingLegalMove(board, row, col)):
            board[oldRow][oldCol] = None
            if row == 0 or row == 7:
                board[row][col] = Queen(self.color, row, col)
            else:
                #check en passant
                if col != oldCol and board[row][col] == None:
                    board[oldRow][col] = None

                board[row][col] = self
                self.hasMoved = True
                self.position = (row, col)
                self.lastPos = (oldRow, oldCol)
            return True
        else:
            return False

    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.position
        centerRow = 5
        dRow = -1 if self.firstPos[0] - centerRow > 0 else 1
        result = []
        
        nRow = row+dRow
        if isOnBoard(board, nRow, col) and board[nRow][col] == None:
            result.append((nRow, col))

        for nCol in [col-1, col+1]:
            if isOnBoard(board, nRow, nCol) and board[nRow][nCol] != None and (
                board[nRow][nCol].getColor() != self.color):
                result.append((nRow, nCol))
            #check en passant
            if isOnBoard(board, row, nCol) and (
                isinstance(board[row][nCol], Pawn) and 
                board[row][nCol].getLastRow() == row + 2*dRow):
                result.append((nRow, nCol))

        nRow = row+dRow*2
        if not self.hasMoved and (
            isOnBoard(board, nRow, col)) and (board[nRow][col] == None):
            result.append((nRow, col))
        return result
    
    def getLastRow(self):
        return self.lastPos[0]

class Rook(Piece):
    def __init__(self, color, row, col):
        icon = Image.open('images/'+ color + 'Rook.png')
        super().__init__(color, row, col, 5, icon)
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.position
        result = []
        for dRow, dCol in [[0,1], [1,0], [0,-1], [-1,0]]:
                result += self.getLegalMovesInDirection(board, dRow, dCol)
        return result

class Bishop(Piece):
    def __init__(self, color, row, col):
        icon = Image.open('images/'+ color + 'Bishop.png')
        super().__init__(color, row, col, 3, icon)
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.position
        result = []

        for dRow in [-1, 1]:
            for dCol in [-1, 1]:
                result += self.getLegalMovesInDirection(board, dRow, dCol)
        return result

class Queen(Piece):
    def __init__(self, color, row, col):
        icon = Image.open('images/'+ color + 'Queen.png')
        super().__init__(color, row, col, 9, icon)

    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.position
        result = []
        for dRow in [-1, 0, 1]:
            for dCol in [-1, 0, 1]:
                if not dRow == dCol == 0:
                    result += self.getLegalMovesInDirection(board, dRow, dCol)
        return result

class Knight(Piece):
    def __init__(self, color, row, col):
        icon = Image.open('images/'+ color + 'Knight.png')
        super().__init__(color, row, col, 3, icon)

    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.position
        result = []
        possibleMoves = [[2,-1], [2,1], [-2,-1], [-2,1], 
                         [-1,2], [1,2], [-1,-2], [1,-2]]
        for dRow, dCol in possibleMoves:
            nRow, nCol = row+dRow, col+dCol
            if isOnBoard(board, nRow, nCol) and (board[nRow][nCol] == None or
                board[nRow][nCol].getColor() != self.color):
                result.append((nRow, nCol))
        return result

class King(Piece):
    def __init__(self, color, row, col):
        icon = Image.open('images/'+ color + 'King.png')
        super().__init__(color, row, col, 0, icon)
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.position
        result = []
        for dRow in [-1, 0, 1]:
            for dCol in [-1, 0, 1]:
                if dRow == dCol == 0:
                    continue
                nRow, nCol = row+dRow, col+dCol
                if isOnBoard(board, nRow, nCol) and (board[nRow][nCol] == None 
                    or board[nRow][nCol].getColor() != self.color):
                    result.append((nRow, nCol))

        #check castle
        if not self.hasMoved:
            rightRook = board[row][7]
            leftRook = board[row][0]
            
            if (len(self.getLegalMovesInDirection(board, 0, 1)) == 2 and
                rightRook != None and not rightRook.hasMoved):
                result.append((row,6))
            if (len(self.getLegalMovesInDirection(board, 0, -1)) == 3 and
                leftRook != None and not leftRook.hasMoved):
                result.append((row,2))
                    
        return result
    
    def move(self, board, row, col):
        oldRow, oldCol = self.position

        if ((row, col) in self.getLegalMoves(board) and 
            self.isKingLegalMove(board, row, col)):
            if abs(col-oldCol) > 1:
                if not self.isChecked(board):
                    self.castle(board, row, col)
                    return True
            else:
                board[oldRow][oldCol] = None
                board[row][col] = self
                self.position = (row, col)   
                self.hasMoved = True
                return True
        else:
            return False
        
    def castle(self, board, row, col):
        oldRow, oldCol = self.position
        board[oldRow][oldCol] = None
        board[row][col] = self
        self.position = (row, col)

        if col - oldCol > 0:
            board[row][7] = None
            board[row][5] = Rook(self.color, row, 5)
        else:
            board[row][0] = None
            board[row][3] = Rook(self.color, row, 3)

    def isChecked(self, board):
        oppColor = getOppColor(self.color)
        return self.position in getAllLegalMoves(oppColor, board)
    
    def isCheckmated(self, board):
        if self.isChecked(board) and not hasAKingLegalMove(self.color, board):
            return True

def main():
    runApp()

main()
    
