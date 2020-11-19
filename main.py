from chessboard import *
import pygame
import copy


def chess_board(screen, board, board_pos):
    screen.blit(board, (x_board, y_board))
    for i in range(8):
        for j in range(8):
            if board_pos[i][j] != '--':  # represents
                piece_img = pygame.image.load("Images/Pieces/" + piece_style + "/" + board_pos[i][j] + ".png")
                piece_img = pygame.transform.scale(piece_img, (square_sz-5, square_sz-5))
                screen.blit(piece_img, (x_board + j * square_sz+2.5, y_board + i * square_sz+2.5))
            pass


def flip(white_down, board_pos):
    flip_pieces(board_pos)
    return not white_down


def get_square_pos(tup):
    x = (tup[0] - x_board) // 80
    y = (tup[1] - y_board) // 80
    return y, x


SCREEN_X = int(1100)
SCREEN_Y = int(640)

# Styles
piece_styles = ['Icy Sea', 'Berlin']
board_styles = ['Icy Sea', 'Staunton', 'Bases', 'Blue']
p = 0
b = 0
piece_style = piece_styles[p]
board_style = board_styles[b]

# Board
l_board = int(640)
square_sz = l_board // 8
x_board = ((SCREEN_X - l_board) // 2) + 20
y_board = ((SCREEN_Y - l_board) // 2)


def new_game():
    a = copy.deepcopy(board_position)
    return a


def check_valid_sq(tup):
    if tup[0] < 0 or tup[1] < 0 or tup[0] > 7 or tup[1] > 7:
        return False
    return True


def side_menu(screen):
    new_game_img = pygame.image.load("Images/Main/new_game.png")
    screen.blit(new_game_img, (10, 10))
    flip_img = pygame.image.load("Images/Main/flip.png")
    screen.blit(flip_img, (x_board - 50, SCREEN_Y - 50))
    bnp_img = pygame.image.load("Images/Main/settings.png")
    screen.blit(bnp_img, (x_board - 50, SCREEN_Y - 98))


def settings(screen):
    set_run = True
    global p
    global b
    i_p = int(p)
    i_b = int(b)
    while set_run:
        settings_img = pygame.image.load("Images/Main/settings_page.png")
        screen.blit(settings_img, (x_board, y_board))
        # noinspection SpellCheckingInspection
        font = pygame.font.Font('freesansbold.ttf', 16)
        piece_text = font.render(piece_styles[i_p], True, (0, 0, 0), None)
        text_rect = piece_text.get_rect()
        text_rect.center = (623, 174)
        screen.blit(piece_text, text_rect)
        piece_text = font.render(board_styles[i_b], True, (0, 0, 0), None)
        text_rect = piece_text.get_rect()
        text_rect.center = (623, 236)
        screen.blit(piece_text, text_rect)
        pygame.display.update()
        update = False
        while not update:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if (mouse_pos[0] > x_board + l_board - 40) and (mouse_pos[0] < x_board + l_board - 40 + 33) \
                            and (mouse_pos[1] > y_board + 10) and (mouse_pos[1] < y_board + 10 + 33):
                        global piece_style
                        piece_style = piece_styles[i_p]
                        global board_style
                        board_style = board_styles[i_b]
                        b = i_b
                        p = i_p
                        return True
                    elif (mouse_pos[0] > 457) and (mouse_pos[0] < 469) and (mouse_pos[1] > 166) and\
                            (mouse_pos[1] < 186):
                        i_p -= 1
                        if i_p == -1:
                            i_p = len(piece_styles) - 1
                    elif (mouse_pos[0] > 779) and (mouse_pos[0] < 791) and (mouse_pos[1] > 166) and\
                            (mouse_pos[1] < 186):
                        i_p += 1
                        if i_p == len(piece_styles):
                            i_p = 0
                    elif (mouse_pos[0] > 457) and (mouse_pos[0] < 469) and (mouse_pos[1] > 166+62) and\
                            (mouse_pos[1] < 186+62):
                        i_b -= 1
                        if i_b == -1:
                            i_b = len(board_styles) - 1
                    elif (mouse_pos[0] > 779) and (mouse_pos[0] < 791) and (mouse_pos[1] > 166+62) and\
                            (mouse_pos[1] < 186+62):
                        i_b += 1
                        if i_b == len(board_styles):
                            i_b = 0
                update = True


def main():
    # initialize
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

    # Title and Icon
    pygame.display.set_caption('Chess')
    icon = pygame.image.load("Images/logo.png")
    pygame.display.set_icon(icon)

    white_down = True

    board_pos = new_game()

    # Game loop
    running = True
    while running:
        screen.fill((89, 91, 92))
        side_menu(screen)
        board = pygame.image.load("Images/Boards/" + board_style + ".png")
        board = pygame.transform.scale(board, (l_board, l_board))
        chess_board(screen, board, board_pos)
        pygame.display.update()
        init_square = 0, 0
        update = False
        drag = False

        while not update:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    update = True
                if event.type == pygame.MOUSEBUTTONDOWN and drag:
                    final_square = get_square_pos(pygame.mouse.get_pos())
                    drag = False
                    update = True
                    if not check_valid_sq(final_square) or (board_pos[init_square[0]][init_square[1]]
                                                            == board_pos[final_square[0]][final_square[1]]):
                        break
                    board_pos[final_square[0]][final_square[1]], board_pos[init_square[0]][init_square[1]] = \
                        board_pos[init_square[0]][init_square[1]], '--'

                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if (mouse_pos[0] > x_board - 50) and (mouse_pos[0] < x_board - 50 + 36) \
                            and (mouse_pos[1] > SCREEN_Y - 50) and (mouse_pos[1] < SCREEN_Y - 50 + 33):
                        flip(white_down, board_pos)
                        update = True
                        break
                    if (mouse_pos[0] > x_board - 50) and (mouse_pos[0] < x_board - 50 + 36) \
                            and (mouse_pos[1] > SCREEN_Y - 98) and (mouse_pos[1] < SCREEN_Y - 98 + 36):
                        running = settings(screen)
                        update = True
                    elif (mouse_pos[0] > 10) and (mouse_pos[0] < 10 + 230) \
                            and (mouse_pos[1] > 10) and (mouse_pos[1] < 10 + 39):
                        board_pos = new_game()
                        update = True
                        break
                    init_square = get_square_pos(mouse_pos)
                    if check_valid_sq(init_square) and (board_pos[init_square[0]][init_square[1]] != '--'):
                        drag = True


if __name__ == '__main__':
    main()
