import tkinter

import pygame
from pygame.time import Clock

import Bot
import Front_End
import Puzzle

pygame.init()
pygame.font.init()
root = tkinter.Tk()
root.update_idletasks()
root.attributes('-fullscreen', True)
root.state('iconic')
screen_size = screen_width, screen_height = (root.winfo_width(), root.winfo_height())

background_color = (50, 50, 50)
game_font = pygame.font.SysFont("Comic Sans MS", 30)
window = pygame.display.set_mode(screen_size)
pygame.display.set_caption('SLIDING PUZZLE')
clock = Clock()
# light shade of the button
color_light = (170, 170, 170)
# dark shade of the button
color_dark = (100, 100, 100)

image_width = screen_width / 2
image_height = screen_height / 2
puzzle = None
p = None

w = a = s = d = False
color_white = (255, 255, 255)
small_font = pygame.font.SysFont('Corbel', 35)
fps = 60

# rendering a text written in
# this font
after_image_coordinates = (
    (screen_width / 2 - image_width / 2) + image_width, (screen_height / 2 - image_height / 2) + (image_height - 40))
scramble_button_text = small_font.render('SCRAMBLE', True, color_white)
scramble_button_attributes = [after_image_coordinates[0] + 80, after_image_coordinates[1] - 180, 200, 40]
get_solution_button_text = small_font.render('SOLUTION', True, color_white)
get_solution_button_attributes = [after_image_coordinates[0] + 80, after_image_coordinates[1] - 120, 200, 40]
solve_button_text = small_font.render('SOLVE', True, color_white)
solve_button_attributes = [after_image_coordinates[0] + 80, after_image_coordinates[1] - 60, 200, 40]
quit_button_text = small_font.render('QUIT', True, color_white)
quit_button_attributes = [after_image_coordinates[0] + 80, after_image_coordinates[1], 200, 40]

running = True

user_text = ''

# create rectangle
input_rect = pygame.Rect(screen_width/2, screen_height/2, 140, 32)

# color_active stores color(lightskyblue3) which
# gets active when input box is clicked by user
color_active = pygame.Color('lightskyblue3')

# color_passive store color(chartreuse4) which is
# color of input box.
color_passive = pygame.Color('chartreuse4')
color = color_passive

base_font = pygame.font.Font(None, 32)

active = False


def handle_mouse(mouse_position, pzle):
    global running
    global puzzle
    if scramble_button_attributes[0] <= mouse_position[0] <= scramble_button_attributes[0] + scramble_button_attributes[
        2] and scramble_button_attributes[1] <= mouse_position[1] <= scramble_button_attributes[1] + \
            scramble_button_attributes[3]:
        pzle.move_list = puzzle.scramble()
        pzle.revealing = False
        pzle.scrambling = True
    elif get_solution_button_attributes[0] <= mouse_position[0] <= get_solution_button_attributes[0] + \
            get_solution_button_attributes[2] and get_solution_button_attributes[1] <= mouse_position[1] <= \
            get_solution_button_attributes[1] + get_solution_button_attributes[3]:
        pass
    elif solve_button_attributes[0] <= mouse_position[0] <= solve_button_attributes[0] + solve_button_attributes[2] and \
            solve_button_attributes[1] <= mouse_position[1] <= solve_button_attributes[1] + solve_button_attributes[3]:
        pzle.move_list, puzzle = Bot.Bot(puzzle).solve()
        pzle.solve = True
    elif quit_button_attributes[0] <= mouse_position[0] <= quit_button_attributes[0] + quit_button_attributes[2] and \
            quit_button_attributes[1] <= mouse_position[1] <= quit_button_attributes[1] + quit_button_attributes[3]:
        running = False


