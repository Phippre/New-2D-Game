import pygame
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('res/sprites/spritesheet.png').parse_sprite('player.png') #Using parse_sprite to cut out the player image.
        self.rect = self.image.get_rect() #Setting a rectangle on the player image
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False #Booleans for checking if the left or right button is pressed. Essentially allows movement based on a boolean instead of adding the numbers in the movement function.
        self.is_jumping, self.on_ground = False, False #Booleans for checking if the player is jumping or on the ground
        self.gravity, self.friction = .38, -.12 #Gravity and friction numbers
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0) #Setting Vectors for the position and velocity. Each Vector holds an x and y coordinate.
        self.acceleration = pygame.math.Vector2(0, self.gravity) #Making an acceleration Vector. X is 0 for now but the Y is gravity because we want gravity to be constantly applied.

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y)) #Blitting the image to the screen at the rectangles x and y position. 

    def update(self, dt, tiles): #Update function used for updating any information on the player in the main game loop
        self.horizontal_movement(dt) #Calling horizontal movement.
        self.checkCollisionsX(tiles)
        self.vertical_movement(dt) #Calling vertical movement. 
        self.checkCollisionsY(tiles)

    def horizontal_movement(self, dt): #Handles horizontal movement.
        self.acceleration.x = 0 #Setting acceleration to 0 so the player doesnt constantly go back and forth.
        if self.LEFT_KEY:
            self.acceleration.x -= .3 #Subtracting from the acceleration if going left.
        elif self.RIGHT_KEY:
            self.acceleration.x += .3 #Adding to acceleration if going right.
        self.acceleration.x += self.velocity.x * self.friction #Adding friction here. Adds the current velocity * friction to the players acceleration. Creates illusion of speeding up and slowing down.
        self.velocity.x += self.acceleration.x * dt #Adding acceleration * dt to the velocity 
        self.limit_velocity(4) #Limiting the velocity to 4
        self.position.x += self.velocity.x * dt - (self.acceleration.x * .5) * (dt * dt) #Setting the players position varable equal to Newtons law of motion
        self.rect.x = self.position.x #Adding the current position to the rectangle location. 

    def vertical_movement(self, dt): #Handles vertical movement.
        self.velocity.y += self.acceleration.y * dt #Constantly adding the acceleration to the velocity. Y acceleration is gravity btw.
        if self.velocity.y > 10: self.velocity.y = 10 #Setting a cap on the y velocity.
        self.position.y += self.velocity.y * dt - (self.acceleration.y * .5) * (dt * dt) #Newtons law shit for movement in relation to time.
        self.rect.bottom = self.position.y #Setting the bottom of the player equal to the current position. 

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 8
            self.on_ground = False

    def get_hits(self, tiles): #Returns a list of collisions
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisionsX(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0: #For right side
                self.position.x = tile.rect.left - self.rect.width
                self.rect.x = self.position.x
            elif self.velocity.x < 0: #Left side
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    def checkCollisionsY(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0: #Hit tile from top
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.height
                self.rect.bottom = self.position.y
