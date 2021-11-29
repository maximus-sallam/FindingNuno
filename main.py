import ntpath as path
import pygame as pg
from settings import *
from sprites import *
from tilemap import *


class Game(object):
    """Controls entire game"""
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.current_time = 0.0
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.map = Map(path.join(game_folder, "map.txt"))
        self.player_image_down = pg.image.load(path.join(img_folder, PLAYER_IMAGE_DOWN))
        self.player_image_up = pg.image.load(path.join(img_folder, PLAYER_IMAGE_UP))
        self.player_image_left = pg.image.load(path.join(img_folder, PLAYER_IMAGE_LEFT))
        self.player_image_right = pg.image.load(path.join(img_folder, PLAYER_IMAGE_RIGHT))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.current_time = pg.time.get_ticks()
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()

    def update(self):
        """Updates entire game"""
        self.all_sprites.update()
        self.camera.update(self.player)

#    def draw_grid(self):
#        for x in range(0, WIDTH, TILESIZE):
#            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
#        for y in range(0, HEIGHT, TILESIZE):
#            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
#        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        """Get's user events and keys pressed"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
