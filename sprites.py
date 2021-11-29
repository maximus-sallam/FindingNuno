import pygame as pg
from settings import *
vec = pg.math.Vector2
moving_up = ["img/player_03.png", "img/player_04.png"]
moving_down = ["img/player_01.png", "img/player_24.png"]
moving_left = ["img/player_15.png", "img/player_16.png"]
moving_right = ["img/player_12.png", "img/player_13.png"]

class Player(pg.sprite.Sprite):
    """Sprite player controls"""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_image_down
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

    def get_keys(self):
        """Handle's user input"""
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.image = self.game.player_image_left
            self.vel.x = -PLAYER_SPEED

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.image = self.game.player_image_right
            self.vel.x = PLAYER_SPEED

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.image = self.game.player_image_up
            self.vel.y = -PLAYER_SPEED

        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.image = self.game.player_image_down
            self.vel.y = PLAYER_SPEED

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def collide_with_walls(self, direction):
        if direction == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if direction == "y":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        """Updates entire game"""
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls("x")
        self.rect.y = self.pos.y
        self.collide_with_walls("y")


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
