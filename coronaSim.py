import pygame
from pygame.locals import *
import time
from random import randint, choice
import matplotlib.pyplot as plt


class Person():

    def __init__(self, x, y, infected=False, quarantined=False):
        self.surf = pygame.Surface((10*DT, 10*DT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.dir = "N"
        self.cnt = 0
        self.n = randint(1, 30)*DT
        self.infected = infected
        self.quarantine = quarantined

    def update(self):
        if self.infected:
            self.surf.fill((255, 0, 0))

        if not self.quarantine:

            speed = randint(MIN_SPEED, MAX_SPEED)

            self.cnt = (self.cnt+1) % self.n

            if self.cnt == 0:
                self.dir = choice(["R", "L", "U", "D", "N"])
                self.n = randint(1, 50)

            if self.dir == "R":
                self.rect.move_ip(speed, 0)
            if self.dir == "D":
                self.rect.move_ip(0, speed)
            if self.dir == "L":
                self.rect.move_ip(-1*speed, 0)
            if self.dir == "U":
                self.rect.move_ip(0, -1*speed)

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


pygame.init()
pygame.display.set_caption('Corona')
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

MIN_SPEED = 0
MAX_SPEED = 3
TOTAL_PPL = 1000
START_INFECTED = 5
QUARANTINED_PERCENT = 0.8
DT = 0.5


def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()


running = True
persons = []
infected = []
count = []
for i in range(START_INFECTED):
    infected.append(Person(randint(0, SCREEN_WIDTH),
                           randint(0, SCREEN_HEIGHT), infected=True))
for i in range(int((TOTAL_PPL - START_INFECTED)*(1-QUARANTINED_PERCENT))):
    persons.append(Person(randint(0, SCREEN_WIDTH),
                          randint(0, SCREEN_HEIGHT)))
for i in range(int((TOTAL_PPL-START_INFECTED)*(QUARANTINED_PERCENT))):
    persons.append(Person(randint(0, SCREEN_WIDTH),
                          randint(0, SCREEN_HEIGHT), quarantined=True))
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
        elif event.type == QUIT:
            pygame.quit()
    screen.fill((0, 0, 0))

    for i in range(len(persons)):
        for j in infected:
            if persons[i]:
                p = persons[i]
                if p.rect.colliderect(j.rect):
                    p.infected = True
                    infected.append(p)
                    persons[i] = None
        if persons[i]:
            persons[i].update()
            screen.blit(persons[i].surf, persons[i].rect)

    for i in infected:
        screen.blit(i.surf, i.rect)
        i.update()

    count.append(len(infected))
    if count[-1] == 1000:
        break

    pygame.display.flip()

plt.plot(count)
plt.show()
