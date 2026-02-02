from tkinter.constants import CENTER
from db import save_game
import pygame
import random

# Inicializace hry
pygame.init()

# Nastavení obrazovky
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("CLICK IT GAME")

# Nastavení hry
hodiny = pygame.time.Clock()
fps = 60
running = True

# Barvy
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
gray = (100, 100, 100)

# Fonty
title_font = pygame.font.SysFont("arialblack", 60)
menu_font = pygame.font.SysFont("arialblack", 40)
small_font = pygame.font.SysFont("arialblack", 25)

# Text titulku
title_text = title_font.render("CLICK IT!", True, white)
title_rect = title_text.get_rect(center=(width//2, 80))

#Hudba v pozadí
pygame.mixer.music.load("song_pozadi.wav")
# Změna hlasitosti
pygame.mixer.music.set_volume(0.3)




# Rozložení hry
UVODNI_MENU = 1
HLAVNI_MENU = 2
HRA = 3
GAME_OVER = 4

stav_hry =  UVODNI_MENU

# Proměnné
cas_start = None
odpocet_cas = 30
audio_zapnute = True #proměnná na klik tlačítka audio
targets = []
target_size = 30
score = 0
game_over_delay = None
jmeno_hrace = ""
psani_jmena = True
max_delka_jmena = 20
score_odeslano = False
mode_30s = 30
mode_2min = 120
vybrany_cas = mode_30s  # default
vybrany_mode_id = 1 #30s

# Funkce pro kreslení tlačítek
def draw_button(text,x, y, color):
    button_text = menu_font.render(text, True, color)
    button_rect = button_text.get_rect(center=(x, y))
    screen.blit(button_text, button_rect)
    return button_rect


def uvodni_menu():
    global running, stav_hry
    screen.fill(black)
    screen.blit(title_text, title_rect)

    space_text = small_font.render("Press SPACE to load the game", True, white)
    space_rect = space_text.get_rect(center=(width // 2, height // 2))
    screen.blit(space_text, space_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Stisk mezerníku
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                stav_hry = HLAVNI_MENU

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

def hlavni_menu():
    global running, stav_hry, audio_zapnute, jmeno_hrace, psani_jmena, max_delka_jmena, vybrany_cas, odpocet_cas, cas_start, vybrany_mode_id
    screen.fill(black)
    screen.blit(title_text, title_rect)

    jmeno_text = small_font.render("Enter name:", True, white)
    jmeno_rect = jmeno_text.get_rect(center=(width // 2, 140))
    screen.blit(jmeno_text, jmeno_rect)

    barva_30 = white if vybrany_cas == mode_30s else gray
    barva_120 = white if vybrany_cas == mode_2min else gray
    barva_audio = white if audio_zapnute == True else gray

    #input box
    box_width = 420
    box_height = 42
    box_rect = pygame.Rect(0, 0, box_width, box_height )
    box_rect.center = (width // 2, 190)
    pygame.draw.rect(screen, gray, box_rect, 2)

    if jmeno_hrace != "":
        input_surface = small_font.render(jmeno_hrace, True, white)
        # zarovnání textu do boxu (vlevo, s odsazením)
        input_rect = input_surface.get_rect(center=box_rect.center)
        screen.blit(input_surface, input_rect)

    mode30_button = draw_button("30s", width // 2 - 150, 240, barva_30)
    mode2min_button = draw_button("2min", width // 2 + 150, 240, barva_120)

    start_button = draw_button("Start", width // 2, 280, white)
    audio_button = draw_button("Audio", width // 2, 340, barva_audio)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # Kliknutí myší na tlačítka
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if box_rect.collidepoint(mouse_pos):
                psani_jmena = True
            else:
                psani_jmena = False

            if mode30_button.collidepoint(mouse_pos):
                vybrany_cas = mode_30s
                vybrany_mode_id = 1

            if mode2min_button.collidepoint(mouse_pos):
                vybrany_cas = mode_2min
                vybrany_mode_id = 2

            elif start_button.collidepoint(mouse_pos):
                if jmeno_hrace != "":
                    odpocet_cas = vybrany_cas
                    cas_start = None
                    stav_hry = HRA

            elif audio_button.collidepoint(mouse_pos):
                audio()

        if event.type == pygame.KEYDOWN and psani_jmena:
            if event.key == pygame.K_BACKSPACE:
                jmeno_hrace = jmeno_hrace[:-1]

            else:
                znak = event.unicode

                # přidávej jen pokud:
                # - znak není prázdný
                # - nepřekročíš max délku 20
                # - je to písmeno/číslo/mezera/_
                if znak != "" and len(jmeno_hrace) < max_delka_jmena:
                    if znak.isalnum() or znak in (" ", "_"):
                        jmeno_hrace += znak
def hra():
    global running, stav_hry, cas_start, targets, score, game_over_delay, target_size, score_odeslano

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # kliknutí myší
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # jestli existuje target a jestli jsem do nej kliknul
            for objekt in targets:
                if objekt.collidepoint(mouse_pos):
                    score += 1
                    if score in (15, 25, 35) and target_size > 15:
                        target_size -= 5

                    if score in (15, 25, 35):
                        x_new = random.randint(0, width - target_size)
                        y_new = random.randint(60, height - target_size)
                        targets.append(pygame.Rect(x_new, y_new, target_size, target_size))

                    x = random.randint(0, width - target_size)
                    y = random.randint(60, height - target_size)
                    objekt.update(x, y, target_size, target_size)

    #vytvoření prvního targetu když není ještě vytvořený
    if len(targets) == 0:
        x = random.randint(0, width - target_size)
        y = random.randint(60, height - target_size)
        targets.append(pygame.Rect(x, y, target_size, target_size))

    # start odpočtu
    if cas_start is None:
        cas_start = pygame.time.get_ticks()

    ubehly_cas = (pygame.time.get_ticks() - cas_start) / 1000
    zbyvajici_cas = max(0, odpocet_cas - int(ubehly_cas))

    # když skonci čas nastane game over
    if zbyvajici_cas == 0:
        stav_hry = GAME_OVER
        game_over_delay = pygame.time.get_ticks()
        score_odeslano = False
        return

    screen.fill(black)

    # čas
    cas_font = pygame.font.SysFont("arialblack", 15)
    cas_text = cas_font.render(f"TIME: {zbyvajici_cas}", True, white)
    screen.blit(cas_text, (10, 30))

    #score
    score_font = pygame.font.SysFont("arialblack", 15)
    score_text = score_font.render(f"SCORE: {score}", True, white)
    screen.blit(score_text, (10, 50))

    #jmeno
    jmeno_font = pygame.font.SysFont("arialblack", 15)
    jmeno_text = jmeno_font.render(f"PLAYER: {jmeno_hrace}", True, white)
    screen.blit(jmeno_text, (10, 10))

    # vykreslení všech targetů
    for objekt in targets:
        pygame.draw.rect(screen, red, objekt)


def game_over():
    global running, stav_hry, cas_start, targets, score, target_size, score_odeslano

    screen.fill(black)

    game_over_text = title_font.render("GAME OVER!", True, white)
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    score_font = pygame.font.SysFont("arialblack", 30)
    score_text = score_font.render(f"SCORE: {score}", True, white)
    score_rect = score_text.get_rect(center=(width // 2, height // 2 + 50))
    screen.blit(score_text, score_rect)

    back_button = draw_button("BACK", width//2, height //2 + 130, white)

    if not score_odeslano:
        save_game(jmeno_hrace, vybrany_mode_id, score)
        score_odeslano = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Kliknutí myši na tlačítko
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if back_button.collidepoint(mouse_pos):
                cas_start = None
                targets = []
                target_size = 30
                score = 0
                stav_hry = HLAVNI_MENU
                return

    if game_over_delay is not None:
        if pygame.time.get_ticks() - game_over_delay >= 4000:
            cas_start = None
            targets = []
            target_size = 30
            score = 0
            stav_hry = HLAVNI_MENU


def audio():
    global audio_zapnute

    audio_zapnute = not audio_zapnute #změna stavu kliknutím na tlacitko

    if audio_zapnute:  #pokud ma byt zvuk zapnuty a nehraje spust ho
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

# Hlavní cyklus hry
while running:
    if stav_hry == UVODNI_MENU:
        uvodni_menu()
    elif stav_hry == HLAVNI_MENU:
        hlavni_menu()
    elif stav_hry == HRA:
        hra()
    elif stav_hry == GAME_OVER:
        game_over()

    # Aktualizace obrazovky
    pygame.display.update()
    hodiny.tick(fps)

# Ukončení hry
pygame.quit()