import pygame

# Inicializace hry
pygame.init()

# Nastavení obrazovky
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("CLICK IT GAME")

# Herní možnosti
show_menu = False

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

# Funkce pro kreslení tlačítek
def draw_button(text, y, color):
    button_text = menu_font.render(text, True, color)
    button_rect = button_text.get_rect(center=(width//2, y))
    screen.blit(button_text, button_rect)
    return button_rect

# Hlavní cyklus
running = True
while running:
    screen.fill(black)
    screen.blit(title_text, title_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Stisk mezerníku
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_menu = True

        # Kliknutí myší na tlačítka
        if event.type == pygame.MOUSEBUTTONDOWN and show_menu:
            mouse_pos = pygame.mouse.get_pos()
            if start_button.collidepoint(mouse_pos):
                print("Hra")
            elif audio_button.collidepoint(mouse_pos):
                print("Audio")

    # Pokud je menu aktivní
    if show_menu:
        start_button = draw_button("Start", 200, white)
        audio_button = draw_button("Audio", 270, white)
    else:
        tip_text = small_font.render("Press SPACE to load the game", True, white)
        tip_rect = tip_text.get_rect(center=(width//2, height//2))
        screen.blit(tip_text, tip_rect)

    # Aktualizace obrazovky
    pygame.display.update()

# Ukončení hry
pygame.quit()