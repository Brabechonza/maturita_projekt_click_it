from db import save_game
import pygame
import random
import os

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
pygame.mixer.music.set_volume(0.3) # nastav hlasitost na 30%

# Rozložení hry
UVODNI_MENU = 1
HLAVNI_MENU = 2
HRA = 3
GAME_OVER = 4
stav_hry =  UVODNI_MENU

SETTINGS_FILE = "audio.txt"  #ukladam bud 1 nebo 0

def load_audio_setting(): #načte audio nastavení ze souboru
    if not os.path.exists(SETTINGS_FILE): #pokud soubor neexistuje (první spuštění)
        return True
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f: #otevři soubor pro čtení
            return f.read().strip() == "1" #1 = True, 0 = False
    except OSError:  #kdyby nesel soubor otevrit
        return True  #radši zapnout aby hra fungovala

def save_audio_setting(is_on: bool):  #uloží audio nastavení do souboru
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f: #otevři soubor pro zápis (přepíše obsah)
            f.write("1" if is_on else "0")  #zapíše jen 1 nebo 0
    except OSError:
        pass   # když zápis selže, hra jede dal

# Proměnné
cas_start = None
odpocet_cas = 30
audio_zapnute = True #výchozí hodnota hned se přepíše tím co je v souboru
audio_zapnute = load_audio_setting() #načíst stav audia z audio.txt
targets = [] # seznam targetů
target_size = 30
score = 0
game_over_delay = None
jmeno_hrace = "" #text z inputu
psani_jmena = True #jestli je aktivní psaní do input boxu
max_delka_jmena = 20
score_odeslano = False #hlídá, aby se score uložilo do DB jen jednou
mode_30s = 30
mode_2min = 120
vybrany_cas = mode_30s  # default
vybrany_mode_id = 1 #30s


# Funkce pro kreslení tlačítek
def draw_button(text,x, y, color): #vykreslí text jako tlačítko
    button_text = menu_font.render(text, True, color) # vykreslený text tlačítka
    button_rect = button_text.get_rect(center=(x, y)) # obdélník tlačítka (kvůli kliknutí)
    screen.blit(button_text, button_rect) # vykresli text na obrazovku
    return button_rect # vrátí rect, tim pozname ze na něj uživatel kliknul


