import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
szerokosc = 800
wysokosc = 600
ekran = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption("Ping Pong z ekranem startowym i końcowym")

# Ustawienia paletki
paletka_szerokosc = 100
paletka_wysokosc = 10
paletka_predkosc = 3  # Prędkość paletki (domyślnie 3)
paletka_x = (szerokosc - paletka_szerokosc) // 2
paletka_y = wysokosc - paletka_wysokosc - 20

# Ustawienia piłki
pilka_x = szerokosc // 2
pilka_y = wysokosc // 2
pilka_predkosc_x = 0.1
pilka_predkosc_y = -0.2
pilka_srednica = 20
przyśpieszenie = 0.1

# Ustawienia wyniku
wynik = 0
font = pygame.font.Font(None, 36)

# Stany gry
STAN_EKRAN_STARTOWY = 0
STAN_GRY = 1
STAN_EKRAN_KONCOWY = 2
stan_gry = STAN_EKRAN_STARTOWY

def rysuj_paletke():
    pygame.draw.rect(ekran, (255, 255, 255), (paletka_x, paletka_y, paletka_szerokosc, paletka_wysokosc))

def rysuj_pilke():
    pygame.draw.circle(ekran, (255, 255, 255), (pilka_x, pilka_y), pilka_srednica // 2)

def rysuj_wynik():
    text = font.render(f"Wynik: {wynik}", True, (255, 255, 255))
    ekran.blit(text, (20, 20))

def rysuj_ekran_startowy():
    ekran.fill((0, 0, 0))
    tekst = font.render("Naciśnij SPACJĘ, aby rozpocząć", True, (255, 255, 255))
    tekst_predkosc = font.render(f"Prędkość paletki: {paletka_predkosc}", True, (255, 255, 255))
    ekran.blit(tekst, (szerokosc // 2 - tekst.get_width() // 2, wysokosc // 2 - 50))
    ekran.blit(tekst_predkosc, (szerokosc // 2 - tekst_predkosc.get_width() // 2, wysokosc // 2 + 20))

def rysuj_ekran_koncowy():
    ekran.fill((0, 0, 0))
    tekst = font.render(f"Koniec gry. Twój wynik: {wynik}", True, (255, 255, 255))
    ekran.blit(tekst, (szerokosc // 2 - tekst.get_width() // 2, wysokosc // 2 - 50))
    przycisk_restart = pygame.Rect(szerokosc // 2 - 100, wysokosc // 2 + 20, 200, 50)
    przycisk_wyjscie = pygame.Rect(szerokosc // 2 - 100, wysokosc // 2 + 80, 200, 50)
    pygame.draw.rect(ekran, (0, 255, 0), przycisk_restart)
    pygame.draw.rect(ekran, (255, 0, 0), przycisk_wyjscie)
    tekst_restart = font.render("Restart", True, (0, 0, 0))
    tekst_wyjscie = font.render("Wyjście", True, (0, 0, 0))
    ekran.blit(tekst_restart, (szerokosc // 2 - tekst_restart.get_width() // 2, wysokosc // 2 + 30))
    ekran.blit(tekst_wyjscie, (szerokosc // 2 - tekst_wyjscie.get_width() // 2, wysokosc // 2 + 90))

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and stan_gry == STAN_EKRAN_STARTOWY:
                stan_gry = STAN_GRY
            elif event.key == pygame.K_UP:
                paletka_predkosc += 1
            elif event.key == pygame.K_DOWN:
                paletka_predkosc = max(1, paletka_predkosc - 1)
        elif event.type == pygame.MOUSEBUTTONDOWN and stan_gry == STAN_EKRAN_KONCOWY:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            przycisk_restart = pygame.Rect(szerokosc // 2 - 100, wysokosc // 2 + 20, 200, 50)
            przycisk_wyjscie = pygame.Rect(szerokosc // 2 - 100, wysokosc // 2 + 80, 200, 50)
            if przycisk_restart.collidepoint(mouse_x, mouse_y):
                stan_gry = STAN_GRY
                pilka_x = szerokosc // 2
                pilka_y = wysokosc // 2
                pilka_predkosc_x = 0.1
                pilka_predkosc_y = -0.2
                wynik = 0
            elif przycisk_wyjscie.collidepoint(mouse_x, mouse_y):
                running = False

    if stan_gry == STAN_GRY:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paletka_x > 0:
            paletka_x -= paletka_predkosc/10
        if keys[pygame.K_RIGHT] and paletka_x < szerokosc - paletka_szerokosc:
            paletka_x += paletka_predkosc/10

        pilka_x += pilka_predkosc_x
        pilka_y += pilka_predkosc_y

        # Kolizja z paletką
        if (paletka_x <= pilka_x <= paletka_x + paletka_szerokosc) and (paletka_y <= pilka_y + pilka_srednica // 2 <= paletka_y + paletka_wysokosc):
            pilka_predkosc_y *= -1
            wynik += 1

            # Przyśpieszenie piłki po odbiciu
            pilka_predkosc_x += random.uniform(-przyśpieszenie, przyśpieszenie)
            pilka_predkosc_y += random.uniform(-przyśpieszenie, przyśpieszenie)

        # Kolizja z górnym brzegiem ekranu
        if pilka_y <= 0:
            pilka_predkosc_y *= -1

        # Kolizja z bokami ekranu
        if pilka_x <= 0 or pilka_x >= szerokosc:
            pilka_predkosc_x *= -1

        # Zakończ grę, jeśli piłka dotknie dolnej krawędzi ekranu
        if pilka_y >= wysokosc:
            stan_gry = STAN_EKRAN_KONCOWY

        # Prędkość piłki nie może przekroczyć pewnej wartości maksymalnej
        predkosc_max = 4.0
        pilka_predkosc_x = min(predkosc_max, max(-predkosc_max, pilka_predkosc_x))
        pilka_predkosc_y = min(predkosc_max, max(-predkosc_max, pilka_predkosc_y))

    ekran.fill((0, 0, 0))
    if stan_gry == STAN_EKRAN_STARTOWY:
        rysuj_ekran_startowy()
    elif stan_gry == STAN_GRY:
        rysuj_paletke()
        rysuj_pilke()
        rysuj_wynik()
    elif stan_gry == STAN_EKRAN_KONCOWY:
        rysuj_ekran_koncowy()

    pygame.display.flip()

# Zamknięcie Pygame po zakończeniu gry
pygame.quit()
