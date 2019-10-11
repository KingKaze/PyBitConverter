import pygame, random, sys

#Initialise pygame and open or create file to save to
pygame.init()

#Intro ask for number of bits, loop if not between 8 and 16, append to list so many times
def create_list():
    print("Enter number of bits. Min 8 & Max 16")
    bits = int(input("Bits: "))
    while True:    
        if 7 < bits < 17 :
            print("Creating the UI...")
            counter = 0 
            while counter < bits:
                bit_list.append(pygame.Color("#FFFFFF"))
                counter += 1
                print(counter)
            break
        else:
            print("Invalid number of bits, try again")
            bits = int(input("Bits: "))
        
bits = 0
bit_list = []
create_list()
    
#Defined some colours for the window
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
grey = (192,192,192)

#Each box dimensions
boxW = 50
boxH = 90
#Global variable for left mouse button
MLEFT = 1
#FPS tickrate
fps=30
#Colours for the boxes, used as binary bit values, to add more bits add more values to the list

clock = pygame.time.Clock()

#Define screen dimenions and assign to a variable
screen_width = 1000
screen_height = 300
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Bit Program ~DOMINIK N~")

rects = pygame.sprite.Group()

#Class for the rectangles which inherits from the Rect class.
class DrawableRect(pygame.sprite.Sprite):
    def __init__(self,color,width,height,value=0):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.value = value
        self.color = color
        self.x = 0
        self.y = 0
    def change_value(self,color,value):
        self.image.fill(color)
        self.value=value
    def check_pos(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    def change_state(self,color,index):
        print("original", color)
        if color == (255,255,255,255):
            bit_list[index] = pygame.Color("#FF0000")
        elif color == (255,0,0,255):
            bit_list[index] = pygame.Color("#FFFFFF")
        print("switch colours")

#Creates 8 sprites of rectangles and puts them into group
def draw_rects(start_x, start_y, rect_spacing, bit_list): 
    current_x_pos = start_x
    rects.empty()
    for rect_num in range(0,len(bit_list)):
        rect = DrawableRect(bit_list[rect_num], boxW, boxH)
        rect.rect.x = current_x_pos
        rect.rect.y = start_y
        current_x_pos = current_x_pos + rect.rect.width + rect_spacing
        rects.add(rect)
    rects.draw(screen)

#Returns a binary number
def convert(states):
    numbers = states
    binary = ""
    for number in numbers:
        if number == pygame.Color("#FF0000"):
            binary += "1"
        elif number == pygame.Color("#FFFFFF"):
            binary += "0"
    
    return int(binary, 2)

def text_objects(text, font):
    textSurface = font.render(text,True,black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=0):
    #Button turns red when hovered
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen,ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            if action == "save":
                save_file(convert(binary_num))
    else:
        pygame.draw.rect(screen,ic,(x,y,w,h))

    button_font = pygame.font.SysFont("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, button_font)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect) #Draw text

def save_file(number):
    text_file = open("BinaryOutput.txt", "a")
    bit_amount = "#0" + str(len(bit_list) + 2) + "b"
    if number != 0:
        print("inside write function")
        text_file.write("({0} bits) {1} is: {2} decimal\n".format(len(bit_list),format(number, bit_amount), number))
    else:
        return
    text_file.close()
    
def terminate(): #Exit program

    pygame.quit()
    sys.exit()

#Loop which runs once per frame until terminated through function                    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == MLEFT:
            print(rects.sprites())
            counter = 0
            for box in rects:
                if box.check_pos() == True:
                    print("first loop", counter)
                    box.change_state(box.color, counter)
                    print("switched!!!", box.color)
                counter += 1
            
    screen.fill(black) #Paint window black
    mouse = pygame.mouse.get_pos() #Get mouse position

    try:
        draw_rects(screen_width*0.01, screen_height*0.1,10,bit_list) #Function renders the 8 rectangles
    except:
        print("Could not render rectangles")
    else:
        print("Rectangles rendered successfuly.")

    button("Save to file",520,205,100,50,grey,green,"save") #Button function for save file

    #Text which displays the decimal number
    screen_font = pygame.font.SysFont("monospace",60)

    binary_num = bit_list
    converted = screen_font.render(str(convert(binary_num)), 0,(80,200,80))
    
    screen.blit(converted,(80,200)) #Draw

    #Debugging tools for Python shell window
    print(mouse) #Print mouse position
    print(convert(binary_num))

    pygame.display.flip() #Update the entire screen
    clock.tick(fps)
