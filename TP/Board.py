from cmu_graphics import *

def onAppStart(app):
    app.rows = app.cols = 8
    app.boardLeft = 100
    app.boardTop = 100
    app.width = app.height = 800
    app.boardSize = 600
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.selected = None
    app.turn = 'white'
    initializePieces(app)

def initializePieces(app):
    for col in range(app.cols):
        app.board[6][col] = Pawn('white', app.board)
        app.board[1][col] = Pawn('black', app.board)
    app.board[0][0] = Rook('black', app.board)
    app.board[0][7] = Rook('black', app.board)
    app.board[7][0] = Rook('white', app.board)
    app.board[7][7] = Rook('white', app.board)

    app.board[0][1] = Knight('black', app.board)
    app.board[0][6] = Knight('black', app.board)
    app.board[7][1] = Knight('white', app.board)
    app.board[7][6] = Knight('white', app.board)

    app.board[0][2] = Bishop('black', app.board)
    app.board[0][5] = Bishop('black', app.board)
    app.board[7][2] = Bishop('white', app.board)
    app.board[7][5] = Bishop('white', app.board)

    app.board[0][3] = Queen('black', app.board)
    app.board[7][3] = Queen('white', app.board)

    app.board[0][4] = King('black', app.board)
    app.board[7][4] = King('white', app.board)

def redrawAll(app):
    drawBoard(app)
    drawBoardBorder(app)
    drawLabel(app.turn + ' to move!', 400, 725, size = 15)

def drawBoard(app):
    light = rgb(243, 225, 194)
    dark = rgb(194, 159, 130)
    color = dark
    for row in range(app.rows):
        if color == light:
            color = dark
        else:
            color = light
        for col in range(app.cols):
            drawCell(app, row, col, color, app.board[row][col])
            if color == light:
                color = dark
            else:
                color = light

def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardSize, app.boardSize,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)
  
def flipBoard(app):
    app.board = app.board[::-1]
    for rowList in app.board:
        rowList = rowList[::-1]

def drawCell(app, row, col, color, piece):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellSize = getCellSize(app)
    drawRect(cellLeft, cellTop, cellSize, cellSize,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)
    if piece != None:
        piece.draw(cellLeft+cellSize/2, cellTop+cellSize/2, cellSize)

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
                flipBoard(app)
                if app.turn == 'white':
                    app.turn = 'black'
                else:
                    app.turn = 'white'
        else:
            app.selected = current

        print(app.turn)

def isOnBoard(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0])
        
class Pawn:
    def __init__(self, color, board):
        self.color = color
        self.firstPos = None
        self.currentPos = None

    def move(self, board, row, col):
        if self.firstPos == None:
            self.firstPos = self.getPosition(board)
        if self.currentPos == None:
            self.currentPos = self.firstPos

        oldRow, oldCol = self.currentPos

        if (row, col) in self.getLegalMoves(board):
            board[oldRow][oldCol] = None
            board[row][col] = self
            self.currentPos = (row, col)
            return True
        else:
            return False
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.currentPos
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

        nRow = row+dRow*2
        if self.firstPos == self.currentPos and (
            isOnBoard(board, nRow, col)) and (board[nRow][col] == None):
            result.append((nRow, col))
        return result
    
    def getPosition(self, board):
        rows, cols = len(board), len(board[0])
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == self:
                    return row, col
        
    def getColor(self):
        return self.color

    def draw(self, x, y, cellSize):
        drawCircle(x, y, cellSize/4, fill = self.color)

class Rook:
    def __init__(self, color, board):
        self.color = color
        self.currentPos = None

    def move(self, board, row, col):
        if self.currentPos == None:
            self.currentPos = self.getPosition(board)
        oldRow, oldCol = self.currentPos

        if (row, col) in self.getLegalMoves(board):
            board[oldRow][oldCol] = None
            board[row][col] = self
            self.currentPos = (row, col)
            return True
        else:
            return False
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.currentPos
        result = []
        for dRow, dCol in [[0,1], [1,0], [0,-1], [-1,0]]:
                result += self.getLegalMovesInDirection(board, dRow, dCol)
        return result
    
    def getLegalMovesInDirection(self, board, dRow, dCol):
        row, col = self.currentPos
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

    def getColor(self):
        return self.color
    
    def getPosition(self, board):
        rows, cols = len(board), len(board[0])
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == self:
                    return row, col

    def draw(self, x, y, cellSize):
        drawRect(x, y, cellSize/2, cellSize/2, fill=self.color, align='center')

