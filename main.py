import pygame
from pygame.math import Vector2
import math
FPS = 60


class OneTileMap(pygame.sprite.Sprite):
    def __init__(self, tile, place, *group):
        super(OneTileMap, self).__init__(*group)
        self.map = [[int(j) for j in i.split()] for i in open('maps/{}'.format(place)).read().split('\n') if
                    i != ' ' and i != '\n']
        self.cell_size = 100
        self.tile = pygame.transform.scale(tile, (self.cell_size, self.cell_size))
        self.width = len(self.map[0]) * self.cell_size
        self.height = len(self.map) * self.cell_size
        self.cell_size_objects = self.cell_size // 2
        self.image = pygame.Surface((self.width, self.height))
        self.render(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def render(self, surface):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 1:
                    surface.blit(self.tile, (self.cell_size * i, self.cell_size * j))


class Hard_Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super(Hard_Enemy, self).__init__(*groups)  # initial position
        self.image = pygame.Surface((50, 100))
        self.image.fill(pygame.Color('red'))
        self.rect = self.image.get_rect()
        self.x, self.y = Vector2(pos)
        self.speed = 30
        self.move_up = False

    def move(self, player):
        # find normalized direction vector (dx, dy) between enemy and player
        dx, dy = self.rect.x - player.rect.x, self.rect.y - player.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        # move along this normalized vector towards the player at current speed
        if not self.move_up:
            self.x -= dx * self.speed
            self.y -= dy * self.speed
            if self.x <= 0 or self.y <= 0 or self.x >= WIDTH or self.y >= HEIGHT:
                self.move_up = True
        else:
            self.move_up = True
            self.x += dx * self.speed
            self.y += dy * self.speed
            if self.x <= 0 or self.y <= 0 or self.x >= WIDTH or self.y >= HEIGHT:
                self.move_up = False


class Hero(pygame.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load('images/Personaj_1.png')
        self.pos = Vector2(pos)
        self.rect = self.image.get_rect(center=pos)
        self.vel = Vector2(0, 0)
        self.speed = 9
        self.dollars = 0

    def handle_event(self, event):
        # Move player
        if event.type == pygame.KEYDOWN:
            self.update()
            if event.key == pygame.K_d:
                self.vel.x = self.speed
            if event.key == pygame.K_a:
                self.vel.x = -self.speed
            if event.key == pygame.K_w:
                self.vel.y = -self.speed
            if event.key == pygame.K_s:
                self.vel.y = self.speed

        # hero can't slide
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.vel.x > 0:
                self.vel.x = 0
            elif event.key == pygame.K_a and self.vel.x < 0:
                self.vel.x = 0
            elif event.key == pygame.K_w:
                self.vel.y = 0
            elif event.key == pygame.K_s:
                self.vel.y = 0

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos


pygame.init()
pygame.mixer.init()
SIZE = pygame.FULLSCREEN
screen = pygame.display.set_mode((0, 0), SIZE)
WIDTH = screen.get_width()
HEIGHT = screen.get_height()
all_sprites = pygame.sprite.Group()
first_layer = pygame.sprite.Group()
second_layer = pygame.sprite.Group()
start_coords = WIDTH // 2, HEIGHT // 2
hero = Hero(start_coords, all_sprites, second_layer)
tile = pygame.Surface((100, 100))
pygame.draw.rect(tile, 'white', (0, 0, 100, 100), 1)
lab = OneTileMap(tile, 'map.txt', all_sprites, first_layer)
take_dollar = pygame.mixer.Sound("sounds/take_dollar")


# enemy = Hard_Enemy((0, 0), all_sprites)


def main():
    camera = Vector2(WIDTH // 2, HEIGHT // 2)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            hero.handle_event(event)
        offset = (camera - hero.pos)
        print(offset, camera, hero.pos)
        for i in all_sprites.sprites():
            i.rect.center += offset
        camera += offset
        all_sprites.update()
        screen.fill((30, 30, 30))
        first_layer.draw(screen)
        second_layer.draw(screen)
        font = pygame.font.Font(None, 36)
        text = font.render(f'dollars: {hero.dollars}', True, pygame.Color('green'))
        screen.blit(text, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
    pygame.quit()
