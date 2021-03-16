##an okay version of snake i made so i could test an AI but the AI didn't work

import pygame
from random import randint


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def Add(self, a):
        return Vector(self.x + a.x, self.y + a.y)

    def ScalarMultiply(self, a):
        return Vector(self.x * a, self.y * a)

    def Compare(self, a):
        return (self.x == a.x) and (self.y == a.y)

class Game:
    def __init__(self, size=32, cell=20):
        pygame.init()
        self.size = size
        self.cell = cell
        self.res = size * cell
        self.win = pygame.display.set_mode((self.res, self.res), pygame.RESIZABLE)
        pygame.display.set_caption("snake")
        self.Reset()
        
    def Run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()

            last = self.direction
            count = 0
            if self.direction.x == 0:
                if keys[pygame.K_LEFT]:
                    self.direction = Vector(-1,0)
                    count += 1
                if keys[pygame.K_RIGHT]:
                    self.direction = Vector(1,0)
                    count += 1
            if self.direction.y == 0:
                if keys[pygame.K_UP]:
                    self.direction = Vector(0,-1)
                    count += 1
                if keys[pygame.K_DOWN]:
                    self.direction = Vector(0,1)
                    count += 1
            if count > 1:
                self.direction = last

            self.Move()
            self.Draw()
            pygame.time.Clock().tick(30)
        pygame.quit()

    def Reset(self):
        self.win.fill((0,0,0))
        pygame.display.update()
        pygame.time.Clock().tick(2)
        self.snake = [Vector(self.res//2 + self.cell*i, self.res//2) for i in range(3)]
        self.Food()
        self.direction = Vector(-1,0)

    def Food(self):
        while True:
            self.food = Vector(self.cell * randint(0,self.size-1), self.cell * randint(0,self.size-1))
            if self.food not in self.snake:
                break

    def Draw(self):
        self.win.fill((0,0,0))
        for i in self.snake:
            pygame.draw.rect(self.win, (255, 255, 255), (i.x, i.y, self.cell, self.cell))
        pygame.draw.rect(self.win, (127, 127, 127), (self.food.x, self.food.y, self.cell, self.cell))
        pygame.display.update()

    def InRange(self, a):
        return a >= 0 and a <= self.res - self.cell
    
    def Move(self):
        self.snake.insert(0, self.snake[0].Add(self.direction.ScalarMultiply(self.cell)))
        if self.snake[0].Compare(self.food):
            self.Food()
        else:
            self.snake.pop()
        if not (self.InRange(self.snake[0].x) and self.InRange(self.snake[0].y)):
            self.Reset()
        for i in range(1,len(self.snake)):
            if self.snake[0].Compare(self.snake[i]):
                self.Reset()
                break
g = Game()
g.Run()
