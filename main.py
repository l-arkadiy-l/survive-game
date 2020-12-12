from random import randrange
import pygame
from pygame.math import Vector2
import math


class DrawMap(pygame.sprite.Sprite):
    def __init__(self, *group):
        super(DrawMap, self).__init__(*group)
        self.map = MAP
        self.cell_size = 100
        self.width = len(self.map[0]) * self.cell_size
        self.height = len(self.map) * self.cell_size
        self.cell_size_objects = self.cell_size // 2

    def render(self, offset):
        # draw map
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 1:
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, pygame.Color('white'), (rect.topleft + offset, rect.size), 1)
                elif self.map[i][j] == 2:
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size_objects,
                                       self.cell_size_objects)
                    pygame.draw.rect(screen, pygame.Color('orange'), (rect.topleft + offset, rect.size), 1)


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
        self.speed = 7
        self.dollars = 0

    def handle_event(self, event):
        # Move player
        if event.type == pygame.KEYDOWN:
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
        # Move the player.
        self.pos += self.vel
        self.rect.center = self.pos


SIZE = pygame.FULLSCREEN
screen = pygame.display.set_mode((0, 0), SIZE)
WIDTH = screen.get_width()
HEIGHT = screen.get_height()
MAP = [[int(j) for j in i.split()] for i in open('maps/map.txt').read().split('\n') if i != ' ' and i != '\n']

all_sprites = pygame.sprite.Group()
hero = Hero((WIDTH // 2, HEIGHT // 2), all_sprites)
lab = DrawMap(all_sprites)
enemy = Hard_Enemy((0, 0), all_sprites)



def main():
    pygame.init()
    camera = Vector2(WIDTH // 2, HEIGHT // 2)
    clock = pygame.time.Clock()
    # green rects
    background_rects = [
        pygame.Rect(randrange(0, lab.width - lab.cell_size), randrange(0, lab.height - lab.cell_size), 30, 10) for _ in
        range(10)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            hero.handle_event(event)
        all_sprites.update()
        # A vector that points from the camera to the player.
        heading = hero.pos - camera
        # Follow the player with the camera.
        # Move the camera by a fraction of the heading vector's length.
        camera += heading * 0.05
        # The actual offset that we have to add to the positions of the objects.
        offset = -camera + Vector2(WIDTH // 2, HEIGHT // 2)  # centering player
        screen.fill((30, 30, 30))
        # Blit all objects and add the offset to their positions.
        enemy.move(hero)
        lab.render(offset)
        for background_rect in background_rects:
            if hero.rect.colliderect(background_rect):
                hero.dollars += 1
                background_rects.remove(background_rect)
                background_rects.append(pygame.Rect(randrange(-2000, 2001), randrange(-3000, 3001), 30, 10))
            else:
                topleft = background_rect.topleft + offset
                pygame.draw.rect(screen, pygame.Color('green'), (topleft, background_rect.size))
        screen.blit(hero.image, hero.rect.topleft + offset)
        screen.blit(enemy.image, (enemy.x, enemy.y))
        font = pygame.font.Font(None, 36)
        text = font.render(f'dollars: {hero.dollars}', True, pygame.Color('green'))
        screen.blit(text, (0, 0))
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pygame.quit()
