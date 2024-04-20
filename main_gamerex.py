import pygame
import random


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, name, jump, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 100))
        self.add(group)
        self.rect = self.image.get_rect(center=(x, y))
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

        monstres_hit_list = pygame.sprite.spritecollide(self, monstres, False)
        for monstr in monstres_hit_list:
            monstr.kill()
            hearts.sprites()[-1].kill()


    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .95
            if self.rect.y > h:
                if heartscount > 0:
                    self.resurrection()

    def jump(self):
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 10

        if len(platform_hit_list) > 0:
            self.change_y = -20

    def go_left(self):
        self.change_x = -9

    def go_right(self):
        self.change_x = 9

    def stop(self):
        self.change_x = 0

    def resurrection(self):
        self.rect = self.image.get_rect(center=(platforms.sprites()[platformsCount - 1].rect.x+60, h-130))
        hearts.sprites()[-1].kill()

    def shoot(self):
        self.image = pygame.image.load('hero/rex_bon.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 100))

    def ordinary(self):
        self.image = pygame.image.load('hero/rex.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 100))



class Monstr(pygame.sprite.Sprite):
    def __init__(self, x, y, name, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 100))
        self.add(group)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, platfromChangeH=0):
        if platfromChangeH == 200:
            self.rect.y += platfromChangeH
        else:
            bulles_hit_list = pygame.sprite.spritecollide(self, bulles, False)
            if len(bulles_hit_list) > 0:
                self.kill()



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, name, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 50))
        self.add(group)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, platfromChangeH):
        self.rect.y += platfromChangeH


class Heart(pygame.sprite.Sprite):
    def __init__(self, name, x, y, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.add(group)
        self.rect = self.image.get_rect(center=(x, y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, name, x, y, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.add(group)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 30
        if self.rect.y < 0:
            self.kill()


class Star(pygame.sprite.Sprite):
    def __init__(self, name, x, y, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.add(group)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, platfromChangeH):
        self.rect.y += platfromChangeH


def Fon(name, x, y):
    fon = pygame.image.load(name)
    fon = pygame.transform.scale(fon, (x, y))
    rect = fon.get_rect(bottomright=(x, y))
    screen.blit(fon, rect)


def DoPlanforms(count):
    for i in range(count):
        rd = random.choice([100, 150, 200, 250, 300])
        Platform(rd, h - 50 - 200 * i, random.choice(platformsName), platforms)
        if random.randint(1, 2) == 2 and i != 0 and i != count - 1:
            Monstr(rd, h - 120 - 200 * i, random.choice(evilName), monstres)
        if i == count - 1:
            Star('things/star.png', rd, h - 120 - 200 * i, star)





pygame.init()
w, h = 400, 700
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Rex in space")
clock = pygame.time.Clock()
speed = 15
platforms = pygame.sprite.Group()
hero = pygame.sprite.Group()
hearts = pygame.sprite.Group()
bulles = pygame.sprite.Group()
monstres = pygame.sprite.Group()
star = pygame.sprite.Group()
platformsName = [f'platforms/platform{i}.png' for i in range(1, 10)]
evilName = [f'evils/evil{i}.png' for i in range(1, 3)]
platformsCount = 1
allPlatforms = 15
heartscount = 3


def gameLoop():
    global platformsCount, heartscount
    game_over = False
    game_close = False
    start_window = True
    DoPlanforms(allPlatforms)
    Hero(platforms.sprites()[0].rect.x+60, h-130, 'hero/rex.png', False, hero)
    for i in range(heartscount):
        Heart('things/heart.png', 15+i*35, 15, hearts)
    allH = h - 130
    while start_window:
        Fon("situations/start.JPG", w, h)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                start_window = False
            if event.type == pygame.QUIT:
                start_window = False
                game_close = True
    while not game_over:
        while game_close:
            for event in pygame.event.get():
                pass
            game_over = True
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_close = True
            rex = hero.sprites()[0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    rex.go_left()
                if event.key == pygame.K_RIGHT:
                    rex.go_right()
                if event.key == pygame.K_UP:
                    rex.jump()
                if event.key == pygame.K_q:
                    rex.shoot()
                    Bullet('things/bon.png', rex.rect.x, rex.rect.y, bulles)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and rex.change_x < 0:
                    rex.stop()
                if event.key == pygame.K_RIGHT and rex.change_x > 0:
                    rex.stop()
                if event.key == pygame.K_q:
                    rex.ordinary()
        if heartscount == 0:
            Fon('situations/lose.JPG', w, h)
            pygame.display.update()
        elif platformsCount == allPlatforms:
            Fon('situations/win.JPG', w, h)
            pygame.display.update()
        else:
            Fon('fon/fon.jpg', w, h)
            rex = hero.sprites()[0]
            if rex.change_y == 0:
                if rex.rect.y - allH == -200:
                    rex.rect.y += 200
                    platformsCount += 1
                    platforms.update(200)
                    monstres.update(200)
                    star.update(200)
                allH = rex.rect.y
            platforms.draw(screen)
            hero.update()
            hero.draw(screen)
            monstres.update()
            monstres.draw(screen)
            heartscount = len(hearts)
            bulles.update()
            bulles.draw(screen)
            hearts.draw(screen)
            star.draw(screen)
            pygame.display.update()
            clock.tick(speed)
    pygame.display.update()

gameLoop()


