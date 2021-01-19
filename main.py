from random import randrange

import pygame
from pygame.math import Vector2
import math


class DrawMap(pygame.sprite.Sprite):
    def __init__(self, place, *group):
        super(DrawMap, self).__init__(*group)
        self.map = [[int(j) for j in i.split()] for i in open('maps/{}'.format(place)).read().split('\n') if
                    i != ' ' and i != '\n']
        self.cell_size = 100
        self.width = len(self.map[0]) * self.cell_size
        self.height = len(self.map) * self.cell_size
        self.cell_size_objects = self.cell_size // 2

    def render(self, offset, only_decorations=False):
        # draw map
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 1 and not only_decorations:
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, pygame.Color('white'), (rect.topleft + offset, rect.size), 1)
                elif self.map[i][j] == 2:
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size_objects,
                                       self.cell_size_objects)
                    pygame.draw.rect(screen, pygame.Color('orange'), (rect.topleft + offset, rect.size), 1)
                elif self.map[i][j] == 3:
                    # portal
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size_objects,
                                       self.cell_size_objects)
                    pygame.draw.rect(screen, pygame.Color('blue'), (rect.topleft + offset, rect.size))


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
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.vel = Vector2(0, 0)
        self.speed = 9
        self.dollars = 0
        self.health = 3
        self.image_health =pygame.image.load('images/health.png')

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
            # x
            if self.pos.x + self.vel.x - self.rect.width >= lab.width - lab.cell_size - self.rect.width:
                self.pos.x = lab.width - self.rect.width // 2 - lab.cell_size

            if self.pos.x + self.vel.x - self.rect.width <= lab.cell_size:
                self.pos.x = self.rect.width // 2 + lab.cell_size
            # y
            if self.pos.y + self.vel.y >= lab.height - lab.cell_size - self.rect.height // 2:
                self.pos.y = lab.height - (self.rect.height // 2 + lab.cell_size)

            if self.pos.y + self.vel.y <= lab.cell_size + self.rect.height // 2:
                self.pos.y = self.rect.height // 2 + lab.cell_size

    def update(self):
        # Move the player.
        self.pos += self.vel
        self.rect.center = self.pos


def render_rects():
    return [
        pygame.Rect(randrange(lab.cell_size, lab.width - lab.cell_size),
                    randrange(lab.cell_size, lab.height - lab.cell_size), 30, 10) for _ in
        range(10)]


pygame.init()
pygame.mixer.init()
SIZE = pygame.FULLSCREEN
screen = pygame.display.set_mode((0, 0), SIZE)
WIDTH = screen.get_width()
HEIGHT = screen.get_height()

all_sprites = pygame.sprite.Group()
start_coords = WIDTH // 2, HEIGHT // 2
hero = Hero(start_coords, all_sprites)
lab = DrawMap('map.txt', all_sprites)
take_dollar = pygame.mixer.Sound("sounds/take_dollar")


# enemy = Hard_Enemy((0, 0), all_sprites)


def main():
    camera = Vector2(WIDTH // 2, HEIGHT // 2)
    clock = pygame.time.Clock()
    teleportation = False
    # green rects
    background_rects = render_rects()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            hero.handle_event(event)
        all_sprites.update()
        # room teleport
        if 23 <= hero.pos.x // lab.cell_size <= 26 and 3 <= hero.pos.y // lab.cell_size <= 5 and not teleportation:
            lab.map = [[int(j) for j in i.split()] for i in open('maps/map_weapoons.txt').read().split('\n') if
                       i != ' ' and i != '\n']
            lab.width = len(lab.map[0]) * lab.cell_size
            lab.height = len(lab.map) * lab.cell_size
            hero.pos.x = 0
            hero.pos.y = 0
            teleportation = True
            background_rects = render_rects()
        # A vector that points from the camera to the player.
        heading = hero.pos - camera
        # Follow the player with the camera.
        # Move the camera by a fraction of the heading vector's length.
        camera += heading * 0.05
        # The actual offset that we have to add to the positions of the objects.
        offset = -camera + Vector2(WIDTH // 2, HEIGHT // 2)  # centering player
        screen.fill((30, 30, 30))
        # Blit all objects and add the offset to their positions.
        # enemy.move(hero)
        if (camera.x - start_coords[0] <= lab.cell_size or camera.y - start_coords[-1] <= lab.cell_size) or \
                (camera.x - start_coords[0] >= WIDTH or camera.y >= HEIGHT):
            lab.render(offset)
        else:
            lab.render(offset, True)
        for background_rect in background_rects:
            if hero.rect.colliderect(background_rect):
                take_dollar.play()
                hero.dollars += 1
                background_rects.remove(background_rect)
                background_rects.append(
                    pygame.Rect(randrange(0, lab.width - lab.cell_size * 2),
                                randrange(0, lab.height - lab.cell_size * 2), 30,
                                10))
            else:
                topleft = background_rect.topleft + offset
                pygame.draw.rect(screen, pygame.Color('green'), (topleft, background_rect.size))
        screen.blit(hero.image, hero.rect.topleft + offset)
        # screen.blit(enemy.image, (enemy.x, enemy.y))
        for i in range(hero.health):
            screen.blit(pygame.transform.scale(hero.image_health, (70, 70)), (i * 80, 0))
        font = pygame.font.Font(None, 36)
        text = font.render(f'score: {hero.dollars}', True, pygame.Color('green'))
        screen.blit(text, (0, HEIGHT - 36))
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pygame.quit()
