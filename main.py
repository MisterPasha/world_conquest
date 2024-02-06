from button import *
import pygame

pygame.init()

# Set display mode
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

clock = pygame.time.Clock()

running = True

center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

screen = pygame.display.set_mode((screen.get_width(), screen.get_height()))
pygame.display.set_caption("World Conquest")

# Load and scale the background image
background_image = pygame.image.load("C:\\Sussex\\Programming\\Software_Eng\\imgs\\background.png").convert_alpha()
flag_image = pygame.image.load("C:\\Sussex\\Programming\\Software_Eng\\imgs\\flag.png")
map_image = pygame.image.load("C:\\Sussex\\Programming\\Software_Eng\\imgs\\map2.jpg")
linen_image = pygame.image.load("C:\\Sussex\\Programming\\Software_Eng\\imgs\\linen.png")
linen_image = pygame.transform.scale(linen_image, (screen.get_width() * 0.55, screen.get_height() * 0.8))
linen_image_rect = linen_image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
flag_image_rect = flag_image.get_rect(center=(screen.get_width() / 2, flag_image.get_height()/2 - 50))
map_image = pygame.transform.scale(map_image, (screen.get_width(), screen.get_height()))


# Game States
EXIT = -1
MAIN_MENU = 0
GAMEPLAY_1 = 1
GAMEPLAY_2 = 2

# Set initial state
game_state = MAIN_MENU

# Set initial numbers of players
players = 0
AI_agents = 0

# Option window to display
option_window = True

# Color sets
BLACK = pygame.Color("black")
WHITE = pygame.Color("white")
main_menu_button_color_hover = (199, 201, 200)
option_menu_button_color_hover = (1, 16, 64)
option_menu_button_color_green = (84, 133, 97)
option_menu_button_color = (245, 247, 246)

# Font sets
font1 = "C:\\Sussex\\Programming\\Software_Eng\\fonts\\norwester.otf"
font2 = "C:\\Sussex\\Programming\\Software_Eng\\fonts\\FFF_Tusj.ttf"


# Function to draw small buttons when choosing players
def get_opt_button_rect(x, y):
    rect_opt_button_width = 50
    rect_opt_button_x = center_x - (linen_image_rect.width / 2) + x
    rect_opt_button_y = center_y - (linen_image_rect.height / 2) + y
    return pygame.Rect(rect_opt_button_x, rect_opt_button_y, rect_opt_button_width, rect_opt_button_width)


# This function creates a list of Button objects. input: Rect shapes, function and constant
def init_opt_buttons(rect_buttons, action, c):
    buttons = []
    for i, button_ in enumerate(rect_buttons):
        buttons.append(Button(button_, option_menu_button_color,
                              option_menu_button_color_hover, str(i+c), 45, lambda i=i: action(i+c)))
    return buttons


def set_players(new_players):
    global players
    players = new_players
    drop_colors(buttons_opt_P, option_menu_button_color_hover, option_menu_button_color)
    for button_ in buttons_opt_P:
        if button_.text == str(new_players):
            button_.change_color(option_menu_button_color_hover)


def set_agents(new_agents):
    global AI_agents
    AI_agents = new_agents
    drop_colors(buttons_opt_AI, option_menu_button_color_hover, option_menu_button_color)
    for button_ in buttons_opt_AI:
        if button_.text == str(new_agents):
            button_.change_color(option_menu_button_color_hover)


# Switch States
def switch_state(new_state):
    global game_state
    global option_window
    global players
    global AI_agents
    game_state = new_state
    close_option_window()
    option_window = True
    players = 0
    AI_agents = 0


def close_option_window():
    global option_window
    global players
    global AI_agents
    if (players + AI_agents < 7) & (players + AI_agents > 1):
        option_window = False
    drop_colors(buttons_opt_AI, option_menu_button_color_hover, option_menu_button_color)
    drop_colors(buttons_opt_P, option_menu_button_color_hover, option_menu_button_color)


def draw_text(surface, text, size, color, x, y, font=None,):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_option_menu():
    screen.blit(linen_image, linen_image_rect)
    button_back.check_hover(mouse_pos)
    button_play.check_hover(mouse_pos)
    button_back.create_button(screen, width=3, br=30, text_color=WHITE)
    button_play.create_button(screen, width=3, br=30, text_color=WHITE)
    for button_ in buttons_opt_P:
        button_.check_hover(mouse_pos)
    for button_ in buttons_opt_AI:
        button_.check_hover(mouse_pos)
    for button_ in buttons_opt_P:
        button_.create_button(screen, width=3, br=30, text_color=WHITE)
    for button_ in buttons_opt_AI:
        button_.create_button(screen, width=3, br=30, text_color=WHITE)
    # Draw texts
    draw_text(screen, "Before you Begin", 50, WHITE, center_x, center_y - (linen_image_rect.height / 2) + 30,
              font=font2)
    draw_text(screen, "Choose Players", 35, WHITE, center_x - (linen_image_rect.width / 2) + 170,
              center_y - (linen_image_rect.height / 2) + 140, font=font1)
    draw_text(screen, "Choose AI Players", 35, WHITE, center_x - (linen_image_rect.width / 2) + 190,
              center_y - (linen_image_rect.height / 2) + 300, font=font1)


