import pygame
from settings import *
from random import choice, randint


class BG(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        bg_image = pygame.image.load(
            'graphics/flappy_beans/png/background.png').convert_alpha()

        scale_factor = (WINDOW_WIDTH + 2) / \
            bg_image.get_width()  # Adjust the scale factor

        full_sized_image = pygame.transform.scale(
            bg_image, (int(bg_image.get_width() * scale_factor), WINDOW_HEIGHT))

        self.image = pygame.Surface((WINDOW_WIDTH * 2, WINDOW_HEIGHT))
        # Overlap the images by 1 pixel
        self.image.blit(full_sized_image, (-1, 0))
        # Adjust the blit position
        self.image.blit(full_sized_image, (WINDOW_WIDTH - 1, 0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)


class Ground(pygame.sprite.Sprite):
    def __init__(self, groups):
        # super().__init__(groups)
        # ground_surf = pygame.image.load(
        #     'graphics/flappy_beans/png/ground.png').convert_alpha()
        # self.image = pygame.transform.scale(
        #     ground_surf, pygame.math.Vector2(ground_surf.get_size()) * scale_factor)
        # self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        super().__init__(groups)
        self.sprite_type = 'ground'
        ground_surf = pygame.image.load(
            'graphics/flappy_beans/png/ground.png').convert_alpha()
        scale_factor = WINDOW_WIDTH / ground_surf.get_width()  # Calculate the scale factor

        width = ground_surf.get_width()
        height = ground_surf.get_height()

        # self.image = pygame.transform.scale(
        #     ground_surf, (scaled_width, scaled_height))

        # self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        # self.pos = pygame.math.Vector2(self.rect.topleft)
        self.image = pygame.Surface(
            (WINDOW_WIDTH * 2, height), pygame.SRCALPHA)
        self.image.blit(ground_surf, (0, 0))  # Blit the first ground image
        # Blit the second ground image
        self.image.blit(ground_surf, (width, 0))
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx < 300:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)


class Plane(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # image
        self.import_frames()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # rect
        self.rect = self.image.get_rect(
            midleft=(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement
        self.gravity = 600
        self.direction = 0

    def import_frames(self):
        self.frames = []
        for i in range(3):
            surf = pygame.image.load(
                f'graphics/flappy_beans/png/bean{i + 1}.png').convert_alpha()
            surf.set_colorkey((255, 255, 255))
            scaled_surf = pygame.transform.scale(
                surf, (int(surf.get_width() * 0.15), int(surf.get_height() * 0.15)))
            self.frames.append(scaled_surf)

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction = -400

    def animate(self, dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_bean = pygame.transform.rotozoom(
            self.image, -self.direction * 0.06, 1)
        rotated_bean.set_colorkey((0, 0, 0))
        self.image = rotated_bean
        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.sprite_type = 'obstacle'
        orientation = choice(('up', 'down'))
        surf = pygame.image.load(
            f'graphics/flappy_beans/png/obs{choice([1, 2])}{orientation}.png').convert_alpha()
        self.image = pygame.transform.scale(
            surf, (int(surf.get_width() * 1.2), int(surf.get_height() * 1.2)))

        x = WINDOW_WIDTH + randint(40, 100)

        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(10, 50)
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            y = randint(-50, -10)
            self.rect = self.image.get_rect(midtop=(x, y))

        self.pos = pygame.math.Vector2(self.rect.topleft)
        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right < -100:
            self.kill()
