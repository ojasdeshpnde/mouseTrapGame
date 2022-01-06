
import random
import pygame

mP = []

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.molecule = None


class Node:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.prev = None
        self.value = 0
        self.visited = False

mouseLocation = [5,5]
def drawHexagon(row, col):
    baseX = 100
    baseY = 100
    if row % 2 == 0:
        pygame.draw.polygon(screen, BLUE, [(52*col + baseX,45*row+baseY),(52 * col + baseX + 26,45*row+baseY + 15),(52 * col + baseX + 26,45*row+baseY + 45),(52 * col + baseX,45*row+baseY + 60),(52 * col + baseX - 26,45*row+baseY + 45),(52 * col + baseX - 26,45*row+baseY + 15)],2)
    else:
        pygame.draw.polygon(screen, BLUE, [(52 * col + baseX+26, 45*row+ baseY), (52 * col + baseX + 52, 45*row+ baseY + 15), (52 * col + baseX + 52,45*row+  baseY + 45), (52 * col + baseX+26, 45*row+ baseY + 60),(52 * col + baseX, 45*row+ baseY + 45), (52 * col + baseX, 45*row+ baseY + 15)], 2)

def drawColorHexagon(row,col, C):
    baseX = 100
    baseY = 100
    if row % 2 == 0:
        pygame.draw.polygon(screen, C, [(52*col + baseX,45*row+baseY),(52 * col + baseX + 26,45*row+baseY + 15),(52 * col + baseX + 26,45*row+baseY + 45),(52 * col + baseX,45*row+baseY + 60),(52 * col + baseX - 26,45*row+baseY + 45),(52 * col + baseX - 26,45*row+baseY + 15)])
    else:
        pygame.draw.polygon(screen, C, [(52 * col + baseX+26, 45*row+ baseY), (52 * col + baseX + 52, 45*row+ baseY + 15), (52 * col + baseX + 52,45*row+  baseY + 45), (52 * col + baseX+26, 45*row+ baseY + 60),(52 * col + baseX, 45*row+ baseY + 45), (52 * col + baseX, 45*row+ baseY + 15)])

def drawMouse(row,col):
    baseX = 100
    baseY = 100
    if row % 2 == 0:
        pygame.draw.circle(screen, GREEN, (52* col + baseX, 45 * row + baseY + 30), 26)
    else:
        pygame.draw.circle(screen, GREEN, (52* col + baseX + 26, 45 * row + baseY + 30), 26)

# 0 is empty spot
# 1 is mouse
# 2 is wall

def setupBoard(board, boardSize):
    for row in range(boardSize):
        subBoard = []
        for col in range(boardSize):
            n = Node(row,col)
            subBoard.append(n)
            drawHexagon(row, col)
        board.append(subBoard)
    drawMouse(mouseLocation[0],mouseLocation[1])
    board[mouseLocation[0]][mouseLocation[1]].value = 1
    counter = 0
    while counter < 8:
        displacementX = 0
        displacementY =  0
        if random.random() < 0.5:
            displacementX = 7
        if random.random() < 0.5:
             displacementY = 7
        x = random.randint(0 + displacementX,3 + displacementX)
        y = random.randint(0 + displacementY,3 + displacementY)
        while(board[x][y].value != 0):
            displacementX = 0
            displacementY = 0
            if random.random() < 0.5:
                displacementX = 7
            if random.random() < 0.5:
                displacementY = 7
            x = random.randint(0 + displacementX, 3 + displacementX)
            y = random.randint(0 + displacementY, 3 + displacementY)
        board[x][y].value = 2
        counter = counter + 1
        drawColorHexagon(x,y,BROWN)
    pygame.display.flip()


def click(pos):
    row = int((pos[1] - 100)/45)
    col = int((pos[0]-74)/52)
    if row % 2 != 0:
        col = int((pos[0]-100)/52)
    drawColorHexagon(row,col,BROWN)
    board[row][col].value = 2
    pygame.display.flip()
    return moveMouse(board)


