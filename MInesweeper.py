import random
import pygame
pygame.init()

screenSize = 800       # Size of the Window
cellSize = 40          # Size of individual Cell
mines = 80             # Number of Mines in the Game
grid = []              # A 2D Array to Store all the Cells
over = False           # Is the Game Over


class Cell():
    def __init__(self, i, j):
        # (i,j) --> index of the cell in the grid
        # (x,y) --> coordinates of the cell on the board
        self.i = i
        self.j = j
        self.x = i*cellSize
        self.y = j*cellSize
        self.mine = False
        self.revealed = False
        self.nmines = 0

    def show(self, win):        # Show the cell on the Screen
        if self.revealed:
            pygame.draw.rect(win, (200, 200, 200), pygame.Rect(
                self.x, self.y, cellSize-2, cellSize-2))
            font = pygame.font.Font('freesansbold.ttf', 15)
            text = font.render(str(self.nmines), True,
                               (0, 0, 0), (200, 200, 200))
            textRect = text.get_rect()
            textRect.center = (self.x + (cellSize*0.5),
                               self.y + (cellSize*0.5))
            if self.mine:
                pygame.draw.circle(
                    win, (0, 0, 0), (self.x + int(cellSize*0.5), self.y + int(cellSize*0.5)), int(cellSize*0.25))
            else:
                if self.nmines != 0:
                    win.blit(text, textRect)
        else:
            pygame.draw.rect(win, (100, 100, 100), pygame.Rect(
                self.x, self.y, cellSize-2, cellSize-2))

    def reveal(self):       # Reveal whats inside of a cell
        global over
        self.revealed = True
        if self.mine:
            over = True
            print("You Lose")
            for rows in grid:
                for cell in rows:
                    cell.revealed = True
        for k in range(-1, 2):
            for l in range(-1, 2):
                if (self.i+k == -1) or (self.j+l == -1) or (self.i+k >= screenSize//cellSize) or (self.j+l >= screenSize//cellSize):
                    pass
                else:
                    if (grid[self.i+k][self.j+l].revealed == False) and self.nmines == 0:
                        grid[self.i+k][self.j+l].reveal()


def checkWin():             # Check if the User won
    global over
    c = 0
    for rows in grid:
        for cell in rows:
            if cell.revealed:
                c += 1
    if c == (screenSize//cellSize)**2 - mines:
        print("You Win")
        over = True


def createGrid():           # Create the grid of Cells
    for i in range(screenSize//cellSize):
        row = []
        for j in range(screenSize//cellSize):
            row.append(Cell(i, j))
        grid.append(row)


def plantMines():           # Plant the mines randomly
    global mines
    if mines > (screenSize//cellSize)**2:
        mines = (screenSize//cellSize)**2
    done = []
    for i in range(mines):
        x = random.randint(0, (screenSize//cellSize)-1)
        y = random.randint(0, (screenSize//cellSize)-1)
        while [x, y] in done:
            x = random.randint(0, (screenSize//cellSize)-1)
            y = random.randint(0, (screenSize//cellSize)-1)
        done.append([x, y])
        grid[x][y].mine = True


def calcMines():            # Count the number of neighboring mines to a cell
    for i in range(screenSize//cellSize):
        for j in range(screenSize//cellSize):
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if (i+k == -1) or (j+l == -1) or (i+k >= screenSize//cellSize) or (j+l >= screenSize//cellSize):
                        pass
                    else:
                        if grid[i+k][j+l].mine:
                            grid[i][j].nmines += 1


def main():                 # Driver Code
    global over
    win = pygame.display.set_mode((screenSize, screenSize))
    pygame.display.set_caption("MineSweeper")
    loop = True
    createGrid()
    plantMines()
    calcMines()
    # Game Loop
    while loop:
        for i in range(screenSize//cellSize):
            for j in range(screenSize//cellSize):
                grid[i][j].show(win)
        checkWin()
        if over:
            loop = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            # If player cicks a cell, the cell's content is revealed
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = x//(screenSize//(screenSize//cellSize))
                y = y//(screenSize//(screenSize//cellSize))
                grid[x][y].reveal()
        pygame.display.flip()


main()
