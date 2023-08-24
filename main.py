import pygame
import pymunk
import sys
import math
from svg.path import parse_path
from svg.path.path import Line
from collections import deque
pygame.init()




# Display
screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h
display_size = (width, height)
display_surface = pygame.display.set_mode(display_size, pygame.FULLSCREEN)

main_menu_texts = ["Rocket Launch - PRESS-1", "Orbit mission - PRESS-2"]
main_menu_positions = [(width // 2, height // 2 - 50), (width // 2, height // 2 + 50)]



# Font

font = pygame.font.SysFont(None, 40)
font_color = (255,255,255)  # White font color
font2 = pygame.font.Font("images/AnkhSanctuary-nROx4.ttf", 72)


#fps and clock
clock = pygame.time.Clock()
FPS = 80



# =====GAME 1 // IMAGES RECTS AND OTHERS=====

bg1_image = pygame.image.load("images/GAME1BG2.png")
bg1_image = pygame.transform.scale(bg1_image, display_size)
bg1_rect = bg1_image.get_rect()


#rocket 
rocket_image = pygame.image.load("images/rocket1.png")
rocket_image = pygame.transform.scale(rocket_image, ((rocket_image.get_width() // 2), (rocket_image.get_height() // 2)))
rocket_rect = rocket_image.get_rect()
rocket_rect.centerx = width // 2
rocket_rect.bottom = height - 170

#launch pad
launchpad_image = pygame.image.load("images/launchpad.png")
launchpad_image = pygame.transform.scale(launchpad_image, ((launchpad_image.get_width() // 2 + 100), (launchpad_image.get_height() // 2) + 200))
launchpad_rect = launchpad_image.get_rect()
launchpad_rect.centerx = width // 2
launchpad_rect.bottom = height


#Ignition effect
ignition1_images = [
    pygame.image.load("images/ignition1.png"),
    pygame.image.load("images/ignition2.png"),
    pygame.image.load("images/ignition3.png")
]

#Resize the ignition images to be 25% smaller
ignition1_images = [pygame.transform.scale(img, (int(img.get_width() * 0.60), int(img.get_height() * 0.60))) for img in ignition1_images]
ignition1_rect = ignition1_images[0].get_rect()
ignition1_index = 0
show_ignition1 = False
ignition1_delay = 60  # Number of frames to show the ignition effect

# Bar to represent rocket ascent progress
bar_width = 20
bar_height = (height - 200)
bar_color = (0, 255, 0)
bar_rect = pygame.Rect(100, 100, bar_width, bar_height)
bar_fill_rect = bar_rect.copy()
bar_fill_height = 0


# =====GAME 2 // IMAGES RECTS AND OTHERS=====
# Images and rectangles

# Ignition effect
ignition_images = [
    pygame.image.load("images/ignition1.png"),
    pygame.image.load("images/ignition2.png"),
    pygame.image.load("images/ignition3.png")
]


bg2_image = pygame.image.load("images/newbeg.png")
bg2_image = pygame.transform.scale(bg2_image, display_size)
bg2_rect = bg2_image.get_rect()


fly1_image = pygame.image.load("images/fly1.png")
fly1_image = pygame.transform.scale(fly1_image, (int(fly1_image.get_width() * 0.6), int(fly1_image.get_height() * 0.6)))
fly1_rect = fly1_image.get_rect()
fly1_rect.center = (width // 2 - 150, height // 2 + 150)

body_image = pygame.image.load("images/body.png")
body_image = pygame.transform.scale(body_image, (int(body_image.get_width() * 0.6), int(body_image.get_height() * 0.6)))
body_rect = body_image.get_rect()
body_rect.left = fly1_rect.left
body_rect.bottom = fly1_rect.bottom - 50

fly2_image = pygame.image.load("images/fly2.png")
fly2_image = pygame.transform.scale(fly2_image, (int(fly2_image.get_width() * 0.6), int(fly2_image.get_height() * 0.6)))
fly2_rect = fly2_image.get_rect()
fly2_rect.left = body_rect.left
fly2_rect.bottom = body_rect.bottom - 50

c_body_image = pygame.image.load("images/c_body.png")
c_body_image = pygame.transform.scale(c_body_image, (int(c_body_image.get_width() * 0.6), int(c_body_image.get_height() * 0.6)))
c_body_rect = c_body_image.get_rect()
c_body_rect.left = body_rect.right - 100
c_body_rect.bottom = body_rect.bottom - 105

mouth_image = pygame.image.load("images/mouth.png")
mouth_image = pygame.transform.scale(mouth_image, (int(mouth_image.get_width() * 0.6), int(mouth_image.get_height() * 0.6)))
mouth_rect = mouth_image.get_rect()
mouth_rect.left = c_body_rect.right - 60
mouth_rect.bottom = c_body_rect.bottom - 70

chandu_image = pygame.image.load("images/chandu.png")
chandu_image = pygame.transform.scale(chandu_image, (int(chandu_image.get_width() * 0.6), int(chandu_image.get_height() * 0.6)))
chandu_rect = chandu_image.get_rect()
chandu_rect.left = c_body_rect.right - 38
chandu_rect.bottom = c_body_rect.bottom - 90


# Resize the ignition images to be 60% of the original size
ignition_images = [pygame.transform.scale(img, (int(img.get_width() * 0.3), int(img.get_height() * 0.30))) for img in ignition_images]

ignition_rect = ignition_images[0].get_rect()
ignition_rect.right = body_rect.left + 10
ignition_rect.bottom = body_rect.bottom + 70

ignition_index = 0
show_ignition = True
ignition_delay = 30  # Number of frames to show each ignition image

# FPS and clock
clock = pygame.time.Clock()
FPS = 60



# Instructions
instructions = {
    "boosters_active" : "Press SHIFT for Boosters separation",
    "mouth_active": "Press SPACE for payload fairing separation",
    "body_active": "Press ENTER for  body separation",
    "c_body_active": "Press CONTROL for CY3 separation",
    "Escape orbit": "Press Up ^ to escape the Orbit"
}




rotated_ignition = pygame.transform.rotate(ignition_images[ignition_index], -70)
rotated_ignition_rect = rotated_ignition.get_rect(center=ignition_rect.center)
rotated_ignition_rect.center = ignition_rect.center
display_surface.blit(rotated_ignition, rotated_ignition_rect)


boosters_active = False
body_active = False
c_body_active = False
mouth_active = False
spray = False

velocity = 60
gravity = 4


# Define the reset_game function
def reset_game():
    global current_state, launched, show_ignition1, boosters_active, body_active, mouth_active, c_body_active, spray, ignition_index, ignition_delay, time, moving_right, separation, drop_deck, fall, rover, fine_bracking, rough_bracking, landing, r_lander2_rect

    current_state = MAIN_MENU
    launched = False
    show_ignition1 = False
    show_ignition = False
    boosters_active = False
    body_active = False
    mouth_active = False
    c_body_active = False
    spray = False

    # Reset rocket position
    rocket_rect.centerx = width // 2
    rocket_rect.bottom = height - 170

    ignition1_rect.centerx = rocket_rect.centerx  # Align horizontally with rocket_rect
    ignition1_rect.top = rocket_rect.bottom

    # Reset progress bar
    bar_fill_height = 0

     # Reset the path_points deque
    path_points.clear()

    # Reset time and previous object position
    time = 0
    prev_object_x, prev_object_y = None, None


    # Reset Game 2 objects' positions
    fly1_rect.center = (width // 2 - 150, height // 2 + 150)
    body_rect.left = fly1_rect.left
    body_rect.bottom = fly1_rect.bottom - 50
    fly2_rect.left = body_rect.left
    fly2_rect.bottom = body_rect.bottom - 50
    c_body_rect.left = body_rect.right - 100
    c_body_rect.bottom = body_rect.bottom - 105
    mouth_rect.left = c_body_rect.right - 60
    mouth_rect.bottom = c_body_rect.bottom - 70
    chandu_rect.left = c_body_rect.right - 38
    chandu_rect.bottom = c_body_rect.bottom - 90
    ignition_index = 0
    ignition_delay = 10
    ignition_rect.right = body_rect.left + 10
    ignition_rect.bottom = body_rect.bottom + 70

    # Reset game 3 variables
    time = 0
    moving_right = False

    # Clear the Pygame window
    display_surface.fill((0, 0, 0))

    # Reset font
    font = pygame.font.SysFont(None, 36)

    # Reset instructions
    instructions = {
        "boosters_active": "Press SHIFT for Boosters separation",
        "mouth_active": "Press SPACE for payload fairing separation",
        "body_active": "Press ENTER for body separation",
        "c_body_active": "Press CONTROL for CY3 separation",
        "Escape orbit": "Press Up ^ to escape the Orbit"
    }

    

    separation = False

    chandu3_rect.center = width//2, height//2
    chandu_holder_rect.left = chandu3_rect.right-190
    chandu_holder_rect.centery = chandu3_rect.centery

    #game5 reset 
    fine_bracking = False
    rough_bracking = False
    landing = False
    non_r_lannder_rect.center == r_lander2_rect.center
    r_lander_rect.topleft = 0,-100
    r_lander2 = pygame.transform.rotate(non_r_lannder, 60)
    r_lander2 = pygame.transform.scale(r_lander2,(250,250))
    r_lander2_rect = r_lander2.get_rect()
    r_lander2_rect.topleft = 400,-100


   








    #game 6 reset
    move_car_right = False
    move_car_left = False
    rover = False
    fall = False
    drop_deck = False
    lander_rect.bottomleft = 0, 0
    deck_rect.topleft = 300, 600
    car.reset_game()
    # Update the display
    pygame.display.update()










# Game states
MAIN_MENU = 0
GAME1 = 1
GAME2 = 2
GAME3 = 3
GAME4 = 4 
GAME5 = 5
GAME6 = 6
current_state = MAIN_MENU
launched = False

## game 3

# Object properties
object_radius = 10
object_color = (0, 255, 255)
line_color = (255, 255, 255)  # Black line color

# Parse the SVG path data
svg_path_data = "M 235 330 A 1 1 0 0 0 280 98 A 1 1 0 0 0 271 481 A 1 1 0 0 0 207 61 A 1 1 0 0 0 335 550 C 635 492 642 361 866 244 C 1102 63 1300 102 1391 349 Q 1401 548 1272 630 T 976 632 Q 791 476 915 307 Q 1049 184 1180 235 C 1493 377 1221 744 1020 585 C 863 447 945 286 1200 310"
svg_path = parse_path(svg_path_data)

# Time parameter for interpolation
time = 0

# Previous position of the object
prev_object_x, prev_object_y = None, None

# Deque to store points of the path
path_points = deque(maxlen=1200)

# Movement control flag
moving_right = False

# Load Earth and Moon images
earth_image = pygame.image.load("images/earth1.png")
moon_image = pygame.image.load("images/moon1.png")

# Resize the images to 60 pixels
earth_image = pygame.transform.scale(earth_image, (250, 250))
moon_image = pygame.transform.scale(moon_image, (60, 60))
moon_image_rect = moon_image.get_rect()
moon_image_rect.topleft = (1151, 310)


# Load the background image for GAME3
bg3_image = pygame.image.load("images/GAME3BG.png")
bg3_image = pygame.transform.scale(bg3_image, display_size)
bg3_rect = bg3_image.get_rect()



# GAME 4 assets

chandu3_image = pygame.image.load("images/chandu3.png")
chandu3_rect = chandu3_image.get_rect()
chandu3_rect.center = width//2, height//2

chandu_holder_image = pygame.image.load("images/chandu_holder.png")
chandu_holder_rect = chandu_holder_image.get_rect()
chandu_holder_rect.left = chandu3_rect.right-190
chandu_holder_rect.centery = chandu3_rect.centery

bg4_image = pygame.image.load("images/moonback.png")
bg4_image = pygame.transform.scale(bg4_image, display_size)
bg4_rect = bg3_image.get_rect()

moon_offset = 0





separation = False

#GAME5 ASSESTS

#images
bg6 = pygame.image.load("images/bg6.png")

non_r_lannder = pygame.image.load("images/non_r_lander.png")
non_r_lannder = pygame.transform.scale(non_r_lannder,(200,200))
non_r_lannder_rect = non_r_lannder.get_rect()





r_lander = pygame.transform.rotate(non_r_lannder, 90)
r_lander_rect = r_lander.get_rect()
r_lander_rect.topleft = 0,-100

r_lander2 = pygame.transform.rotate(non_r_lannder, 60)
r_lander2 = pygame.transform.scale(r_lander2,(250,250))
r_lander2_rect = r_lander2.get_rect()
r_lander2_rect.topleft = 400,-100









#GAME6 assets

#images
moonland_image = pygame.image.load("images/moonland.png")
moonland_image = pygame.transform.scale(moonland_image, (display_size))
moonland_rect = moonland_image.get_rect()
moonland_rect.bottomleft = 0,height

lander_image = pygame.image.load("images/lander.png")
lander_image = pygame.transform.scale(lander_image,(600,400))
lander_rect = lander_image.get_rect()
lander_rect.bottomleft = 0, 0

deck_image = pygame.image.load("images/deck.png")
deck_image = pygame.transform.scale(deck_image,(200,150))
deck_rect = deck_image.get_rect()
deck_rect.topleft = 300, 600



fine_bracking = False
rough_bracking = False
landing = False
horizontal_velocity_lander = 5
vertical_velocity_lander = 5





# Pymunk setup
space = pymunk.Space()
space.gravity = 0, -800  # Adjust gravity to match the scaling

def convert_coord(point): #pygame to pymunk coord
    return point[0], height - point[1]






class Rover:
    def __init__(self, x=255, y=600, width=60, height=30):
        self.body = pymunk.Body(1, 1666)
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.body.position = (x, y)
        space.add(self.body, self.shape)
        self.shape.friction = 1
        self.shape.density = 1
        self.car_image = pygame.image.load("images/rover.png")
        self.car_image = pygame.transform.scale(self.car_image,(60,60))
        self.car_rect = self.car_image.get_rect()
        self.car_rect.center = x,y

    def draw(self, screen):
        vertices = [v.rotated(self.body.angle) + self.body.position for v in self.shape.get_vertices()]
        pygame_vertices = [(v.x, height - v.y) for v in vertices]
        
        # Draw the car image
        rotated_car = pygame.transform.rotate(self.car_image, self.body.angle * 180 / math.pi)
        car_rect = rotated_car.get_rect(center=(self.body.position.x, height - self.body.position.y))
        screen.blit(rotated_car, car_rect.topleft)

    def reset_game(self, x=255, y= height-500):
        self.body.position = (x, y)
        self.body.velocity = (0, 0)

class Floor:
    def __init__(self, start_coord, end_coord, thickness=8):
        self.start_coord = start_coord
        self.end_coord = end_coord
        self.thickness = thickness
        self.start_pymunk = convert_coord(start_coord)
        self.end_pymunk = convert_coord(end_coord)
        self.segment_shape = pymunk.Segment(space.static_body, self.start_pymunk, self.end_pymunk, self.thickness)
        self.segment_shape.elasticity = 1
        self.segment_shape.density = 500
        self.segment_shape.friction = 1
        space.add(self.segment_shape)  # Add to space here

    def draw(self, screen):
        #pygame.draw.line(screen, (255, 255, 255), self.start_coord, self.end_coord, self.thickness)
        pass

car = Rover()

floors = [Floor((0, 740), (200, 740), 10),
Floor((200, 740), (400, 740),10),
Floor((400, 740), (600, 750), 10),
Floor((600, 750), (800, 710), 10),
Floor((800, 710), (1000, 660), 10),
Floor((1000, 660), (1200, 660), 10),
Floor((1200, 660), (width, 640), 10),
Floor((150,600),(290,600),20),
Floor((290,600),(500,750),20)
] 


move_car_right = False
move_car_left = False
rover = False
fall = False
fall_speed = 5
drop_deck = False
# Game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if current_state == MAIN_MENU:
                if event.key == pygame.K_1:
                    reset_game()
                    current_state = GAME1
             
                elif event.key == pygame.K_2:
                    reset_game()
                    current_state = GAME2

                elif event.key == pygame.K_3:
                    reset_game()
                    current_state = GAME3
                elif event.key == pygame.K_4:
                    reset_game()
                    current_state = GAME4

                elif event.key == pygame.K_5:
                    reset_game()
                    current_state = GAME5
                elif event.key == pygame.K_6:
                    reset_game()
                    current_state = GAME6
            elif current_state == GAME1:

                if event.key == pygame.K_ESCAPE:
                    reset_game()
                    current_state = MAIN_MENU
                elif event.key == pygame.K_SPACE:
                    ignition1_index = (ignition1_index + 1) % len(ignition1_images)
                    show_ignition1 = True
                    rocket_rect.centery -= velocity

            elif current_state == GAME2:
                if event.key == pygame.K_ESCAPE:

                    reset_game()
                    current_state = MAIN_MENU
                elif not boosters_active and not body_active and not mouth_active and not c_body_active:
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        boosters_active = True
                elif boosters_active and not mouth_active and not body_active and not c_body_active:
                    if event.key == pygame.K_SPACE:
                        mouth_active = True
                elif boosters_active and not body_active and mouth_active and not c_body_active:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        body_active = True
                elif boosters_active and body_active and mouth_active and not c_body_active:
                    if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                        c_body_active = True
                elif boosters_active and body_active and mouth_active and c_body_active:
                    if event.key == pygame.K_UP:
                        spray = True
            elif current_state == GAME3:
                if event.key == pygame.K_ESCAPE:
                    reset_game()
                    current_state = MAIN_MENU
                
                if event.key == pygame.K_RIGHT:
                    moving_right = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        moving_right = False
            elif current_state == GAME4:
                if event.key == pygame.K_ESCAPE:
                    reset_game()
                    current_state = MAIN_MENU
                
                if event.key == pygame.K_SPACE:
                    separation = True

            
            elif current_state == GAME5:
                if event.key == pygame.K_ESCAPE:
                    reset_game()
                    current_state = MAIN_MENU

                if event.key == pygame.K_r:
                    rough_bracking = True

            elif current_state == GAME6:
                if event.key == pygame.K_ESCAPE:
                    reset_game()
                    current_state = MAIN_MENU
                if event.key == pygame.K_r:
                    car.reset_game()
                if event.key == pygame.K_RIGHT:
                    move_car_right = True
                if event.key == pygame.K_LEFT:
                    move_car_left = True

                if event.key == pygame.K_DOWN and lander_rect.centery <= height -340 :
                    fall = True

                if event.key == pygame.K_d and lander_rect.centery >= height -340:
                    drop_deck = True

        elif event.type == pygame.KEYUP and current_state == GAME6:
                    if event.key == pygame.K_RIGHT:
                        move_car_right = False
                    if event.key == pygame.K_LEFT:
                        move_car_left = False

                


               

    # Clear the Pygame window
    display_surface.fill((0, 0, 0))

    # Main menu
    # Main menu
    if current_state == MAIN_MENU:


        # Reset launched state

        game_name = "Chandrayaan-3"
        game_name_text = font2.render(game_name, True, font_color)
        game_name_rect = game_name_text.get_rect()
        game_name_rect.center = (width // 2, height // 2-200)

        display_surface.fill((0,0,0))

        display_surface.blit(game_name_text, game_name_rect)

    

        main_menu_texts_with_restart = ["LEVEL 1 - PRESS 1", "LEVEL 2 - PRESS 2", "LEVEL 3 - PRESS 3", "LEVEL 4 - PRESS 4", "LEVEL 5 - Press 5", "LEVEL 6 - Press 6" ]
        main_menu_positions_with_restart = [(width // 2, height // 2 - 50), (width // 2, height // 2), (width // 2, height // 2 + 50), (width // 2, height // 2 + 100), (width // 2, height // 2 + 150), (width // 2, height // 2 + 200)]

        for text, position in zip(main_menu_texts_with_restart, main_menu_positions_with_restart):
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=position)
            display_surface.blit(text_surface, text_rect)

      


    # Game 1
    elif current_state == GAME1:

        display_surface.fill((255, 255, 255))

        display_surface.blit(bg1_image,bg1_rect)

        # TICK THE CLOCK
        clock.tick(FPS)

       

        # Gravity effect
        if rocket_rect.bottom < height - 170:
            rocket_rect.centery += gravity

        # Update the bar fill height based on the rocket's ascent progress
        ascent_progress = 1 - (ignition1_rect.bottom - 115) / (height - 170)
        if rocket_rect.bottom == height - 170:  # Rocket at starting position
            bar_fill_height = 0
        else:
            bar_fill_height = int(ascent_progress * bar_height)
        bar_fill_rect.height = bar_fill_height
        bar_fill_rect.y = bar_rect.y + bar_height - bar_fill_height


        press3_name = "Press SPACE several times to launch"
        press3_name_text = font.render(press3_name, True, font_color, (0,0,0))
        press3_name_rect = press3_name_text.get_rect()
        press3_name_rect.center = (width // 2, (height-50))
        display_surface.blit(press3_name_text, press3_name_rect)


        # Blit the launchpad
        display_surface.blit(launchpad_image, launchpad_rect)

        # Draw the bar
        pygame.draw.rect(display_surface, (0, 0, 0), bar_rect)
        pygame.draw.rect(display_surface, bar_color, bar_fill_rect)

        display_surface.blit(press3_name_text, press3_name_rect)

        # Ignition effect
        if show_ignition1:
            ignition1_rect.centerx = rocket_rect.centerx  # Align horizontally with rocket_rect
            ignition1_rect.top = rocket_rect.bottom  # Align top of ignition_rect with bottom of rocket_rect
            display_surface.blit(ignition1_images[ignition1_index], ignition1_rect)
            ignition1_delay -= 1
            if ignition1_delay <= 0:
                show_ignition1 = False
                ignition1_delay = 60

        if ignition1_rect.centery+50 < 0:
               current_state = GAME2

        
            
        



        # Blit the rocket
        display_surface.blit(rocket_image, rocket_rect)

  


    # Game 2
    elif current_state == GAME2:

        show_ignition= True

       
        # Clear the Pygame window
        display_surface.fill((255, 255, 255))

        display_surface.blit(bg2_image,bg2_rect)

        # TICK THE CLOCK
        clock.tick(FPS)

        # Ignition effect animation
        if show_ignition:
            rotated_ignition = pygame.transform.rotate(ignition_images[ignition_index], -70)
            rotated_ignition_rect = rotated_ignition.get_rect(center=ignition_rect.center)
            rotated_ignition_rect.center = ignition_rect.center
            display_surface.blit(rotated_ignition, rotated_ignition_rect)
            ignition_delay -= 1
            if ignition_delay <= 0:
                ignition_index = (ignition_index + 1) % len(ignition_images)
                ignition_delay = 10

        # Blit the images
        display_surface.blit(fly2_image, fly2_rect)
        display_surface.blit(chandu_image, chandu_rect)
        display_surface.blit(mouth_image, mouth_rect)
        display_surface.blit(c_body_image, c_body_rect)
        display_surface.blit(body_image, body_rect)
        display_surface.blit(fly1_image, fly1_rect)

        if c_body_active:
            display_surface.blit(c_body_image, c_body_rect)
            c_body_rect.move_ip(-5, 3)

            if c_body_rect.right < -10000:
                c_body_active = False

        if body_active:
            display_surface.blit(body_image, body_rect)
            body_rect.move_ip(-5, 3)
            ignition_rect = ignition_images[0].get_rect()
            ignition_rect.right = body_rect.left + 10
            ignition_rect.bottom = body_rect.bottom + 70

            if body_rect.right < -10000:
                body_active = False

        if boosters_active:
            display_surface.blit(fly2_image, fly2_rect)
            display_surface.blit(fly1_image, fly1_rect)
            fly1_rect.move_ip(-5, 2)
            fly2_rect.move_ip(-5, 2)

            if fly1_rect.right < -10000:
                boosters_active = False

        if mouth_active:
            display_surface.blit(mouth_image, mouth_rect)
            mouth_rect.move_ip(-5, 4)

            if mouth_rect.right < -10000:
                mouth_active = False

        if spray:
            display_surface.blit(chandu_image, chandu_rect)
            chandu_rect.move_ip(5, -4)



        # Display instructions
        active_instructions = []
        if not boosters_active:
            active_instructions.append(instructions["boosters_active"])
        if boosters_active and not mouth_active:
            active_instructions.append(instructions["mouth_active"])
        if boosters_active and mouth_active and not body_active:
            active_instructions.append(instructions["body_active"])
        if boosters_active and body_active and mouth_active and not c_body_active:
            active_instructions.append(instructions["c_body_active"])
        if boosters_active and body_active and mouth_active and c_body_active:
            active_instructions.append(instructions["Escape orbit"])

        instruction_y = 20
        for instruction in active_instructions:
            text = font.render(instruction, True, (255, 255, 255), (0, 0, 0))
            text_rect = text.get_rect(center=(width // 2, (height - 50) - instruction_y))
            display_surface.blit(text, text_rect)
            instruction_y += 40

        if chandu_rect.left >= width:
            current_state= GAME3
    # Game 3
    elif current_state == GAME3:

        
        # Control the frame rate
        delta_time = clock.tick(FPS) / 1000.0

        # Clear the screen
        display_surface.fill((0, 0, 0))

        display_surface.blit(bg3_image, bg3_rect)

        # Draw Earth at the center of the screen
        display_surface.blit(earth_image, (170, 200))

        # Draw Moon at the center of the screen
        display_surface.blit(moon_image, (1151, 310))

        press4_name = "Keep Pressing Right > for orbit Rotation"
        press4_name_text = font.render(press4_name, True, font_color, (0, 0, 0))
        press4_name_rect = press4_name_text.get_rect()
        press4_name_rect.center = (width // 2, (height - 50))
        display_surface.blit(press4_name_text, press4_name_rect)

 

        # Calculate the object's position along the SVG path
        if moving_right:
            time += delta_time * 0.09 # Adjust the speed of movement

        # Wrap the time parameter within the range [0, 1]
        time %= 1

        # Draw the object at its position on the screen
        point = svg_path.point(time)
        object_x = int(point.real)
        object_y = int(point.imag)
        chandu2_image = pygame.image.load("images/chandu.png")
        chandu2_image = pygame.transform.scale(chandu_image, (int(chandu_image.get_width() * 0.6), int(chandu_image.get_height() * 0.6)))

        chandu2_rect = chandu_image.get_rect()
        chandu2_rect = pygame.Rect(object_x-30, object_y-30, chandu_image.get_width() * 0.6, chandu_image.get_height() * 0.6)

        display_surface.blit(chandu2_image, chandu2_rect)


        # Store the point in the path_points deque
        path_points.append((object_x, object_y))

    
        

        # Get the center position of the screen
        center_x = width // 2
        center_y = height // 2
        pygame.draw.rect(display_surface, (0, 0, 255), (width-100,0, 300, 50))

        # Print the coordinates
        font = pygame.font.Font(None, 36)
        text = f"Coordinates: ({object_x}, {object_y})"
        text_surface = font.render(text, True, (0, 0, 0))
        display_surface.blit(text_surface, (10, 10))

        if moon_image_rect.colliderect(chandu2_rect):
            current_state = GAME4

        # Update the display
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    reset_game()
                    current_state = MAIN_MENU
                elif event.key == pygame.K_RIGHT:
                    
                    moving_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    moving_right = False

    #game4 

    elif current_state == GAME4:

        moon_offset += 10  # Adjust the sliding speed

        if moon_offset >= bg4_rect.width:
            moon_offset = 0

        # Clear the display
        display_surface.fill((0, 0, 0))

        # Blit the background with the updated offsets
        display_surface.blit(bg4_image, (moon_offset, 0))
        display_surface.blit(bg4_image, (moon_offset - bg4_rect.width, 0))  # Second instance

        # Blit the foreground elements
        display_surface.blit(chandu_holder_image, chandu_holder_rect)
        display_surface.blit(chandu3_image, chandu3_rect)

     

  

        if separation:
            chandu3_rect.move_ip(-5, 0)
            chandu_holder_rect.move_ip(-2,0)

        if chandu3_rect.centerx <= -500:
            current_state = GAME5
            

        
        press5_name = "Press SPACE for separation"
        press5_name_text = font.render(press5_name, True, font_color, (0,0,0))
        press5_name_rect = press5_name_text.get_rect()
        press5_name_rect.center = (width // 2, (height-50))
        display_surface.blit(press5_name_text, press5_name_rect)



        # Update the display
        pygame.display.update()

        # TICK THE CLOCK
        clock.tick(FPS)

    #GAME5 


    elif current_state == GAME5:

        
        display_surface.fill((0,0,0))
        display_surface.blit(bg6, (0,0))

        non_r_lannder_rect = non_r_lannder.get_rect()
        non_r_lannder_rect.center = r_lander2_rect.center

        if rough_bracking:
            r_lander_rect.x += horizontal_velocity_lander
            display_surface.blit(r_lander, r_lander_rect)
            if r_lander_rect.centerx >= 400:
                rough_bracking = False
                fine_bracking = True

        if fine_bracking:
            r_lander2_rect.centerx += horizontal_velocity_lander
            r_lander2_rect.centery += vertical_velocity_lander

            display_surface.blit(r_lander2, r_lander2_rect)


        if r_lander2_rect.centerx >= 1200:
            fine_bracking = False
            landing = True

        if landing:
            
            non_r_lannder_rect.centery += vertical_velocity_lander
            r_lander2_rect.centery += vertical_velocity_lander
            display_surface.blit(non_r_lannder, non_r_lannder_rect)

        if non_r_lannder_rect.bottom >=  height :
            current_state = GAME6

        if not rough_bracking and not landing and  not fine_bracking :
            press7_name = "Press R to Start Rough Bracking Phase"
            press7_name_text = font.render(press7_name, True, font_color, (0,0,0))
            press7_name_rect = press7_name_text.get_rect()
            press7_name_rect.center = (width // 2, (height-50))
            display_surface.blit(press7_name_text, press7_name_rect)


    
        pygame.display.update()


        clock.tick(FPS)

                
    #GAME6

    elif current_state == GAME6:

        


        display_surface.fill((0, 0, 0))
        display_surface.blit(moonland_image, moonland_rect)
        
        
        if fall:
            lander_rect.centery += fall_speed

            if lander_rect.centery >= height -340:
                fall = False

        if drop_deck:
            display_surface.blit(deck_image,deck_rect)
            rover = True



        for floor in floors:
            floor.draw(display_surface)

        if move_car_right and rover:
            car.body.position += (5, 0)
        if move_car_left and rover:
            car.body.position -= (5, 0)

        if rover:
            car.draw(display_surface)

        display_surface.blit(lander_image,lander_rect)

        instructions_game6 = {
        "fall": "Press down arrow for  soft landing",
        "deck": "Press D to open the Doors of lander",
        "rover": "use LEFT & RIGHT Keys to move the Rover ",
       
    }


         # Display instructions
        active_instructions = []
        if not fall and lander_rect.centery <= height -350:
            active_instructions.append(instructions_game6["fall"])
        if lander_rect.centery >= height -350 and not drop_deck:
            active_instructions.append(instructions_game6["deck"])
        if drop_deck :
            active_instructions.append(instructions_game6["rover"])
      

        instruction_y = 20
        for instructions_game6 in active_instructions:
            text = font.render(instructions_game6, True, (255, 255, 255), (0, 0, 0))
            text_rect = text.get_rect(center=(width // 2, (height - 50) - instruction_y))
            display_surface.blit(text, text_rect)
            instruction_y += 40

    space.step(1 / FPS)         
    # Update the display
    pygame.display.update()
    # TICK THE CLOCK
    clock.tick(FPS)
    # Update the display
pygame.display.update()
pygame.quit()

#code by Hariom Tiwari