def uvodni_menu():
    global running, stav_hry, audio_zapnute
    screen.fill(black)
    screen.blit(title_text, title_rect) #vykreslí nadpis CLICK IT!

    space_text = small_font.render("Press SPACE to load the game", True, white)
    space_rect = space_text.get_rect(center=(width // 2, height // 2))
    screen.blit(space_text, space_rect)

    for event in pygame.event.get(): #projde všechny události od pygame klik, klavesy a tak
        if event.type == pygame.QUIT: #když uživatel zavře okno
            running = False # ukončí se hlavní smyčka

        # Stisk mezerníku
        if event.type == pygame.KEYDOWN: # stisk klávesy
            if event.key == pygame.K_SPACE: # pokud je to mezerník
                stav_hry = HLAVNI_MENU # přepni do hlavního menu

        #pustí se jen pokud je audio zapnuté
        if audio_zapnute and not pygame.mixer.music.get_busy(): # jestli má hrát hudba a jestli už nehraje
            pygame.mixer.music.play(-1) # -1 = nekonečná smyčka

def hlavni_menu():
    global running, stav_hry, audio_zapnute, jmeno_hrace, psani_jmena, max_delka_jmena, vybrany_cas, odpocet_cas, cas_start, vybrany_mode_id
    screen.fill(black)
    screen.blit(title_text, title_rect)

    jmeno_text = small_font.render("Enter name:", True, white)  # text pro input
    jmeno_rect = jmeno_text.get_rect(center=(width // 2, 140)) # pozice textu
    screen.blit(jmeno_text, jmeno_rect)

    #barvy tlačítek, vybrano bílé, nevybrano šedé)
    barva_30 = white if vybrany_cas == mode_30s else gray
    barva_120 = white if vybrany_cas == mode_2min else gray
    barva_audio = white if audio_zapnute == True else gray

    #input box, jen ten obdelnik
    box_width = 420
    box_height = 42
    box_rect = pygame.Rect(0, 0, box_width, box_height )
    box_rect.center = (width // 2, 190)  # posune do středu
    pygame.draw.rect(screen, gray, box_rect, 2) # vykreslí rámeček input boxu

    # vykreslení jména do input boxu
    if jmeno_hrace != "":  # pokud neni jmeno prazdne
        input_surface = small_font.render(jmeno_hrace, True, white) # render text jména
        input_rect = input_surface.get_rect(center=box_rect.center) # zarovnání textu do boxu (vlevo, s odsazením)
        screen.blit(input_surface, input_rect)

    mode30_button = draw_button("30s", width // 2 - 150, 240, barva_30)
    mode2min_button = draw_button("2min", width // 2 + 150, 240, barva_120)

    start_button = draw_button("Start", width // 2, 280, white)
    audio_button = draw_button("Audio", width // 2, 340, barva_audio)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # ukončení hry

            # Kliknutí myší na tlačítka
        if event.type == pygame.MOUSEBUTTONDOWN: # klik myši
            mouse_pos = pygame.mouse.get_pos() # aktuální pozice myši

            # aktivace psaní jména jen když klikneš do input boxu
            if box_rect.collidepoint(mouse_pos): # pokud klik byl v input bo
                psani_jmena = True # povol psaní
            else:
                psani_jmena = False # jinak vypni psaní

            if mode30_button.collidepoint(mouse_pos):   # klik na 30s
                vybrany_cas = mode_30s
                vybrany_mode_id = 1

            if mode2min_button.collidepoint(mouse_pos): # klik na 2min
                vybrany_cas = mode_2min
                vybrany_mode_id = 2

            elif start_button.collidepoint(mouse_pos): # klik na Start
                if jmeno_hrace != "":  # bez jména nelze spustit hru
                    odpocet_cas = vybrany_cas # nastav délku kola podle vybraného módu
                    cas_start = None
                    stav_hry = HRA

            elif audio_button.collidepoint(mouse_pos):
                audio()  # zavolá funkci, která přepne hudbu + uloží do audio.txt

        if event.type == pygame.KEYDOWN and psani_jmena: # jen pokud je aktivní psaní
            if event.key == pygame.K_BACKSPACE:  # backspace
                jmeno_hrace = jmeno_hrace[:-1]   # smaže poslední znak z řetězce

            else:
                znak = event.unicode  #znak, který uživatel napsal

                # validace vstupu: délka a povolené znaky
                if znak != "" and len(jmeno_hrace) < max_delka_jmena: # nepřekroč 20 znaků a pokud jmeno neni prazdny
                    if znak.isalnum() or znak in (" ", "_"):  # povolíme písmena/čísla/mezera/_
                        jmeno_hrace += znak # přidej znak do jména
def hra():
    global running, stav_hry, cas_start, targets, score, game_over_delay, target_size, score_odeslano

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # kliknutí myší
        if event.type == pygame.MOUSEBUTTONDOWN:   # klik myší
            mouse_pos = pygame.mouse.get_pos() # pozice kliknutí

            # jestli existuje target a jestli jsem do nej kliknul
            for objekt in targets:
                if objekt.collidepoint(mouse_pos): # zásah targetu
                    score += 1 # zvýšení skóre +1
                    if score in (15, 25, 35) and target_size > 15:  # zmenseni targetu pokud target neni mensi nez 15
                        target_size -= 5

                    if score in (15, 25, 35): # přidaní dalšího targetu při 15/25/35
                        x_new = random.randint(0, width - target_size)  # náhodná X pozice
                        y_new = random.randint(60, height - target_size)  # náhodná Y pozice
                        targets.append(pygame.Rect(x_new, y_new, target_size, target_size)) # přidá nový target

                    # Přesun zasaženého targetu na nové místo
                    x = random.randint(0, width - target_size)
                    y = random.randint(60, height - target_size)
                    objekt.update(x, y, target_size, target_size) # update změní pozici i velikost

    #vytvoření prvního targetu když není ještě vytvořený
    if len(targets) == 0:  # když seznam targetů je prázdný, len vrací počet položek v seznamu nebo počet znaků v řetězci.
        x = random.randint(0, width - target_size)
        y = random.randint(60, height - target_size)
        targets.append(pygame.Rect(x, y, target_size, target_size)) # přidá první target

    # start odpočtu (pouze jednou na zacatku kola)
    if cas_start is None: # pokud ještě nebyl nastaven start kola
        cas_start = pygame.time.get_ticks()   # ulož aktuální čas

    #vypocet zbyvajiciho casu
    ubehly_cas = (pygame.time.get_ticks() - cas_start) / 1000
    zbyvajici_cas = max(0, odpocet_cas - int(ubehly_cas)) # zbývající čas (nesmí jít pod 0)

    # když skonci čas nastane game over
    if zbyvajici_cas == 0: # pokud už není čas
        stav_hry = GAME_OVER # přepni stav
        game_over_delay = pygame.time.get_ticks() # uloží čas, kdy nastal game over (použite pro návrat po 4s)
        score_odeslano = False    # připraví ukládání score: v game_over se má uložit zase „jednou“ pro nové kolo
        return

    screen.fill(black)

    # čas
    cas_font = pygame.font.SysFont("arialblack", 15)
    cas_text = cas_font.render(f"TIME: {zbyvajici_cas}", True, white) # text času
    screen.blit(cas_text, (10, 30))

    #score
    score_font = pygame.font.SysFont("arialblack", 15)
    score_text = score_font.render(f"SCORE: {score}", True, white) # text score
    screen.blit(score_text, (10, 50))

    #jmeno
    jmeno_font = pygame.font.SysFont("arialblack", 15)
    jmeno_text = jmeno_font.render(f"PLAYER: {jmeno_hrace}", True, white) # text hráče
    screen.blit(jmeno_text, (10, 10))

        # vykreslení všech targetů
    for objekt in targets:  # projde všechny targety v listu
        pygame.draw.rect(screen, red, objekt) # vykreslí target


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

    # uloží do db jen jednou, ochrana pred kopirovanim score protoze v game_over běží vice framů
    if not score_odeslano:  # pokud ještě nebylo uloženo
        save_game(jmeno_hrace, vybrany_mode_id, score) # uloží hráče a hru do db
        score_odeslano = True   # nastav, že už to je uložené

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Kliknutí myši na tlačítko
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if back_button.collidepoint(mouse_pos): # klik na BACK
                cas_start = None # reset start času
                targets = []  # smaž targety
                target_size = 30 # reset velikosti targetu
                score = 0 # reset score
                stav_hry = HLAVNI_MENU
                return
    # automatický návrat po 4 sekundách pokud nebylo kliknuto na BACK
    if game_over_delay is not None:  # pokud je čas game over
        if pygame.time.get_ticks() - game_over_delay >= 4000:
            cas_start = None
            targets = []
            target_size = 30
            score = 0
            stav_hry = HLAVNI_MENU

#přepínání zvuku + uložení do audio.txt
def audio():
    global audio_zapnute

    audio_zapnute = not audio_zapnute #změna stavu kliknutím na tlacitko

    if audio_zapnute:  #pokud ma byt zvuk zapnuty a nehraje spust ho
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

    save_audio_setting(audio_zapnute) # uloží stav do souboru audio.txt
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
    pygame.display.update()   # překreslí obrazovk
    hodiny.tick(fps) # omezí rychlost smyčky na 60 FPS

# Ukončení hry
pygame.quit()