import pygame
import json

#Spritesheet class, used for parsing through the JSON file to grab names and coordinates for the image in the spritesheet.
#Then returns the requested sprite

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename #Setting the file path inputted (your spritesheet) to a variable
        self.sprite_sheet = pygame.image.load(filename).convert() #Loading the image and converting for performance things
        self.meta_data = self.filename.replace('png', 'json') #Assigning a variable for the JSON file. Same name as the spritesheet, just replacing the PNG with JSON
        with open(self.meta_data) as f: #Opening the JSON file
            self.data = json.load(f) #Loading all the data in the JSON file into a variable for later parsing
        f.close() #Closing file

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h)) #Making a Surface specifically for setting transparency and tings
        sprite.set_colorkey((0,0,0)) #Setting color key
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h)) #Displaying the the requested sprite onto the Surface created above, displaying it at 0, 0 (on the Surface). Then we pass the variables to get the positions on where to cut out the image. 
        return sprite #Then we return the sprite. This part is confusing due to how the next function is inter-twined with this one. 

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame'] #Parsing through the data created above from the JSON file. Traversing through it with the name variable and going one step deeper to eventually get the x, y, w, h
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"] #Setting variables for the x, y, w, h inside the "sprite variable"
        image = self.get_sprite(x, y, w, h) #Calling the above function get_sprite with the parsed coordinates. In the other function it essentially cuts the image out from the spritesheet and returns it back to us.
        return image #We then return the parsed and processed image back to whatever called this function. 