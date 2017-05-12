import sys, time, pygame
pygame.init()

size = width, height = 1000, 400
speed = [2, 2]
black = 0, 0, 0

class Game_world:
    w, h = 10, 5
    
    def __init__(self):
        self.blockworld = [[255 for y in range(self.h)] for x in range(self.w)]
    def load(self, image):
        surface = pygame.image.load("game_world.png")
        surfacerect = surface.get_rect()
        self.w = surfacerect.w
        self.h = surfacerect.h
            
        print(str(surfacerect.w)+ " world w " + str(surfacerect.h) + " world h")
        world_string = pygame.image.tostring(surface, "RGB")
        for x, byte in enumerate(world_string):
            print(byte)
            jumpOver = x/3
            if(x % 3 == 0):
                # self.blockworld = [[byte for xx in range(self.w)] for y in range(self.h)]
                
                xx = int(jumpOver%self.w)
                yy = int(jumpOver//self.w)
                print(str(xx) + " " + str(yy))
                self.blockworld[xx ][yy] = byte
                print(byte)
            
        
    def save(self, image):
        # elements = [5]
        # byte_object = bytes(elements)
        # print(byte_object)
        world_string = b''
        # for y, column in enumerate(self.blockworld):
            # for x, row in enumerate(column):
        # for x in self.blockworld:
            # for y in x:
                # world_string = world_string + bytes([y]) + bytes([253]) + bytes([254]) 
        # for column in self.blockworld:
            # for row in column:
        for i in range(self.w * self.h):
            x = i % self.w
            y = i // self.w
            world_string = world_string + bytes([self.blockworld[x][y]]) + bytes([253]) + bytes([254])    #bad performance?
        # print(world_string)
        # inten = 255
        # letter = b'' + b'a'
        # for x in world_string:
            # print(x)
        
        # print(letter)
        surface = pygame.image.fromstring(world_string, (self.w, self.h), "RGB")
        # surface = pygame.image.fromstring(world_string, (10, 5), "ARGB")
        pygame.image.save(surface, "game_world.png")
        # pygame.image.save(
        
        
        # Hmm... For the save/load thing
# Why not using prickle?
# Like, import pickle
# with open("savegame", "wb") as f:
    # pickle.dump(foo, f)
# Considerating that your entire game state is stored in the foo object
# Lord Alucard - Today at 2:00 AM
# Then, to load

# with open("savegame", "rb") as f:
    # foo = pickle.load(f)
    
# https://docs.python.org/3/library/pickle.html
        
        
# >>> chr(97)
# 'a'
# >>> ord('a')
# 97

# tostring(Surface, format, flipped=False) -> string        
#fromstring(string, size, format, flipped=False) -> Surface
# pygame.image.tostring()
# pygame.image.fromstring()
game_world = Game_world()

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.bmp")
ballrect = ball.get_rect()
blockpic = pygame.image.load("block.bmp")
blockrect = blockpic.get_rect()
placeholderpic = pygame.image.load("placeholder.bmp")
placeholderrect = placeholderpic.get_rect()
playerpic = pygame.image.load("player.bmp")
# pygame.image.save
blocksize = blockrect.w
#print(blocksize)
zoom = 1
zoomwheelmult = 1.05

screenpos = xpos, ypos = 0, 0

def windowPosToGamePos(windowPos):
    x = (windowPos[0]-width/2)/blocksize+xpos
    y = (windowPos[1]-height/2)/blocksize+ypos
    
    return (x,y)
    
    #return((windowPos-height/2

def gamePosToWindowPos(gamePos):
    #(gamePos[0]*blocksize)-(xpos*blocksize)+width/2
	#(gamePos[1]*blocksize)-(ypos*blocksize)+height/2
	
	return ((gamePos[0]*blocksize)-(xpos*blocksize)+width/2, (gamePos[1]*blocksize)-(ypos*blocksize)+height/2)

# print(gamePosToWindowPos((1, 5))[1:2])

    
class Player:
    playerrect = playerpic.get_rect()
    playerrect.x = playerrect.x*100
    playerrect.y = playerrect.y*100
    playerspeed = xspeed, yspeed = 0, 0
    playeracceleration = xacc, yacc = 0, 1
    input = []
    # input2 = [2, 3]
    def draw(self):
        windowPos = gamePosToWindowPos((self.playerrect.x/100, self.playerrect.y/100))
        blitrect = pygame.Rect(windowPos[0], windowPos[1], self.playerrect.w, self.playerrect.h)
        #print(blitrect)
        screen.blit(playerpic, blitrect)
    def move(self, *args):
        self.playerrect.x = self.playerrect.x + args[0]
        self.playerrect.y = self.playerrect.y + args[1]
    def tick(self):
        player_input_direction = [0, 0]
        # for x in self.input2:
            # print(x)
        # print(self.input)
        for xx in self.input:
            # print("Inputloop")
            xx(player_input_direction)
        self.playerrect.x = self.playerrect.x + self.xspeed
        self.playerrect.y = self.playerrect.y + self.yspeed
        self.xacc = player_input_direction[0]
        # self.xacc = self.move_right(player_input_direction)
        self.xspeed = self.xspeed + self.xacc
        self.yspeed = self.yspeed + self.yacc
        #print(self.xacc)
        
        self.world_collide()
        
        
    def world_collide(self):

        # print(game_world.blockworld[0][-10])
        x = self.playerrect.x/100
        # print(x)
        y = self.playerrect.y/100
        # print(y)
        w = x + self.playerrect.w/blocksize
        # print(w)
        h = y + self.playerrect.h/blocksize
        # print(h)
        if(w >= 0 and x < game_world.w and h >= 0 and y < game_world.h):
            if(x < 0):
                x = 0
            if(y < 0):
                y = 0
            for yy in range(int(x), int(w+0.99)):      #something, something float precision 
                for xx in range(int(y), int(h+0.99)):
                    if (game_world.blockworld[int(xx)][int(yy)] != 0):
                        # print(str(xx) + " " + str(yy))
                        # self.halt()
                        # self.move(0, -1)
                        break
                        
    def g(self, world):
        pass                #
        
        
    
        
    def herr(self, player_rect, player_dest_rect):  #define velocity vector with this, yes... i think so
        hard_collision_bool = False # defines if the player was already in the collision to start with with
        hit_from_sides = up, down, left, right = False, False, False, False
        return (hard_collision_bool, hit_from_sides)
        
    def blockCollision(self, block_pos, player_rect, player_dest_rect):
        hard_collision = False
        block_pos[0] = block_pos[0]*100
        block_pos[1] = block_pos[1]*100
        player_rect.x = player_rect.x - 100
        player_rect.y = player_rect.y - 100
        player_dest_rect.x = player_dest_rect.x - 100
        player_dest_rect.y = player_dest_rect.y - 100
        if(block_pos[0] < x or block_pos[0] >= player_rect.w or block_pos[1] < player_rect.y or block_pos[1] >= player_rect.h ):
            pass
        else:
            hard_collision_bool = True
            print("Hard collision, what do to do now?")
            return(hard_collision_bool, 0, (player_dest_rect.x - player_dest_rect.y , player_rect.y))
        
        west_velocity = player_dest_rect.x - player_rect.x
        north_velocity = player_dest_rect.y - player_dest_rect.y
        east_velocity = player_dest_rect.x+player_dest_rect.w - (player_rect.x+player_rect.w) 
        south_velocity = player_dest_rect.y+player_dest_rect.h - (player_dest_rect.y+player_rect.h)
        north_velocity = player_dest_rect.y - player_rect.y, player_dest_rect.y - player_dest_rect.y    
        
        if(collision == True):
            return (hard_collision_bool, interpolated_frame_impact, directional_impact_vector)
    
    def move_right(self, vector):
        # print("move_right")
        #return 1
        vector[0] = 1
    def move_left(self, vector):
        # print("move_left")
        vector[0] = -1
    def add_input(self, input_method):
        self.input.append(input_method)
        # print("input")
        # print(self.-input)
    def remove_input(self, input_to_remove):
        try:
            self.input.remove(input_to_remove)
        except ValueError:     #catch if there is no input to remove
            pass
        
    def halt(self):
        self.xspeed, self.yspeed = 0, 0
        self.xacc, self.yacc = 0, 1   #always accelerate downwards?
    def jump(self):
        self.yspeed = -25


        
player = Player()
objects = []
objects.append(player)
blocks = []

fps = 0
lastsecond = 0

left_button = False
right_button = False

while 1:
    # for event in pygame.event.get():
        # if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
    
    player.tick()
    

    
    screen.fill(black)
    screen.blit(ball, ballrect)
    for x, column in enumerate(game_world.blockworld):
        for y, row in enumerate(column):
            #print(str(x)+ " " + str(y))
            if(row == 255):
                windowPos = gamePosToWindowPos((x, y))
                #print(windowPos)
                dest = pygame.Rect(windowPos[0], windowPos[1], 10, 10)
                blockrect2 = pygame.Rect(0, 0, 32, 32)
                #print(rect)
                screen.blit(blockpic, dest, blockrect2)
                #y use y for drawing specific blocks
            elif(row == 0):
                pass
            else:
                windowPos = gamePosToWindowPos((x, y))

                dest = pygame.Rect(windowPos[0], windowPos[1], 10, 10)
                blockrect2 = pygame.Rect(0, 0, 32, 32)

                screen.blit(placeholderpic, dest, blockrect2)
    
    for a in objects:
        a.draw()
    
    #event polling:
    #self.keys is [] 256 len. 
    #mouse = ((0,0), 0, 0, 0, 0, 0, 0) #(pos, b1,b2,b3,b4,b5,b6)
    #squeezing a new Apple mouse is button 6. 
    # for event in pygame.event.get():
# if event.type == pygame.QUIT:
# self.running = 0
# elif event.type == pygame.MOUSEBUTTONDOWN:
# self.mouse[event.button] = 1
# self.mouse[0] = event.pos
# elif event.type == pygame.MOUSEBUTTONUP:
# self.mouse[event.button] = 0
# self.mouse[0] = event.pos
# elif event.type == pygame.MOUSEMOTION:
# self.mouse[0] = event.pos
# elif event.type == pygame.KEYDOWN:
# self.keys[event.key % 255] = 1
# elif event.type == pygame.KEYUP:
# self.keys[event.key % 255] = 0
    
    for a in pygame.event.get():
        #print(a)
        if a.type == pygame.QUIT:
            sys.exit()
        elif(a.type == pygame.KEYDOWN):
            print("Keydown " + str(a))
            
            if(a.scancode == 45): #x
                sys.exit()
            elif(a.scancode == 57): #a
                player.jump()
            elif(a.scancode == 30):
                player.add_input(player.move_left)
            elif(a.scancode == 32): #d
                player.add_input(player.move_right)
            elif(a.scancode == 37): #k
                game_world.save("game_world")
            elif(a.scancode == 38): #l
                game_world.load("game_world")
            # x, y = pygame.mouse.get_pos()
            # player.playerrect.x = x
            # player.playerrect.y = y
        elif(a.type == pygame.KEYUP):
            print("Keyup " + str(a))
            if(False):
                pass
            elif(a.scancode == 30):
                player.remove_input(player.move_left)
            elif(a.scancode == 32):
                player.remove_input(player.move_right)
        elif(a.type == pygame.MOUSEBUTTONDOWN):
            print(a)
            if(a.button == 1):
                x, y = pygame.mouse.get_pos()
                windowPos = windowPosToGamePos((x, y))
                player.playerrect.x = windowPos[0]*100
                player.playerrect.y = windowPos[1]*100
                xpos = windowPos[0]
                ypos = windowPos[1]
            elif(a.button == 3):
                gamePos = windowPosToGamePos(a.pos)
                print(gamePos)
                if(gamePos[0] >= 0 and gamePos[0] < game_world.w and gamePos[1] >= 0 and gamePos[1] < game_world.h):
                    if(game_world.blockworld[int(gamePos[0])][int(gamePos[1])] == 255):
                        game_world.blockworld[int(gamePos[0])][int(gamePos[1])] = 0
                    else:
                        game_world.blockworld[int(gamePos[0])][int(gamePos[1])] = 255
                
            
            elif(a.button == 4):
                zoom = zoom * zoomwheelmult
                print(zoom)
            elif(a.button == 5):
                zoom = zoom / zoomwheelmult
                print(zoom)
            #print("Mousebuttondown")
    
    
    #screen.blit(ball, player.playerrect)
    pygame.display.flip()
    #print(str(pygame.mouse.get_pos()[1]) + " " + str(pygame.mouse.get_pos()[0]))
    fps = fps + 1
    if(lastsecond+1 < time.clock()):
        lastsecond = time.clock()
        #print(fps)
        fps = 0
        
    # time.sleep(0.01)
