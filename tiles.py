import pygame, csv, os

#tiles.py is used to get requested tile assets and draw the map based off the CSV file by creating an instance of Tile() for every positive number. 

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet): #Tile() takes the name of the image to grab from the JSON file, and x and y position to render the tile and a spritesheet for where to pull the image from. 
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image) #Calling the parse_sprite function in spritesheet.py to cut out an image from the spritesheet and assigning it to the image variable.
        self.rect = self.image.get_rect() #Assigning a rectangle to the tile (Later used for collisions and shit)
        self.rect.x = x #Setting x variable
        self.rect.y = y #Setting y variable
        
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y)) #This will draw each tile at 0, 0 in the Surface passed in which will be the Surface made in TileMap() and THAT Surface will be drawn into the canvas which will THEN be drawn in the window.

class TileMap():
    def __init__(self, filename, spritesheet): #The spritesheet parameter here will actually be the one created and assigned in the main.py, NOT THE ACTUAL SPRITESHEET IMAGE. The filename is the map CSV file to be used.
        self.tile_size = 32 #Declaring tile size
        self.start_x, self.start_y = 0, 0 #Declaring where to start drawing tiles. These variables are cached so we can update where to draw tiles. 
        self.spritesheet = spritesheet #Spritesheet variable (The one made in main.py)
        self.tiles = self.load_tiles(filename) #Calling load_tiles on the CSV file which will light off parsing the map and creating an array that contains all the created Tile() instances. 
        self.map_surface = pygame.Surface((self.map_w, self.map_h)) #Creating the Surface to draw all the tile to. Passing in map_w and map_h. These variables will later be edited to be the size of the screen itself.
        self.map_surface.set_colorkey((0,0,0)) #Setting color key for transparent colors
        self.load_map() #Calling load_map which will actually DRAW the tiles onto the map Surface.

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0)) #Takes the final map_surface as an input and draws it at 0, 0

    def load_map(self):
        for tile in self.tiles: #Gets the tile array that has finished processing in load_tiles and iterates through them.
            tile.draw(self.map_surface) #For each tile in the array, it draws it to the map Surface. After this is done the map is ready to be rendered. 

    def read_csv(self, filename): #read_csv will read all the data in the map CSV file and input it into an array for later use.
        map = [] #Making the array to store the map in.
        with open(os.path.join(filename)) as data: #Open the CSV
            data = csv.reader(data, delimiter=',') #Set the reader and the delimiter
            for row in data: #Iterate through each row
                map.append(list(row)) #Put every row into a list (Nested array for x and y coords)
        return map #Return the finished map array.

    def load_tiles(self, filename):
        tiles = [] #Creating the tiles array to store all the finished tiles in
        map = self.read_csv(filename) #Calling the read_csv function with the CSV file
        x, y = 0, 0 #Setting x and y variables used for getting the position when we loop through the map CSV file
        for row in map: #Looping through each row
            x = 0 #Every row we go through we have to set x back to the starting position
            for tile in row: #For each number in each row we will start creating the tiles. 
                if tile == '1': #This is saying that if the number in the CSV file is equal to "whatever" then we will draw a certain tile for it
                    tiles.append(Tile('grass1.png', x * self.tile_size, y * self.tile_size, self.spritesheet)) #Creating an instance of Tile() for every "0". This will get passed the name of the tile we want to grab the position is gonna be whatever x and y we are at times the tile size. 
                    #Then its passing the instance of the Spritesheet class we made in main.py and pass it off to Tile().
                elif tile == '2':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size #"1" is the player. Setting the starting position for it here
                elif tile == '0':
                    tiles.append(Tile("dirt1.png", x * self.tile_size, y * self.tile_size, self.spritesheet))
                x+=1 #Adding one to x in each loop
            y+=1 #Once the loop is done we add to y and it will set x back to 0
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size #Setting map_w and map_h to the last value of x and y times the tile size.
        return tiles #Returning the list of tiles to the __init__ function.