from pygame import *

mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()
mixer.music.set_volume(0.3)

kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')
money.set_volume(0.4)

WIDTH, HEIGHT = 700, 525
FPS = 60

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Лабіринт")

class GameSprite(sprite.Sprite):
    def __init__ (self, sprite_image, width, height, x, y):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.image, self.rect) 

class Player(GameSprite):
    def __init__ (self, sprite_image, width, height, x, y):
        super().__init__(sprite_image, width, height, x, y)
        self.orig_image = self.image
        self.up_image = transform.rotate(self.orig_image, 90)
        self.left_image = transform.rotate(self.orig_image, -180)
        self.down_image = transform.rotate(self.orig_image, -90)
        self.dir = "right"
    def update(self):
        old_pos = self.rect.x, self.rect.y
        pressed = key.get_pressed()
        if pressed[K_UP] and self.rect.y > 0:
            self.image = self.up_image
            self.dir = "up"
            self.rect.y -= 3
        if pressed[K_DOWN] and self.rect.y < HEIGHT - 70:
            self.image = self.down_image
            self.dir = "down"
            self.rect.y += 3
        if pressed[K_LEFT] and self.rect.x > 0:
            self.image = self.left_image
            self.dir = "left"
            self.rect.x -= 3
        if pressed[K_RIGHT] and self.rect.y < WIDTH - 70:
            self.image = self.orig_image
            self.dir = "right"
            self.rect.x += 3
        for wall in walls:
            if sprite.collide_rect(self, wall):
                self.rect.x, self.rect.y = old_pos

class Enemy(GameSprite):
    def __init__(self, x, y):
        super().__init__('cyborg.png', x=x, y=y, width=30, height=30)
        self.speed = 3
    def update(self, walls):
        for w in walls:
            if sprite.collide_rect(self, wall):
                self.speed *= -1
        self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, x, y):
        super().__init__("bullet.png", x, y, 10, 20)
        self.speed = 4
    def update(self):
        """рух кулі"""
        self.rect.y -= self.speed
        if self.rect.y < -30:
            self.kill()

class Wall(GameSprite):
    def __init__(self, x, y):
        super().__init__("wall.jpg", 35, 35, x, y)

bg = transform.scale(image.load("background.jpg"), (WIDTH, HEIGHT))
player = Player('player.png', width=30, height=30, x = 40, y = 350)
gold = GameSprite('treasure.png', width=30, height=30, x = WIDTH - 100, y = 420)

class Coin(GameSprite):
    def __init__(self, x, y):
        super().__init__("coin.png", 20, 20, x + 10, y + 10)

walls = []
enemys = []
coins = []

with open('map.txt', 'r') as file:
    map = file.readlines()
    x, y = 0, 0
    for line in map:
        for symbol in line:
            if symbol == 'W':
                walls.append(Wall(x,y))
            if symbol == 'S':
                player.rect.x = x
                player.rect.y = y
            if symbol == 'F':
                gold.rect.x = x
                gold.rect.y = y
            if symbol == 'E':
                enemys.append(Enemy(x, y))
            if symbol == '.':
                coins.append(Coin(x,y))

            x+=35
        y += 35
        x = 0
count = 0
run = True
finish = False
clock = time.Clock()

font.init()
font1 = font.SysFont("Impact", 50)
result = font1.render("YOU LOSE",True, (248, 255, 148))

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        player.update()

        window.blit(bg, (0,0))
        for wall in walls:
            wall.draw()
            if sprite.collide_rect(wall, player):
               finish = True 
               kick.play()

        player.draw()
        gold.draw()
        if sprite.collide_rect(gold, player):
            finish = True
            result = font1.render("YOU WIN \n count:"+str(count), True, (248, 255, 148))
            money.play()
        for e in enemys:
            e.update(walls)
            e.draw()
            if sprite.collide_rect(e, player):
               finish = True 
               kick.play()
        for c in coins:
            c.draw()
            if sprite.collide_rect(c, player):
                coins.remove(c)
                count += 1
    else:
        window.blit(result,(255, 200))        
    display.update()
    clock.tick(FPS)