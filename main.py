import pygame
from tiles import *
from spritesheet import Spritesheet
from player import Player

screen_width = 1600
screen_height = 960

TARGET_FPS = 60

run = True

#Creating canvas to draw to and render to the screen.
canvas = pygame.Surface((screen_width, screen_height))
#Screen is the "Window"
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("~Something")
clock = pygame.time.Clock()

#Declaring the spritesheet to use, calling the Spritesheet class. This is used to initialize the class and pass what spritesheet and JSON file we are using. 
spritesheet = Spritesheet('res/sprites/spritesheet.png')
#Creating an instance of the Player class.
player = Player()
#Creating a map, passing the map csv file, passing the spritesheet instance created earlier
map = TileMap('res/map.csv', spritesheet)
#Setting player spawn position.
player.position.x, player.position.y = map.start_x, map.start_y

while run:
    dt = clock.tick(60) * .001 * TARGET_FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.LEFT_KEY = True
            elif event.key == pygame.K_d:
                player.RIGHT_KEY = True
            elif event.key == pygame.K_SPACE:
                player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.LEFT_KEY = False
            elif event.key == pygame.K_d:
                player.RIGHT_KEY = False
            elif event.key == pygame.K_SPACE:
                if player.is_jumping:
                    player.velocity.y *= .25
                    player.is_jumping = False

    player.update(dt, map.tiles)

    canvas.fill((30, 30, 30))
    #Drawing the map onto the canvas
    map.draw_map(canvas)
    #Drawing the player. 
    player.draw(canvas)
    #Drawing the canvas onto the screen at 0, 0
    screen.blit(canvas, (0, 0))
    pygame.display.update()

pygame.quit()