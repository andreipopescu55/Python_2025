import pygame
import json
import random

with open('config.json', 'r') as f:
    config = json.load(f)

BLOCK_SIZE = config['board']['block_size']
WIDTH = config['board']['width']
HEIGHT = config['board']['height']

pygame.init()
ecran= pygame.display.set_mode((WIDTH,HEIGHT))
ceas = pygame.time.Clock()

def genereaza_mancare(sarpe, obstacole):
    while True:
        x=random.randrange(0, WIDTH, BLOCK_SIZE)
        y=random.randrange(0, HEIGHT, BLOCK_SIZE)
        if[x,y] not in sarpe and [x,y] not in obstacole:
            return [x,y]
        

sarpe = config['snake']['start_pos']
obstacole = config['obstacles']
mancare= genereaza_mancare(sarpe, obstacole)
directie = 'DREAPTA'
schimba_in = directie
scor = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and directie != 'JOS': schimba_in = 'SUS'
            if event.key == pygame.K_DOWN and directie != 'SUS': schimba_in = 'JOS'
            if event.key == pygame.K_LEFT and directie != 'DREAPTA': schimba_in = 'LEFT'
            if event.key == pygame.K_RIGHT and directie != 'STANGA': schimba_in = 'DREAPTA'


    directie = schimba_in        
    
    cap_actual = list(sarpe[0])
    if directie == 'SUS': cap_actual[1] -= BLOCK_SIZE
    if directie == 'JOS': cap_actual[1] += BLOCK_SIZE
    if directie == 'STANGA': cap_actual[0] -= BLOCK_SIZE
    if directie == 'DREAPTA': cap_actual[0] += BLOCK_SIZE

    #  Coliziune cu pereții
    if cap_actual[0] < 0 or cap_actual[0] >= WIDTH or cap_actual[1] < 0 or cap_actual[1] >= HEIGHT:
        running = False
    
    #  Coliziune cu obstacolele
    if cap_actual in obstacole:
        running = False

    #  Coliziune cu propriul corp
    if cap_actual in sarpe:
        running = False

    # Actualizare corp șarpe
    sarpe.insert(0, cap_actual)

    if cap_actual == mancare:
        scor += 1
        mancare = genereaza_mancare(sarpe, obstacole)
    else:
        sarpe.pop()
    ecran.fill((0, 0, 0)) # Fundal negru
    for segment in sarpe:
        pygame.draw.rect(ecran, (0, 255, 0), [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])  
    for obs in obstacole:
        pygame.draw.rect(ecran, (213, 50, 80), [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])
    
    pygame.draw.rect(ecran, (255, 255, 255), [mancare[0], mancare[1], BLOCK_SIZE, BLOCK_SIZE])

    pygame.display.update()
    ceas.tick(config['snake']['speed'])

pygame.quit()      