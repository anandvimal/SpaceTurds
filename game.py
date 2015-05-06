import pygame
import random
import sys
import pygame.mixer
import time

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)


black   = (   0,   0,   0)
white   = ( 255, 255, 255)
red     = ( 200,   0,   0)
green   = (   0, 200,   0)

bright_red = (255,0,0)
bright_green = (0,255,0)

block_color = (53,115,255)

turd_width  = 72
turd_height = 72

# Initialize Pygame
pygame.init()

#sound stuff

#sound for shooting bullets. (is called when shooting button pressed)
shoot = pygame.mixer.Sound("pew.ogg")
die = pygame.mixer.Sound("die.wav")

#background music needs to find something less lout than goteam.
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

# Set the height and width of the screen
screen_width = 640
screen_height = 640
screen = pygame.display.set_mode([screen_width, screen_height])

#this is list which contain all bullets.
bullet_list = pygame.sprite.Group()

# this one conatins all the falling objects.
object_list = pygame.sprite.Group()

all_sprites_list = pygame.sprite.Group()

#list of collision with bullets.
object_hit_list = pygame.sprite.Group()

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

'''
def load_image(name):
    image = pygame.image.load(name)
    return image
'''

'''
class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super(Block, self).__init__()

        self.image = pygame.Surface([20, 15])
        self.image.fill(color)

        self.rect = self.image.get_rect()
'''
def game_loop():
    global done, score
# -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Fire a bullet if the user clicks the mouse button
                shoot.play()
                bullet = Bullet()
                bullet2 = Bullet()

                # Set the bullet so it is where the player is
                bullet.rect.x = player.rect.x
                bullet.rect.y = player.rect.y

                #set the second bullet on right of ship
                bullet2.rect.x = player.rect.x + 90
                bullet2.rect.y = player.rect.y

                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                all_sprites_list.add(bullet2)

                bullet_list.add(bullet)
                bullet_list.add(bullet2)

        # Calculate mechanics for each bullet
        for bullet in bullet_list:

            # See if it hit a block
            object_hit_list = pygame.sprite.spritecollide(bullet, object_list, True)

            # For each block hit, remove the bullet and add to the score
            for object in object_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                score += 1
                die.play()
                print(score)

            # Remove the bullet if it fliefaces up off the screen
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)


        # Call the update() method on all the sprites
        all_sprites_list.update()

        # Clear the screen
        screen.fill(BLACK)

        # Draw all the spites
        all_sprites_list.draw(screen)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 20 frames per second
        #print("killer: "+str(Falling_Objects.object_strike))
        clock.tick(30)
        if (Falling_Objects.object_strike > 10):
            done = True


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    screen.blit(text,(0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(screen, color, [thingx, thingy, thingw, thingh])

#def car(x,y):
    #screen.blit(carImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((screen_width/2),(screen_height/2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    #game_loop()


def crash():
    message_display('You Crashed')

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Space Turds!", largeText)
        TextRect.center = ((screen_width/2),(screen_height/2))
        screen.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,bright_green, game_loop )
        button("Quit",550,450,100,50,red,bright_red,quit)
        #button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)


class Falling_Objects(pygame.sprite.Sprite):
    height = 72
    width = 72
    object_strike = 0
    def __init__(self):

        super(Falling_Objects, self).__init__()
        self.image = pygame.image.load("turd.png").convert()
        self.image.set_colorkey(BLACK)
        Falling_Objects.object_strike = 0
        #object_strike= 0
        #self.object_strike = 0
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y = self.rect.y+1
        #self.image.set_colorkey(BLACK)
        if self.rect.y > screen_height:
            Falling_Objects.object_strike += 1
            #object_strike += 1
            #self.object_strike += 1
            self.rect.y = random.randrange(-100,-10)
            self.rect.x = random.randrange(0, screen_width - self.width)


# --- Classes
class Player(pygame.sprite.Sprite):
    width = 99
    """ This class represents the block. """
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("playerShip1_orange.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        if(pos[0] > screen_width - self.width):
            self.rect.x = screen_width - self.width
        else:
            self.rect.x = pos[0]

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.image = pygame.Surface([10,40])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 10

player = Player()
player.rect.y = screen_height-100
player.rect.x = screen_width/2

all_sprites_list.add(player)

for i in range(50):
    object = Falling_Objects()
    object.rect.x = random.randrange(0, screen_width - object.width )
    object.rect.y = random.randrange(-1000,0)
    object_list.add(object)
    all_sprites_list.add(object)


game_intro()
game_loop()
pygame.quit()
