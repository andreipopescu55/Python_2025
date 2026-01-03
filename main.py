import pygame
import json
import random
import time 

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
        x=random.randrange(0, WIDTH, BLOCK_SIZE)
        y=random.randrange(0, HEIGHT, BLOCK_SIZE)
        if[x,y] not in sarpe and [x,y] not in obstacole:
            return [x,y]
        
def afiseaza_scor(scor):
    font = pygame.font.SysFont("arial", 25)
    valoare = font.render("Scor: " + str(scor), True, ALB)
    ecran.blit(valoare, [10, 10])        
        

def ecran_final(scor_final):
    # 1. Pregătim fonturile
    font_mare = pygame.font.SysFont("arial", 60, bold=True)
    font_mic = pygame.font.SysFont("arial", 30)

   
    text_game_over = font_mare.render("GAME OVER", True, ROSU)
    text_scor = font_mic.render(f"Scorul tău: {scor_final}", True, ALB)
    text_restart = font_mic.render("Apasă R pentru Restart sau Q pentru Ieșire", True, GRI_INCHIS)

   
   
    rect_game_over = text_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    rect_scor = text_scor.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    rect_restart = text_restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))

   
    ecran.fill(NEGRU)
    ecran.blit(text_game_over, rect_game_over)
    ecran.blit(text_scor, rect_scor)
    ecran.blit(text_restart, rect_restart)
    
    pygame.display.update()


pygame.init()
ecran= pygame.display.set_mode((WIDTH,HEIGHT))
ceas = pygame.time.Clock()

sarpe = config['snake']['start_pos']
obstacole = config['obstacles']
mancare= genereaza_mancare(sarpe, obstacole)
directie = 'DREAPTA'
schimba_in = directie
scor = 0
coliziune = 0 

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


    directie = schimba_in        
    
    cap_actual = list(sarpe[0])
    if directie == 'SUS': cap_actual[1] -= BLOCK_SIZE
    if directie == 'JOS': cap_actual[1] += BLOCK_SIZE
    if directie == 'STANGA': cap_actual[0] -= BLOCK_SIZE
    if directie == 'DREAPTA': cap_actual[0] += BLOCK_SIZE

    #  Coliziune cu pereții
    if cap_actual[0] < 0 or cap_actual[0] >= WIDTH or cap_actual[1] < 0 or cap_actual[1] >= HEIGHT:
        coliziune = 1
    
    #  Coliziune cu obstacolele
    if cap_actual in obstacole:
       coliziune = 1

    #  Coliziune cu propriul corp
    if cap_actual in sarpe:
       coliziune = 1

    if coliziune ==1:
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
                        # RESETARE JOC
                        sarpe = list(config['snake']['start_pos'])
                        mancare = genereaza_mancare(sarpe, obstacole)
                        directie = 'DREAPTA'
                        schimba_in = 'DREAPTA'
                        scor = 0
                        asteptare = False 
        continue

    # Actualizare corp șarpe
    sarpe.insert(0, cap_actual)
   
    if running == False:
        time.sleep(1)

    if cap_actual == mancare:
        scor += 1
        mancare = genereaza_mancare(sarpe, obstacole)
    else:
        sarpe.pop()
    
    ecran.fill(NEGRU) 
    
    deseneaza_grid(ecran) 

   
    for obs in obstacole:
        pygame.draw.rect(ecran, ROSU, [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])

    # 4. Șarpele (Cap vs Corp)
    for i, segment in enumerate(sarpe):
        culoare_segment = VERDE_CAP if i == 0 else VERDE
        pygame.draw.rect(ecran, culoare_segment, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])
       
    # 5. Mâncarea
    pygame.draw.rect(ecran, ALB, [mancare[0], mancare[1], BLOCK_SIZE, BLOCK_SIZE])
    
    afiseaza_scor(scor)

    pygame.display.update()
    ceas.tick(config['snake']['speed'])

pygame.quit()      