def draw_main_menu():
    # Draw flag
    screen.blit(flag_image, flag_image_rect)
    # Draw text
    draw_text(screen, "World", 60, BLACK, center_x, center_y - 320, font=font2)
    draw_text(screen, "Conquest", 60, BLACK, center_x, center_y - 250, font=font2)
    # Draw Buttons
    button_fullGameMode.check_hover(mouse_pos)
    button_capitalMode.check_hover(mouse_pos)
    button_quit.check_hover(mouse_pos)
    button_fullGameMode.create_button(screen, width=3, br=50)
    button_capitalMode.create_button(screen, width=3, br=50)
    button_quit.create_button(screen, width=3, br=50)


# Main menu Button Rectangles
center_x, center_y = screen.get_width() / 2, screen.get_height() / 2
rect_button_width = 250
rect_button_height = 50
rect_button_x = center_x - rect_button_width / 2
rect_button_y_fullGameMode = center_y - 140
rect_button_y_capitalMode = center_y - 70
rect_button_y_quit = center_y
rect_button_fullGameMode = pygame.Rect(rect_button_x, rect_button_y_fullGameMode,
                                       rect_button_width, rect_button_height)
rect_button_capitalMode = pygame.Rect(rect_button_x + 25, rect_button_y_capitalMode,
                                      rect_button_width - 50, rect_button_height)
rect_button_quit = pygame.Rect(rect_button_x + 50, rect_button_y_quit,
                               rect_button_width - 100, rect_button_height)

# Main menu Button Initialisation
button_fullGameMode = Button(rect_button_fullGameMode, option_menu_button_color,
                             main_menu_button_color_hover, "World Domination", 25, lambda: switch_state(GAMEPLAY_1),
                             font=font1)
button_capitalMode = Button(rect_button_capitalMode, option_menu_button_color,
                            main_menu_button_color_hover, "Capital Mode", 25, lambda: switch_state(GAMEPLAY_2),
                            font=font1)
button_quit = Button(rect_button_quit, option_menu_button_color,
                     main_menu_button_color_hover, "Quit", 25, lambda: switch_state(EXIT),
                     font=font1)

# Option Menu Button Rectangles
rect_button_width_back = 175
rect_button_height_back = 60
rect_button_x_back = center_x - (linen_image_rect.width / 2) + 60
rect_button_y_back = center_y + (linen_image_rect.height / 2) - rect_button_height_back - 70
rect_button_back = pygame.Rect(rect_button_x_back, rect_button_y_back,
                               rect_button_width_back, rect_button_height_back)
rect_button_x_play = center_x + (linen_image_rect.width / 2) - rect_button_width_back - 60
rect_button_play = pygame.Rect(rect_button_x_play, rect_button_y_back,          # Uses same coordinates and size
                               rect_button_width_back, rect_button_height_back)  # as button back, except x


rect_opt_buttons_P = [get_opt_button_rect(i + 60, 200) for i in range(0, 600, 100)]
rect_opt_buttons_AI = [get_opt_button_rect(i + 60, 360) for i in range(0, 600, 100)]

# Option Menu Button Initialisation
button_back = Button(rect_button_back, option_menu_button_color,
                     option_menu_button_color_hover, "Back", 30, lambda: switch_state(MAIN_MENU),
                     font=font1)
button_play = Button(rect_button_play, option_menu_button_color,
                     option_menu_button_color_green, "Play", 30, lambda: close_option_window(),
                     font=font1)

buttons_opt_P = init_opt_buttons(rect_opt_buttons_P, set_players, 1)
buttons_opt_AI = init_opt_buttons(rect_opt_buttons_AI, set_agents, 0)


while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Update the screen size when the window is resized
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == MAIN_MENU:
                button_fullGameMode.check_click(mouse_pos)
                button_capitalMode.check_click(mouse_pos)
                button_quit.check_click(mouse_pos)
            elif game_state == GAMEPLAY_1:
                button_back.check_click(mouse_pos)
                button_play.check_click(mouse_pos)
                for button in buttons_opt_P:
                    button.check_click(mouse_pos)
                for button in buttons_opt_AI:
                    button.check_click(mouse_pos)
            elif game_state == GAMEPLAY_2:
                button_back.check_click(mouse_pos)
                button_play.check_click(mouse_pos)
                for button in buttons_opt_P:
                    button.check_click(mouse_pos)
                for button in buttons_opt_AI:
                    button.check_click(mouse_pos)

    # RENDER GAME HERE #####

    if game_state == MAIN_MENU:
        screen.blit(background_image, (0, 0))  # Set Background image
        draw_main_menu()                       # Draw main menu
    elif game_state == GAMEPLAY_1:
        if option_window:
            draw_option_menu()                 # Draw option menu
        else:
            screen.blit(map_image, (0, 0))
        button_back.check_hover(mouse_pos)
        button_back.create_button(screen, br=30, width=3, text_color=WHITE)
    elif game_state == GAMEPLAY_2:
        if option_window:
            draw_option_menu()
        else:
            screen.blit(map_image, (0, 0))
        button_back.check_hover(mouse_pos)
        button_back.create_button(screen, br=30, width=3, text_color=WHITE)
    elif game_state == EXIT:
        running = False


    pygame.display.flip()

    clock.tick(60)

pygame.quit()
