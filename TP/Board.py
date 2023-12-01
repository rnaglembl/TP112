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
    app.inCheck = False
    app.inCheckmate = False
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
    if app.inCheckmate:
        drawLabel(app.turn + ' lost!', 400, 725, size = 15)
    else:
        drawLabel(app.turn + ' to move!', 400, 725, size = 15)
        if app.inCheck:
            drawLabel(app.turn + ' is in check!', 400, 750, size = 15)

def drawBoard(app):
    light = rgb(243, 225, 194)
    dark = rgb(194, 159, 130)
    color = dark
    for row in range(app.rows):
        color = dark if color == light else light
        for col in range(app.cols):
            drawCell(app, row, col, color, app.board[row][col])
            color = dark if color == light else light

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
                #flipBoard(app)
                app.turn = 'black' if app.turn == 'white' else 'white'
        else:
            app.selected = current

        king = getKing(app.turn, app.board)

        if king.isChecked(app.board):
            app.inCheck = True
            if king.isCheckmated(app.board):
                app.inCheckmate = True
        else:
            app.inCheck = False

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
            if current != None and current.getColor() == color:
                for nRow, nCol in current.getLegalMoves(board):
                    if current.isKingLegalMove(board, nRow, nCol):
                        return True

class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.hasMoved = False
        self.position = row, col

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
        
    def getColor(self):
        return self.color

class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.firstPos = row, col

    def move(self, board, row, col):
        oldRow, oldCol = self.position

        if ((row, col) in self.getLegalMoves(board) and 
            self.isKingLegalMove(board, row, col)):
            board[oldRow][oldCol] = None
            if row == 0 or row == 7:
                board[row][col] = Queen(self.color, row, col)
            else:
                board[row][col] = self
                self.hasMoved = True
                self.position = (row, col)
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

        nRow = row+dRow*2
        if not self.hasMoved and (
            isOnBoard(board, nRow, col)) and (board[nRow][col] == None):
            result.append((nRow, col))
        return result

    def draw(self, x, y, cellSize):
        drawCircle(x, y, cellSize/4, fill = self.color)

class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.position
        result = []
        for dRow, dCol in [[0,1], [1,0], [0,-1], [-1,0]]:
                result += self.getLegalMovesInDirection(board, dRow, dCol)
        return result

    def draw(self, x, y, cellSize):
        drawRect(x, y, cellSize/2, cellSize/2, fill=self.color, align='center')

class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.position
        result = []

        for dRow in [-1, 1]:
            for dCol in [-1, 1]:
                result += self.getLegalMovesInDirection(board, dRow, dCol)
        return result

    def draw(self, x, y, cellSize):
        drawCircle(x, y, cellSize/4, fill = self.color)
        drawCircle(x, y, cellSize/8, fill = self.color, border = 'brown')

class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.position
        result = []
        for dRow in [-1, 0, 1]:
            for dCol in [-1, 0, 1]:
                if not dRow == dCol == 0:
                    result += self.getLegalMovesInDirection(board, dRow, dCol)
        return result

    def draw(self, x, y, cellSize):
        drawCircle(x, y, cellSize/4, fill = self.color)
        drawCircle(x, y, cellSize/6, fill = self.color, border = 'brown')
        drawCircle(x, y, cellSize/8, fill = self.color, border = 'brown')

class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)

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

    def draw(self, x, y, cellSize):
        drawRect(x, y, cellSize/3, cellSize/1.5, fill=self.color, align='center')

class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        
    def getLegalMoves(self, board):
        rows = cols = len(board)
        row, col = self.position
        result = []
        for dRow in [-1, 0, 1]:
            for dCol in [-1, 0, 1]:
                if dRow == dCol == 0:
                    continue
                nRow, nCol = row+dRow, col+dCol
                if isOnBoard(board, nRow, nCol) and (board[nRow][nCol] == None or
                    board[nRow][nCol].getColor() != self.color):
                    result.append((nRow, nCol))

        if not self.hasMoved:
            rightRook = board[row][7]
            leftRook = board[row][0]

            print(rightRook)
            
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
                self.castleRook(board, row, col)
            board[oldRow][oldCol] = None
            board[row][col] = self
            self.hasMoved = True
            self.position = (row, col)
            return True
        else:
            return False
        
    def castleRook(self, board, row, col):
        oldRow, oldCol = self.position
        if col - oldCol > 0:
            board[row][7] = None
            board[row][5] = Rook(self.color, row, 5)
        else:
            board[row][0] = None
            board[row][3] = Rook(self.color, row, 3)

    def isChecked(self, board):
        oppColor = 'white' if self.color == 'black' else 'black'
        return self.position in getAllLegalMoves(oppColor, board)
    
    def isCheckmated(self, board):
        if self.isChecked(board) and not hasAKingLegalMove(self.color, board):
            return True
            
    def draw(self, x, y, cellSize):
        drawCircle(x, y, cellSize/4, fill = self.color)
        drawLine(x-cellSize/4, y, x+cellSize/4, y, fill = 'brown')
        drawLine(x, y-cellSize/4, x, y+cellSize/4, fill = 'brown')

def main():
    runApp()

main()
    