def moveMouse(board):
    global mP
    if len(mP) == 0:
        mP = BFS(board)
    else:
        redo = False
        for n in mP:
            if(board[n.row][n.col].value == 2):
                redo = True
        if redo:
            mP = BFS(board)
    if(len(mP) == 0):
        return True
    board[mouseLocation[0]][mouseLocation[1]].value = 0
    drawColorHexagon(mouseLocation[0],mouseLocation[1],BLACK)
    drawHexagon(mouseLocation[0],mouseLocation[1])
    mouseLocation[0] = mP[len(mP)-1].row
    mouseLocation[1] = mP[len(mP)-1].col
    del mP[len(mP)-1]
    board[mouseLocation[0]][mouseLocation[1]].value = 1
    drawMouse(mouseLocation[0],mouseLocation[1])
    pygame.display.flip()
    if mouseLocation[0] == 0 or mouseLocation[0] == 10 or mouseLocation[1] == 0 or mouseLocation[1] == 10:
        return True
    else:
        return False

def BFS(board):
    retValue = []
    cN = board[mouseLocation[0]][mouseLocation[1]]
    queue = []

    counter = 0
    while(cN.row != 0 and cN.row != 10 and cN.col != 0 and cN.col != 10 and (len(queue) != 0 or counter == 0) ):

        if board[cN.row-1][cN.col].value == 0 and board[cN.row-1][cN.col].visited == False:
            queue.append(board[cN.row-1][cN.col])
            board[cN.row-1][cN.col].visited = True
            board[cN.row - 1][cN.col].prev = cN
        if board[cN.row-1][cN.col+1].value == 0 and board[cN.row-1][cN.col+1].visited == False and cN.row %2 != 0:
            queue.append(board[cN.row-1][cN.col+1])
            board[cN.row - 1][cN.col + 1].visited = True
            board[cN.row - 1][cN.col + 1].prev = cN
        elif board[cN.row-1][cN.col-1].value == 0 and board[cN.row-1][cN.col-1].visited == False and cN.row %2 == 0:
            queue.append(board[cN.row - 1][cN.col - 1])
            board[cN.row - 1][cN.col - 1].visited = True
            board[cN.row - 1][cN.col - 1].prev = cN
        if board[cN.row][cN.col-1].value == 0 and board[cN.row][cN.col-1].visited == False:
            queue.append(board[cN.row][cN.col-1])
            board[cN.row][cN.col - 1].visited = True
            board[cN.row][cN.col - 1].prev = cN
        if board[cN.row][cN.col+1].value == 0 and board[cN.row][cN.col+1].visited == False:
            queue.append(board[cN.row][cN.col+1])
            board[cN.row][cN.col+1].visited = True
            board[cN.row][cN.col + 1].prev = cN
        if board[cN.row+1][cN.col].value == 0 and board[cN.row+1][cN.col].visited == False:
            queue.append(board[cN.row+1][cN.col])
            board[cN.row + 1][cN.col].visited = True
            board[cN.row + 1][cN.col].prev = cN
        if board[cN.row+1][cN.col+1].value == 0 and board[cN.row+1][cN.col+1].visited == False and cN.row %2 != 0:
            queue.append(board[cN.row+1][cN.col+1])
            board[cN.row + 1][cN.col + 1].visited = True
            board[cN.row + 1][cN.col + 1].prev = cN
        elif board[cN.row+1][cN.col-1].value == 0 and board[cN.row+1][cN.col-1].visited == False and cN.row %2 == 0:
            queue.append(board[cN.row+1][cN.col-1])
            board[cN.row + 1][cN.col - 1].visited = True
            board[cN.row + 1][cN.col - 1].prev = cN
        counter = counter +1
        if len(queue)!=0:
            cN = queue[0]
            del queue[0]


    while cN.prev != None:
        retValue.append(cN)
        cN = cN.prev
    for r in range(len(board)):
        for c in range(len(board)):
            board[r][c].visited = False
            board[r][c].prev = None
    return retValue


BLUE = (0,0,255)
SAND = (194,178,128)
GREEN = (0,128,0)
BROWN = (150,75,0)
BLACK = (0,0,0)

pygame.init()
screen = pygame.display.set_mode([1000,1000])
board = []
boardSize = 11


setupBoard(board, boardSize)

end = False
while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            end = click(pos)

if mouseLocation[0] == 0 or mouseLocation[0] == 10 or mouseLocation[1] == 0 or mouseLocation[1] == 10:
    print("YOU LOST!")
else:
    print("YOU WON!")