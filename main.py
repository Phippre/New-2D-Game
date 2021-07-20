import pygame
from tiles import *
from spritesheet import Spritesheet

screen_width = 1600
screen_height = 960

run = True

canvas = pygame.Surface((screen_width, screen_height))
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("~Something")
clock = pygame.time.Clock()

spritesheet = Spritesheet('res/sprites/spritesheet.png')
player_img = spritesheet.parse_sprite('player.png')
player_rect = player_img.get_rect()

map = TileMap('res/map.csv', spritesheet)
player_rect.x = map.start_x
player_rect.y = map.start_y

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    canvas.fill((30, 30, 30))
    map.draw_map(canvas)
    canvas.blit(player_img, player_rect)
    screen.blit(canvas, (0, 0))
    pygame.display.update()

pygame.quit()