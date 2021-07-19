import pygame

screen_width = 1600
screen_height = 960

run = True

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("~Something")
clock = pygame.time.Clock()

block_list = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", ]
blockx = 0
blocky = 925

def drawGround():
    global blockx
    for i in block_list:
        i = pygame.draw.rect(screen, (255, 0, 0), (blockx, blocky, 32, 32), 4)
        blockx += 32


class Player(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.player_img = pygame.image.load(image)
        self.player_rect = self.player_img.get_rect()
        self.x = x
        self.y = y
        self.xVel = 2
        self.yVel = 10
        self.jumping = False
        self.jump_cool = 0

    def draw(self):
        self.player_rect.x = self.x
        self.player_rect.y = self.y
        
        screen.blit(self.player_img, (self.player_rect.x, self.player_rect.y))

    def check_collision(self):
        collision_buffer = 2
        if abs(some_object.left - self.player_rect.right) < collision_buffer and self.player_rect.bottom > some_object.top and self.player_rect.top < some_object.bottom and self.player_rect.left < some_object.right: #Right Collision
            return "RIGHT"
        if abs(some_object.right - self.player_rect.left) < collision_buffer and self.player_rect.bottom > some_object.top and self.player_rect.top < some_object.bottom and self.player_rect.right > some_object.left: #Left Collision
            return "LEFT"
        if abs(some_object.top - self.player_rect.bottom) < 5 and self.player_rect.right > some_object.left and self.player_rect.left < some_object.right: #Bottom Collision
            self.jumping = False
            self.yVel = 10
            return "BOTTOM"
        if abs(some_object.bottom - self.player_rect.top) < 9 and self.player_rect.right > some_object.left and self.player_rect.left < some_object.right:
            self.jumping = False
            self.yVel = 10
            return "TOP"

    def jumpCooldown(self):
        if self.jump_cool >= 30:
            self.jump_cool = 0
        elif self.jump_cool > 0:
            self.jump_cool += 1

    def jump(self, keys):
        self.jumpCooldown()
        if self.jumping is False and keys[pygame.K_SPACE] and self.jump_cool == 0 and self.check_collision() != "TOP":
            self.jumping = True
            self.jump_cool = 1

        if self.jumping == True:
            self.y -= self.yVel
            self.yVel -=1
            if self.yVel < -10:
                self.jumping = False
                self.yVel = 10

    def movement(self):
        keys = pygame.key.get_pressed()
        collisions = self.check_collision()

        if self.player_rect.bottom <= screen_height - self.yVel and self.jumping == False and collisions != "BOTTOM":
            self.y += self.yVel

        self.jump(keys)

        if keys[pygame.K_a] and self.x > self.xVel and collisions != "LEFT": #collisions != "LEFT" and 
            self.x -= self.xVel
        if keys[pygame.K_d] and self.x < screen_width - self.player_rect.width - self.xVel and collisions != "RIGHT": #collisions != "RIGHT" and 
            self.x += self.xVel
        if collisions == "BOTTOM":
            self.player_rect.x = some_object.top - 1
        
#Call classes here~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
character = Player("res/sprites/player.png", 100, 700)

while run:

    clock.tick(70)

    blockx = 0

    screen.fill((30, 30, 30))

    some_object = pygame.draw.rect(screen, (255, 0, 0), (100, blocky, 32, 32), 4)

    character.movement()
    character.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()