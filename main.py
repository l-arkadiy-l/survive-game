from random import randrange
import pygame
from pygame.math import Vector2


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


def main():
    pygame.init()
    SIZE = pygame.FULLSCREEN
    screen = pygame.display.set_mode((0, 0), SIZE)
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()

    clock = pygame.time.Clock()
    camera = Vector2(WIDTH // 2, HEIGHT // 2)
    hero = Hero((WIDTH // 2, HEIGHT // 2))
    # green rects
    background_rects = [pygame.Rect(randrange(-3000, 3001), randrange(-3000, 3001), 30, 10) for _ in range(500)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            hero.handle_event(event)
        hero.update()
        # A vector that points from the camera to the player.
        heading = hero.pos - camera
        # Follow the player with the camera.
        # Move the camera by a fraction of the heading vector's length.
        camera += heading * 0.05
        # The actual offset that we have to add to the positions of the objects.
        offset = -camera + Vector2(WIDTH // 2, HEIGHT // 2)  # centering player
        screen.fill((30, 30, 30))
        # Blit all objects and add the offset to their positions.
        for background_rect in background_rects:
            if hero.rect.colliderect(background_rect):
                hero.dollars += 1
                background_rects.remove(background_rect)
            else:
                topleft = background_rect.topleft + offset
                pygame.draw.rect(screen, pygame.Color('green'), (topleft, background_rect.size))

        screen.blit(hero.image, hero.rect.topleft + offset)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pygame.quit()
