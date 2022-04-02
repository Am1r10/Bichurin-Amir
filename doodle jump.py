import pygame
import random
import sys

WIDTH = 550
HEIGHT = 700
FPS = 70


class Menu:
    def __init__(self, punkts):
        self.punkts = punkts

    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def menu(self):
        running = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0

        while running:
            screen.blit(menu_image, [0, 0])

            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if (mp[0] > i[0]) and (mp[0] < i[0] + 155) and (mp[1] > i[1]) and (mp[1] < i[1] + 50):
                    punkt = i[5]
            self.render(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        running = False
                        punkt = 1
                    elif punkt == 1:
                        sys.exit()
            screen.blit(screen, (0, 30))
            pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, platforms, img='Doodler.png'):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.mask = pygame.mask.from_surface(self.image)
        self.image2 = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.change_x = 0
        self.change_y = 0
        self.platforms = platforms

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35

        if self.rect.y >= HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = HEIGHT - self.rect.height

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        self.mask = pygame.mask.from_surface(self.image)

        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False, pygame.sprite.collide_mask)

        if (len(platform_hit_list) > 0) and (self.change_y > 5):
            self.change_y = -10

        self.rect.y += self.change_y


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, img='platform.png'):
        super().__init__()
        self.img = img
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load(self.img)
        self.image = pygame.transform.scale(self.image, (70, 20))
        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, width, height)
        self.change_x = random.randint(0, 3)

    def move(self):
        if self.rect.x > WIDTH - 70:
            self.change_x = -self.change_x
        elif self.rect.x < 0:
            self.change_x = -self.change_x
        self.rect.x += self.change_x


class Game:

    def game(self):
        platform_coords = [
            (150, HEIGHT - 100),
            (random.randint(0, 480), random.randint(0, 680)),
            (random.randint(0, 445), random.randint(0, 680)),
            (random.randint(0, 410), random.randint(0, 680)),
            (random.randint(0, 385), random.randint(0, 680)),
            (random.randint(0, 350), random.randint(0, 680)),
            (random.randint(0, 315), random.randint(0, 680)),
            (random.randint(0, 380), random.randint(0, 680)),
            (random.randint(0, 345), random.randint(0, 680)),
        ]

        platforms = pygame.sprite.Group()
        player = Player(150, HEIGHT - 300, platforms)
        all_sprite_list = pygame.sprite.Group()
        all_sprite_list.add(player)

        for coord in platform_coords:
            platform = Platform(coord[0], coord[1], 70, 20)
            platforms.add(platform)
            all_sprite_list.add(platform)

        pygame.font.init()
        SCORE = pygame.font.SysFont('Times New Roman', 25)

        g = 100
        b = 255
        score = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.change_x = -5
                        player.image = player.image2
                    if event.key == pygame.K_RIGHT:
                        player.change_x = 5
                        player.image = pygame.image.load('Doodler.png')
                        player.image = pygame.transform.scale(player.image, (60, 60))
                if event.type == pygame.KEYUP:
                    player.change_x = 0

            if player.rect.left == 0:
                player.rect.right = 545
            if player.rect.right == 550:
                player.rect.left = 5

            if player.rect.bottom == HEIGHT:
                running = False

            for platform in platforms:
                platform.rect.y += 2
                if score > 50:
                    platform.move()
                if platform.rect.y > HEIGHT:
                    platform.rect.y = 0
                    platform.rect.x = random.randrange(0, WIDTH - 70)
                    score += 1

            text = SCORE.render('СЧЁТ: ' + str(score), True, (0, 0, 0))
            screen.blit(bg_image, [0, 0])

            if score % 10 == 0 and b > 0:
                b -= 1
                if g > 0:
                    g -= 1

            all_sprite_list.draw(screen)
            all_sprite_list.update()
            screen.blit(text, (10, 10))

            pygame.display.update()
            clock.tick(FPS)
        else:
            global playing
            playing += 1
            menu.menu()


bg_image = pygame.image.load('bgdoodler.png')
bg_image = pygame.transform.scale(bg_image, (550, 700))
menu_image = pygame.image.load('bgdoodler.png')
menu_image = pygame.transform.scale(menu_image, (700, 800))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

punkts = [(200, 300, u'Играть', (0, 0, 0), (255, 0, 0), 0),
          (200, 340, u'Выход', (0, 0, 0), (255, 0, 0), 1)]


playing = 0


menu = Menu(punkts)
game = Game()
menu.menu()
while True:
    game.game()
