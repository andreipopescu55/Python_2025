import pygame
import json
import random
import time
import os

with open('config.json', 'r') as f:
    config = json.load(f)

BLOCK_SIZE = config['board']['block_size']
WIDTH = config['board']['width']
HEIGHT = config['board']['height']


ALB = (255, 255, 255)
NEGRU = (0, 0, 0)
ROSU = (213, 50, 80)
VERDE = (0, 255, 0)
VERDE_CAP = (0, 150, 0)
GRI_INCHIS = (40, 40, 40)


def deseneaza_grid(ecran):
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(ecran, GRI_INCHIS, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(ecran, GRI_INCHIS, (0, y), (WIDTH, y))

def genereaza_mancare(sarpe, obstacole):
    while True:
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        if [x, y] not in sarpe and [x, y] not in obstacole:
            return [x, y]

def afiseaza_scoruri(scor_curent, record):
    font = pygame.font.SysFont("arial", 20)
    text_scor = font.render(f"Scor: {scor_curent}", True, ALB)
    text_record = font.render(f"Record: {record}", True, (255, 215, 0)) # Culoare aurie
    ecran.blit(text_scor, [10, 10])
    ecran.blit(text_record, [10, 35])

def ecran_final(scor_final):
    font_mare = pygame.font.SysFont("arial", 60, bold=True)
    font_mic = pygame.font.SysFont("arial", 30)
    
    t_game_over = font_mare.render("GAME OVER", True, ROSU)
    t_scor = font_mic.render(f"Scorul tău: {scor_final}", True, ALB)
    t_restart = font_mic.render("R - Restart | Q - Ieșire", True, ALB)
    t_record = font_mic.render(f"Record: {high_score}", True, ALB)

    r_game_over = t_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    r_scor = t_scor.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    r_restart = t_restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    r_record = t_record.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))

    ecran.fill(NEGRU)
    ecran.blit(t_game_over, r_game_over)
    ecran.blit(t_scor, r_scor)
    ecran.blit(t_restart, r_restart)
    ecran.blit(t_record,r_record)
    pygame.display.update()

def reseteaza_joc():
    global sarpe, mancare, directie, schimba_in, scor, coliziune,high_score
    
    sarpe = [list(pos) for pos in config['snake']['start_pos']]
    mancare = genereaza_mancare(sarpe, obstacole)
    directie = 'DREAPTA'
    schimba_in = 'DREAPTA'
    scor = 0
    coliziune = False 
    high_score = incarc_high_score()
    time.sleep(0.5)

def incarc_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def salveaza_high_score(nou_record):
    with open("highscore.txt", "w") as f:
        f.write(str(nou_record))

pygame.init()
ecran = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Proiect")
ceas = pygame.time.Clock()

obstacole = config['obstacles']
reseteaza_joc() 


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and directie != 'JOS': schimba_in = 'SUS'
            if event.key == pygame.K_DOWN and directie != 'SUS': schimba_in = 'JOS'
            if event.key == pygame.K_LEFT and directie != 'DREAPTA': schimba_in = 'STANGA'
            if event.key == pygame.K_RIGHT and directie != 'STANGA': schimba_in = 'DREAPTA'

    # --- LOGICĂ MIȘCARE ---
    directie = schimba_in
    cap_actual = list(sarpe[0])
    
    if directie == 'SUS': cap_actual[1] -= BLOCK_SIZE
    elif directie == 'JOS': cap_actual[1] += BLOCK_SIZE
    elif directie == 'STANGA': cap_actual[0] -= BLOCK_SIZE
    elif directie == 'DREAPTA': cap_actual[0] += BLOCK_SIZE

   
    if cap_actual[0] < 0 or cap_actual[0] >= WIDTH or cap_actual[1] < 0 or cap_actual[1] >= HEIGHT:
        coliziune = True
   
    if cap_actual in obstacole or cap_actual in sarpe:
        coliziune = True

   
    if coliziune:
        salveaza_high_score(high_score)
        ecran_final(scor)
        asteptare = True
        while asteptare:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    asteptare = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        asteptare = False
                    if event.key == pygame.K_r:
                        reseteaza_joc() 
                        asteptare = False
        continue 
    
    sarpe.insert(0, cap_actual)
    if cap_actual == mancare:
        scor += 1
        if scor > high_score:
            high_score = scor
        mancare = genereaza_mancare(sarpe, obstacole)
    else:
        sarpe.pop()

 
    ecran.fill(NEGRU)
    deseneaza_grid(ecran)
    

    for obs in obstacole:
        pygame.draw.rect(ecran, ROSU, [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])
    

    for i, segment in enumerate(sarpe):
        culoare = VERDE_CAP if i == 0 else VERDE
        pygame.draw.rect(ecran, culoare, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])
        pygame.draw.rect(ecran, NEGRU, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE], 1)
    

    pygame.draw.rect(ecran, ALB, [mancare[0], mancare[1], BLOCK_SIZE, BLOCK_SIZE])
    
    afiseaza_scoruri(scor,high_score)
    pygame.display.update()
    ceas.tick(config['snake']['speed'])

pygame.quit()