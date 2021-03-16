import pygame
import numpy as np
from numpy import array
from random import randint

pygame.init()
win = pygame.display.set_mode((761, 761))
pygame.display.set_caption("maze")
w = 40
x = win.get_width()//w
y = win.get_height()//w

class Node:
    def __init__(self, value, children=[], visited=False):
        self.value = value
        self.children = children[:]
        self.visited = visited

    def add(self, value):
        new = Node(value)
        new.children.append(self)
        self.children.append(new)
        return self.children[-1]

    def furthest(self, depth=0): #go in all directions, not just down
        self.visited = True
        children = False
        furthest = (self, 0)
        for i in self.children:
            if not i.visited:
                children = True
                n = i.furthest(depth+1)
                if n[1] > furthest[1]: furthest = n
        if children: return furthest
        else: return (self, depth)

    def longest(self):
        n = self.furthest()[0]
        return (n.value, n.furthest()[0].value)
        
    
class Grid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cells = array([[False]*y]*x)
        self.walls_x = array([[True]*(y+1)]*x)
        self.walls_y = array([[True]*y]*(x+1))
        self.stack = []
        self.current = array([0,0])
        self.tree = Node(self.current)

    def draw(self):
        win.fill((127,127,127))
        for i in range(self.x+1):
            for j in range(self.y+1):
                iw = i*w
                jw = j*w
                if i < self.x and j < self.y and self.cells[i][j]:
                    pygame.draw.rect(win, (0, 0, 0), (iw, jw, w, w))
                if i < self.x and self.walls_x[i][j]:
                    pygame.draw.line(win, (255, 255, 255), (iw, jw), (iw+w, jw))
                if j < self.y and self.walls_y[i][j]:
                    pygame.draw.line(win, (255, 255, 255), (iw, jw), (iw, jw+w))
        pygame.display.update()

    def run(self):
        cur_node = self.tree
        self.cells[0][0] = True
        xy = self.x*self.y
        run = True
        done = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: run = False
            while not done:
                n = self.neighbours()
                if n:
                    nxt = n[randint(0,len(n)-1)]
                    cur_node = cur_node.add(nxt)
                    self.stack.append(self.current)
                    choose = self.current
                    if sum(nxt) > sum(self.current): choose = nxt
                    if nxt[0] == self.current[0]:
                        self.walls_x[choose[0]][choose[1]] = False
                    else: self.walls_y[choose[0]][choose[1]] = False
                    self.current = nxt
                    self.cells[nxt[0]][nxt[1]] = True
                elif self.stack:
                    self.current = self.stack.pop()
                    cur_node = cur_node.add(self.current)
                else:
                    g = self.tree.longest()
                    [pygame.draw.rect(win, (255, 0, 0), (i[0]*w, i[1]*w, w, w)) for i in g]
                    pygame.display.update()
                    print(g)
                    done = True
                self.draw()
            
        pygame.quit()
                
        
    def neighbours(self):
        cx = self.current[0]
        cy = self.current[1]
        neighbours = []
        for i in array([[cx-1,cy], [cx+1,cy], [cx,cy-1], [cx,cy+1]]):
            if (i[0] >= 0 and i[1] >= 0
                and i[0] < self.x and i[1] < self.y
                and not self.cells[i[0]][i[1]]):
                neighbours.append(array([i[0],i[1]]))
        return neighbours
                
                
grid = Grid(x,y)
grid.run()
