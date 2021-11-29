import sys, os
import pygame

BACKGROUND = pygame.image.load('C:/Users/DrMaxipadMD/Pictures/Personal/map.png')
BACKGROUND_RECT = BACKGROUND.get_rect()

class Player(pygame.sprite.Sprite):
    """Sprite player controls"""
    def __init__(self, startx, starty):
        super(Player, self).__init__()
        self.image_dict = self.create_image_dict()
        self.animation_lists = self.create_animation_lists()
        self.image_list = self.animation_lists['walking_down']
        self.image_index = 0
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect(x=startx, y=starty)
        self.state_dict = self.create_state_dict()
        self.state = 'resting'
        self.x_vel = 0
        self.y_vel = 0
        self.timer = 0.0


    def create_image_dict(self):
        """Creates a dictionary for all images"""

        walk_left_1 = pygame.image.load("img/player_14.png")
        walk_left_2 = pygame.image.load("img/player_15.png")
        walk_left_3 = pygame.image.load("img/player_16.png")
        walk_right_1 = pygame.image.load("img/player_11.png")
        walk_right_2 = pygame.image.load("img/player_12.png")
        walk_right_3 = pygame.image.load("img/player_13.png")
        walk_up_1 = pygame.image.load("img/player_02.png")
        walk_up_2 = pygame.image.load("img/player_03.png")
        walk_up_3 = pygame.image.load("img/player_04.png")
        walk_down_1 = pygame.image.load("img/player_23.png")
        walk_down_2 = pygame.image.load("img/player_24.png")
        walk_down_3 = pygame.image.load("img/player_01.png")


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
        state_dict = {'walking_left': self.walking_left,
                      'walking_right': self.walking_right,
                      'walking_up': self.walking_up,
                      'walking_down': self.walking_down,
                      'resting': self.resting}

        return state_dict

    def walking_left(self):
        """Called when player is in a walking state"""
        if self.direction == 'left':
            self.x_vel = -5
        else:
            self.x_vel = 5

        self.image_list = self.animation_lists['walking_left']
        self.rect.x += self.x_vel
        self.image = self.animation()


    def walking_right(self):
        """Called when player is in a walking state"""
        if self.direction == 'right':
            self.x_vel = 5
        else:
            self.x_vel = 5

        self.image_list = self.animation_lists['walking_right']
        self.rect.x += self.x_vel
        self.image = self.animation()


    def walking_up(self):
        """Called when player is in a walking up state"""
        if self.direction == 'up':
            self.y_vel = -5
        else:
            self.y_vel = 5

        self.image_list = self.animation_lists['walking_up']
        self.rect.y += self.y_vel
        self.image = self.animation()


    def walking_down(self):
        """Called when player is in a walking down state"""
        if self.direction == 'down':
            self.y_vel = 5
        else:
            self.y_vel = 5

        self.image_list = self.animation_lists['walking_down']
        self.rect.y += self.y_vel
        self.image = self.animation()


    def resting(self):
        """Called when player is stationary"""
        pass


    def animation(self):
        """Animates the player"""
        if (self.current_time - self.timer) > 200:
            if self.image_index < (len(self.image_list) - 1):
                self.image_index += 1
            else:
                self.image_index = 0
            self.timer = self.current_time

        return self.image_list[self.image_index]


    def update(self, current_time, keys):
        """Updates player state"""
        self.current_time = current_time
        self.handle_input(keys)
        state_function = self.state_dict[self.state]
        state_function()


    def handle_input(self, keys):
        """Handle's user input"""
        if keys[pygame.K_UP]:
            self.state = 'walking_up'
            self.direction = 'up'
        elif keys[pygame.K_RIGHT]:
            self.state = 'walking_right'
            self.direction = 'right'
        elif keys[pygame.K_LEFT]:
            self.state = 'walking_left'
            self.direction = 'left'
        elif keys[pygame.K_DOWN]:
            self.state = 'walking_down'
            self.direction = 'down'
        else:
            self.state = 'resting'


class Game(object):
    """Controls entire game"""
    def __init__(self):
        self.screen = self.setup_pygame()
        self.screen_rect = self.screen.get_rect()
        self.player_group = self.create_player()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.done = False
        self.current_time = 0.0


    def setup_pygame(self):
        """Initializes pygame and produces a surface to blit on"""
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption('Walking Demo')
        screen = pygame.display.set_mode((800, 600))

        return screen


    def create_player(self):
        """Creates a player to control"""
        sprite_group = pygame.sprite.Group()
        player = Player(100, 500)
        sprite_group.add(player)

        return sprite_group


    def update(self):
        """Updates entire game"""
        while not self.done:
            self.current_time = pygame.time.get_ticks()
            self.keys = self.get_user_input()
            self.player_group.update(self.current_time, self.keys)
            self.screen.blit(BACKGROUND, BACKGROUND_RECT)
            self.player_group.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.fps)


    def get_user_input(self):
        """Get's user events and keys pressed"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

        keys = pygame.key.get_pressed()

        return keys


if __name__ == '__main__':
    game = Game()
    game.update()
    pygame.quit()
    sys.exit()
