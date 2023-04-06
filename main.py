#xx
import pygame
from random import randint

pygame. init()
x_resolution = 1280
y_resolution = 720
window = pygame.display.set_mode((x_resolution, y_resolution))
ballon_size = (40, 50)
dart_size = (60, 25)

def color_balloon():
    color = pygame.transform.scale(pygame.image.load("black0.png"), ballon_size) #wczytanie obrazka
    color_num = randint(0,5) #6 colors
    if color_num == 0: #green
        color = pygame.transform.scale(pygame.image.load("green0.png"), ballon_size) #wczytanie obrazka
    if color_num == 1: #red
        color = pygame.transform.scale(pygame.image.load("red0.png"), ballon_size) #wczytanie obrazka
    if color_num == 2: #blue
        color = pygame.transform.scale(pygame.image.load("blue0.png"), ballon_size) #wczytanie obrazka
    if color_num == 3: #yellow
        color = pygame.transform.scale(pygame.image.load("yellow0.png"), ballon_size) #wczytanie obrazka
    if color_num == 4: #orange
        color = pygame.transform.scale(pygame.image.load("orange0.png"), ballon_size) #wczytanie obrazka
    if color_num == 5: #purple
        color = pygame.transform.scale(pygame.image.load("purple0.png"), ballon_size) #wczytanie obrazka
    return color

class Physics:
    def __init__(self, x, y, width, height, acc, max_vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.v_hor = 0                      #poziomo
        self.v_ver = 0                      #pionowo
        self.acc = acc                      #przyspieszenie
        self.max_vel = max_vel              #prędkość maksymalna
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)  # refreshing hitbox (tutaj maska)


    def physic_tick(self):
        #self.v_ver -= 0.3
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height) #refreshing hitbox (tutaj maska)

class Power_bar(Physics):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.thick = 5
        self.clock = pygame.time.Clock().tick(120) / 1000  # max 60 fps (refreshing loop)
        self.power = 0
        self.back = pygame.rect.Rect(self.x, self. y, self.width, self.height)
        self.front = pygame.rect.Rect(self.x+self.thick, self.y+self.thick, self.width-self.thick, self.height-self.thick)
        self.green_bar = pygame.rect.Rect(self.x + self.thick, self.y + self.thick, self.power - self.thick,
                                      self.height - self.thick)
        super().__init__(x, y, width, height, 0.5, 5)


    def draw(self):
        pygame.draw.rect(window, (0, 0, 0), self.back) #black
        pygame.draw.rect(window, (255, 255, 255), self.front)
        pygame.draw.rect(window, (255, 0, 0), self.green_bar)

    def tick(self, mouse):
        self.clock += pygame.time.Clock().tick(120) / 1000  # max 60 fps (refreshing loop)
        if self.clock < 2:
            self.power = 100 * self.clock
        if pygame.mouse.get_pressed()[0]:
            print("Lewy przycisk myszki został wciśnięty!")



class Player:
    def __init__(self):
        pass

class Balloon(Physics):
    def __init__(self, x, y):
        self.x = x
        self.x = y
        self.image = color_balloon()  # wczytanie obrazka
        self.mask = pygame.mask.from_surface(self.image)
        width = self.image.get_width()
        height = self.image.get_height()
        super().__init__(x, y, width, height, 0.5, 5)  #liczy i tak sie chyba tylko ten

    def tick(self):
        Physics.physic_tick(self)
    def draw(self):
        window.blit(self.image, (self.x, self.y))

class Dart(Physics):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load("dart0.png"), (dart_size))  # wczytywanie grafiki
        self.mask = pygame.mask.from_surface(self.image)
        width = self.image.get_width()
        height = self.image.get_height()
        super().__init__(x, y, width, height, 0.5, 5)

    def tick(self, keys):
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.x += 1
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.x -= 1

        Physics.physic_tick(self)

    def draw(self):
        window.blit(self.image, (self.x, self.y))

class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(window, (128,128,128), self.hitbox)

class Stage:
    def __init__(self):
        pass



def main():
    run = True
    clock = 0

    power_bar = Power_bar(400,500,250,100)
    dart = Dart(100,130)
    balloon = Balloon(400, 100)

    while run:
        window.fill((200, 200, 200))
        clock += pygame.time.Clock().tick(120) / 1000  # max 60 fps (refreshing loop)
        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        power_bar.tick(mouse)
        dart.tick(keys)
        balloon.draw()
        dart.draw()
        power_bar.draw()
        if dart.mask.overlap(balloon.mask, (balloon.x - dart.x, balloon.y - dart.y)):
            balloon.x = 800

        pygame.display.update()

if __name__ == "__main__":
    main()