class Bishop:
    def __init__(self, color, board):
        self.color = color
        self.currentPos = None

    def move(self, board, row, col):
        if self.currentPos == None:
            self.currentPos = self.getPosition(board)
        oldRow, oldCol = self.currentPos

        if (row, col) in self.getLegalMoves(board):
            board[oldRow][oldCol] = None
            board[row][col] = self
            self.currentPos = (row, col)
            return True
        else:
            return False
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.currentPos
        result = []

        for dRow in [-1, 1]:
            for dCol in [-1, 1]:
                result += self.getLegalMovesInDirection(board, dRow, dCol)
        return result
    
    def getLegalMovesInDirection(self, board, dRow, dCol):
        row, col = self.currentPos
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

    def getColor(self):
        return self.color
    
    def getPosition(self, board):
        rows, cols = len(board), len(board[0])
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == self:
                    return row, col

    def draw(self, x, y, cellSize):
        drawCircle(x, y, cellSize/4, fill = self.color)
        drawCircle(x, y, cellSize/8, fill = self.color, border = 'brown')

class Queen:
    def __init__(self, color, board):
        self.color = color
        self.currentPos = None

    def move(self, board, row, col):
        if self.currentPos == None:
            self.currentPos = self.getPosition(board)
        oldRow, oldCol = self.currentPos

        if (row, col) in self.getLegalMoves(board):
            board[oldRow][oldCol] = None
            board[row][col] = self
            self.currentPos = (row, col)
            return True
        else:
            return False
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.currentPos
        result = []
        for dRow in [-1, 0, 1]:
            for dCol in [-1, 0, 1]:
                if not dRow == dCol == 0:
                    result += self.getLegalMovesInDirection(board, dRow, dCol)
        return result
    
    def getLegalMovesInDirection(self, board, dRow, dCol):
        row, col = self.currentPos
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

    def getColor(self):
        return self.color
    
    def getPosition(self, board):
        rows, cols = len(board), len(board[0])
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == self:
                    return row, col

    def draw(self, x, y, cellSize):
        drawCircle(x, y, cellSize/4, fill = self.color)
        drawCircle(x, y, cellSize/6, fill = self.color, border = 'brown')
        drawCircle(x, y, cellSize/8, fill = self.color, border = 'brown')

class Knight:
    def __init__(self, color, board):
        self.color = color
        self.currentPos = None

    def move(self, board, row, col):
        if self.currentPos == None:
            self.currentPos = self.getPosition(board)
        oldRow, oldCol = self.currentPos

        if (row, col) in self.getLegalMoves(board):
            board[oldRow][oldCol] = None
            board[row][col] = self
            self.currentPos = (row, col)
            return True
        else:
            return False
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.currentPos
        result = []
        possibleMoves = [[2,-1], [2,1], [-2,-1], [-2,1], 
                         [-1,2], [1,2], [-1,-2], [1,-2]]
        for dRow, dCol in possibleMoves:
            nRow, nCol = row+dRow, col+dCol
            if isOnBoard(board, nRow, nCol) and (board[nRow][nCol] == None or
                board[nRow][nCol].getColor() != self.color):
                result.append((nRow, nCol))
        return result

    def getColor(self):
        return self.color
    
    def getPosition(self, board):
        rows, cols = len(board), len(board[0])
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == self:
                    return row, col

    def draw(self, x, y, cellSize):
        drawRect(x, y, cellSize/3, cellSize/1.5, fill=self.color, align='center')

class King:
    def __init__(self, color, board):
        self.color = color
        self.currentPos = None

    def move(self, board, row, col):
        if self.currentPos == None:
            self.currentPos = self.getPosition(board)
        oldRow, oldCol = self.currentPos

        if (row, col) in self.getLegalMoves(board):
            board[oldRow][oldCol] = None
            board[row][col] = self
            self.currentPos = (row, col)
            return True
        else:
            return False
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.currentPos
        result = []
        for dRow in [-1, 0, 1]:
            for dCol in [-1, 0, 1]:
                if dRow == dCol == 0:
                    continue
                nRow, nCol = row+dRow, col+dCol
                if isOnBoard(board, nRow, nCol) and (board[nRow][nCol] == None or
                    board[nRow][nCol].getColor() != self.color):
                    result.append((nRow, nCol))
        return result

    def getColor(self):
        return self.color
    
    def getPosition(self, board):
        rows, cols = len(board), len(board[0])
        for row in range(rows):
            for col in range(cols):
                if board[row][col] == self:
                    return row, col

    def draw(self, x, y, cellSize):
        drawCircle(x, y, cellSize/4, fill = self.color)
        drawLine(x-cellSize/4, y, x+cellSize/4, y, fill = 'brown')
        drawLine(x, y-cellSize/4, x, y+cellSize/4, fill = 'brown')

def main():
    runApp()

main()
    
