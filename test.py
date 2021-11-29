import pygame as pg

BACKGROUND = pg.image.load("img/map.png")
BACKGROUND_RECT = BACKGROUND.get_rect()


class Player(pg.sprite.Sprite):
    """Sprite player controls"""
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.image_dict = self.create_image_dict()
        self.animation_lists = self.create_animation_lists()
        self.image_list = self.animation_lists["walking_down"]
        self.image_index = 0
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect(x=x, y=y)
        self.state_dict = self.create_state_dict()
        self.x_vel = 0
        self.y_vel = 0
        self.timer = 0.0

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

        image_dict = {"walk_left_1": walk_left_1,
                      "walk_left_2": walk_left_2,
                      "walk_left_3": walk_left_3,
                      "walk_right_1": walk_right_1,
                      "walk_right_2": walk_right_2,
                      "walk_right_3": walk_right_3,
                      "walk_up_1": walk_up_1,
                      "walk_up_2": walk_up_2,
                      "walk_up_3": walk_up_3,
                      "walk_down_1": walk_down_1,
                      "walk_down_2": walk_down_2,
                      "walk_down_3": walk_down_3}

        return image_dict

    def create_animation_lists(self):
        """Creates the different lists of images for animation"""
        image_dict = self.image_dict

        walk_left_list = [image_dict["walk_left_1"], image_dict["walk_left_2"], image_dict["walk_left_3"]]
        walk_right_list = [image_dict["walk_right_1"], image_dict["walk_right_2"], image_dict["walk_right_3"]]
        walk_up_list = [image_dict["walk_up_1"], image_dict["walk_up_2"], image_dict["walk_up_3"]]
        walk_down_list = [image_dict["walk_down_1"], image_dict["walk_down_2"], image_dict["walk_down_3"]]

        animation_dict = {"walking_left": walk_left_list,
                          "walking_right": walk_right_list,
                          "walking_up": walk_up_list,
                          "walking_down": walk_down_list}

        return animation_dict

    def create_state_dict(self):
        """Creates a dictionary of a player"s behavior states"""
        state_dict = {"walking_left": self.get_keys,
                      "walking_right": self.get_keys,
                      "walking_up": self.get_keys,
                      "walking_down": self.get_keys}

        return state_dict

    def animation(self):
        """Animates the player"""
        if (self.current_time - self.timer) > 200:
            if self.image_index < (len(self.image_list) - 1):
                self.image_index += 1
            else:
                self.image_index = 0
            self.timer = self.current_time

        return self.image_list[self.image_index]

    def update(self, current_time):
        """Updates player state"""
        self.current_time = current_time
        self.get_keys()
        state_function = self.state_dict["walking_down"]
        state_function()

    def get_keys(self):
        """Handle"s user input"""

        keys = pg.key.get_pressed()

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.y_vel = -2.5
            self.image_list = self.animation_lists["walking_up"]
            self.rect.y += self.y_vel
            self.image = self.animation()

        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.x_vel = 2.5
            self.image_list = self.animation_lists["walking_right"]
            self.rect.x += self.x_vel
            self.image = self.animation()

        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.x_vel = -2.5
            self.image_list = self.animation_lists["walking_left"]
            self.rect.x += self.x_vel
            self.image = self.animation()

        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.y_vel = 2.5
            self.image_list = self.animation_lists["walking_down"]
            self.rect.y += self.y_vel
            self.image = self.animation()


class Game(object):
    """Controls entire game"""
    def __init__(self):
        pg.init()
        pg.display.set_caption("Walking Demo")
        self.screen = pg.display.set_mode((800, 600))
        self.screen_rect = self.screen.get_rect()
        self.player_group = self.create_player()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.playing = True
        self.current_time = 0.0

    def create_player(self):
        """Creates a player to control"""
        sprite_group = pg.sprite.Group()
        player = Player(500, 500)
        sprite_group.add(player)

        return sprite_group

    def run(self):
        pass

    def quit(self):
        pg.quit()

    def update(self):
        """Updates entire game"""
        while self.playing:
            self.current_time = pg.time.get_ticks()
            self.player_group.update(self.current_time)
            self.screen.blit(BACKGROUND, BACKGROUND_RECT)
            self.player_group.draw(self.screen)
            pg.display.update()
            self.events()
            self.clock.tick(self.fps)

    def events(self):
        """Get"s user events and keys pressed"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()


# create the game object
if __name__ == "__main__":
    game = Game()
    game.update()
    pg.quit()
