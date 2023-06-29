import pygame
import sys
import time
from settings import *
from sprites import BG, Ground, Plane, Obstacle


class Game:
    def __init__(self):

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.active = True

        self.load_digit_images()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # sprite setup
        BG(self.all_sprites)
        Ground([self.all_sprites, self.collision_sprites])
        # self.all_sprites.add(BG())
        self.plane = Plane(self.all_sprites)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)
        self.start_offset = 0

        # text
        self.score = 0
        self.start_offset = 0

        # menu
        self.menu_surf = pygame.image.load(
            'graphics/flappy_beans/png/gameover.png')
        self.menu_rect = self.menu_surf.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    def load_digit_images(self):
        self.digit_images = {}
        for i in range(10):
            image_path = f'graphics/flappy_beans/png/{i}.png'
            digit_image = pygame.image.load(image_path).convert_alpha()
            digit_image.set_colorkey((255, 255, 255))
            scaled_digit_image = pygame.transform.scale(
                digit_image, (30, 30))  # Adjust the scale as needed
            self.digit_images[str(i)] = scaled_digit_image

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)
        score_str = str(self.score)
        digit_width = 20
        x = 10
        y = 10

        for digit in score_str:
            if digit in self.digit_images:
                digit_image = self.digit_images[digit]
                self.display_surface.blit(digit_image, (x, y))
                x += digit_width

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.plane.kill()

    def run(self):
        last_time = time.time()
        is_start_screen = True
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.plane = Plane(self.all_sprites)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites])
            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            # self.collisions()
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)


if __name__ == "__main__":
    game = Game()
    game.run()
