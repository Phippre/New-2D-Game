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
player = Player()
#Delcaring the player image by parsing the spritesheet for the player.png. This will automatically search through the JSON file for coordinates and send back a processed image on a Surface, ready to display to the canvas. 
#player_img = spritesheet.parse_sprite('player.png')
#player_rect = player_img.get_rect()
#Creating a map, passing the map csv file, passing the spritesheet instance created earlier
map = TileMap('res/map.csv', spritesheet)
player.position.x, player.position.y = map.start_x, map.start_y
#player_rect.x = map.start_x
#player_rect.y = map.start_y

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

    player.update(dt)

    canvas.fill((30, 30, 30))
    #Drawing the map onto the canvas
    map.draw_map(canvas)
    player.draw(canvas)
    #Drawing the player on the canvas
    #canvas.blit(player_img, player_rect)
    #Drawing the canvas onto the screen at 0, 0
    screen.blit(canvas, (0, 0))
    pygame.display.update()

pygame.quit()