def handle_hover(mouse_position):
    if scramble_button_attributes[0] <= mouse_position[0] <= scramble_button_attributes[0] + scramble_button_attributes[
        2] and scramble_button_attributes[1] <= mouse_position[1] <= scramble_button_attributes[1] + \
            scramble_button_attributes[3]:
        pygame.draw.rect(window, color_light, scramble_button_attributes)
    else:
        pygame.draw.rect(window, color_dark, scramble_button_attributes)
    if get_solution_button_attributes[0] <= mouse_position[0] <= get_solution_button_attributes[0] + \
            get_solution_button_attributes[2] and get_solution_button_attributes[1] <= mouse_position[1] <= \
            get_solution_button_attributes[1] + get_solution_button_attributes[3]:
        pygame.draw.rect(window, color_light, get_solution_button_attributes)
    else:
        pygame.draw.rect(window, color_dark, get_solution_button_attributes)
    if solve_button_attributes[0] <= mouse_position[0] <= solve_button_attributes[0] + solve_button_attributes[2] and \
            solve_button_attributes[1] <= mouse_position[1] <= solve_button_attributes[1] + solve_button_attributes[3]:
        pygame.draw.rect(window, color_light, solve_button_attributes)
    else:
        pygame.draw.rect(window, color_dark, solve_button_attributes)
    if quit_button_attributes[0] <= mouse_position[0] <= quit_button_attributes[0] + quit_button_attributes[2] and \
            quit_button_attributes[1] <= mouse_position[1] <= quit_button_attributes[1] + quit_button_attributes[3]:
        pygame.draw.rect(window, color_light, quit_button_attributes)
    else:
        pygame.draw.rect(window, color_dark, quit_button_attributes)


def add_text_to_buttons():
    window.blit(scramble_button_text, (scramble_button_attributes[0] + 5, scramble_button_attributes[1] + 5))
    window.blit(get_solution_button_text,
                (get_solution_button_attributes[0] + 5, get_solution_button_attributes[1] + 5))
    window.blit(solve_button_text, (solve_button_attributes[0] + 5, solve_button_attributes[1] + 5))
    window.blit(quit_button_text, (quit_button_attributes[0] + 5, quit_button_attributes[1] + 5))


def menu():
    global user_text, active, color, running, show_menu
    for event in pygame.event.get():

        # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                if str.isdigit(user_text):
                    game_setup(abs(int(user_text) % 20))
                    show_menu = False
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:

                # get text input from 0 to -1 i.e. end.
                user_text = user_text[:-1]

            # Unicode standard is used for string
            # formation
            else:
                user_text += event.unicode

    # it will set background color of screen
    window.fill(background_color)

    if active:
        color = color_active
    else:
        color = color_passive

    # draw rectangle and argument passed which should
    # be on screen
    pygame.draw.rect(window, color, input_rect)

    text_surface = base_font.render(user_text, True, (255, 255, 255))

    # render at position stated in arguments
    window.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    window.blit(small_font.render("PUZZLE SIZE : ", True, (0, 0, 0)), (((screen_width/2)-220), screen_height/2))
    window.blit(small_font.render("(PRESS ENTER)", True, (0, 0, 0)), (((screen_width/2)-220), (screen_height/2)+40))

    # set width of textfield so that text cannot get
    # outside of user's text input
    input_rect.w = max(100, text_surface.get_width() + 10)

    # display.flip() will update only a portion of the
    # screen to updated, not full area
    pygame.display.flip()


def game_setup(size_value):
    global puzzle, p
    puzzle = Puzzle.Puzzle(size_value, [[0 for _ in range(size_value)] for _ in range(size_value)],
                           [size_value - 1, size_value - 1])
    puzzle.populate()
    p = Front_End.GUI("image.jpg", (image_width, image_height), (size_value, size_value),
                      (screen_width / 2 - image_width / 2, screen_height / 2 - image_height / 2))


def game():
    global running
    mouse_position = pygame.mouse.get_pos()
    window.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # checks if a mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse(mouse_position, p)

    # if mouse is hovered on a button it
    # changes to lighter shade
    handle_hover(mouse_position)
    add_text_to_buttons()

    p.update()
    p.render(window)
    if p.is_solved():
        p.reveal(window)

    pygame.display.update()


show_menu = True

while running:
    clock.tick(fps)
    if show_menu:
        menu()
    else:
        game()
