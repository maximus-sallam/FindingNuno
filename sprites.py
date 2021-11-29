import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    """Sprite player controls"""
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_index = 0
        self.image = game.player_image_down
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE

    def create_image_dict(self):
        """Creates a dictionary for all images"""

        walk_left_1 = pg.image.load("img/player_14.png")
        walk_left_2 = pg.image.load("img/player_15.png")
        walk_left_3 = pg.image.load("img/player_16.png")

        walk_right_1 = pg.image.load("img/player_11.png")
        walk_right_2 = pg.image.load("img/player_12.png")
        walk_right_3 = pg.image.load("img/player_13.png")

        walk_up_1 = pg.image.load("img/player_02.png")
        walk_up_2 = pg.image.load("img/player_03.png")
        walk_up_3 = pg.image.load("img/player_04.png")

        walk_down_1 = pg.image.load("img/player_23.png")
        walk_down_2 = pg.image.load("img/player_24.png")
        walk_down_3 = pg.image.load("img/player_01.png")

        image_dict = {'walk_left_1': walk_left_1,
                      'walk_left_2': walk_left_2,
                      'walk_left_3': walk_left_3,
                      'walk_right_1': walk_right_1,
                      'walk_right_2': walk_right_2,
                      'walk_right_3': walk_right_3,
                      'walk_up_1': walk_up_1,
                      'walk_up_2': walk_up_2,
                      'walk_up_3': walk_up_3,
                      'walk_down_1': walk_down_1,
                      'walk_down_2': walk_down_2,
                      'walk_down_3': walk_down_3}

        return image_dict

    def create_animation_lists(self):
        """Creates the different lists of images for animation"""
        image_dict = self.image_dict

        walk_left_list = [image_dict['walk_left_1'], image_dict['walk_left_2'], image_dict['walk_left_3']]
        walk_right_list = [image_dict['walk_right_1'], image_dict['walk_right_2'], image_dict['walk_right_3']]
        walk_up_list = [image_dict['walk_up_1'], image_dict['walk_up_2'], image_dict['walk_up_3']]
        walk_down_list = [image_dict['walk_down_1'], image_dict['walk_down_2'], image_dict['walk_down_3']]

        animation_dict = {'walking_left': walk_left_list,
                          'walking_right': walk_right_list,
                          'walking_up': walk_up_list,
                          'walking_down': walk_down_list}

        return animation_dict

    def create_state_dict(self):
        """Creates a dictionary of a player's behavior states"""
        state_dict = {"walking_left": self.get_keys,
                      "walking_right": self.get_keys,
                      "walking_up": self.get_keys,
                      "walking_down": self.get_keys}

        return state_dict

    def get_keys(self):
        """Handle's user input"""
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.image = self.game.player_image_left
            self.vel.x = -PLAYER_SPEED

        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.image = self.game.player_image_right
            self.vel.x = PLAYER_SPEED

        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.image = self.game.player_image_up
            self.vel.y = -PLAYER_SPEED

        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.image = self.game.player_image_down
            self.vel.y = PLAYER_SPEED

#        if self.vel.x != 0 and self.vel.y != 0:
#            self.vel *= 0.7071

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

    def animation(self):
        """Animates the player"""
        if (self.current_time - self.timer) > 200:
            if self.image_index < (len(self.image_list) - 1):
                self.image_index += 1
            else:
                self.image_index = 0
            self.timer = self.current_time

        return self.image_list[self.image_index]

    def update(self):
        """Updates player state"""
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
