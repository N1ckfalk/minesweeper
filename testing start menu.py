from time import time
import pygame

pygame.font.init()

side = 30
font = pygame.font.SysFont('Arial', side - 10) 
GREEN = (0,255,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
cols = 20
rows = 15

screen = pygame.display.set_mode((cols * side, rows * side + 50))
player_name = ""
def print_name():
    pygame.draw.rect(screen, WHITE, (150, 200, 280,50))
    font2 = pygame.font.SysFont('Times New Roman', 28)
    print_win = font2.render(player_name,True,BLACK)
    screen.blit(print_win, (150, 210))
print_name()

def difficult_menu():
    j = 300
    font2 = pygame.font.SysFont('Times New Roman', 20)
    p = 100
    pygame.draw.rect(screen, WHITE, (p, j, 100,100))
    screen.blit(font2.render("   Легкий",True,BLACK), (p, j))
    screen.blit(font2.render("   15x10",True,BLACK), (p, j + 30))
    screen.blit(font2.render("   10 бомб",True,BLACK), (p, j + 60))
    p = 240
    pygame.draw.rect(screen, WHITE, (p, j, 100,100))
    screen.blit(font2.render("   Средний",True,BLACK), (p, j))
    screen.blit(font2.render("   20x15",True,BLACK), (p, j + 30))
    screen.blit(font2.render("   40 бомб",True,BLACK), (p, j + 60))
    p = 380
    pygame.draw.rect(screen, WHITE, (p, j, 100,100))
    screen.blit(font2.render("  Сложный",True,BLACK), (p, j))
    screen.blit(font2.render("  35x25",True,BLACK), (p, j + 30))
    screen.blit(font2.render("  130 бомб",True,BLACK), (p, j + 60))

difficult_menu()

while True:
    events = pygame.event.get()
    for i in range(len(events)):
        if events[i].type == pygame.QUIT:
            exit()
        if events[i].type == pygame.MOUSEBUTTONDOWN and events[i].button == 1:
            x, y = events[i].pos


        if events[i].type == pygame.KEYDOWN:
            print(events[i])
            letter = events[i].unicode
            if letter.isalpha():
                player_name += letter
                print_name()
            if events[i].key == 8:
                player_name = player_name[:-1]
                print_name()
    pygame.display.update()