import pygame
import time
import random 
from glob import glob 


file_name = "results.txt"
if not glob(file_name):
    with open(file_name,"w") as f:
        pass

pygame.font.init()

def create_field(rows,cols):
    matrix = []
    for i in range(rows):
        matrix.append([0] * cols)    
    return matrix

def read_results():
    with open("results.txt", "r", encoding= "UTF-8") as f:
        strings = f.readlines()
    info = {}
    for string in strings:
        k,v = string.strip().split(" --> ")
        info[k] = int(v)
    return info



def gen_field(rows,cols,bombs):
    matrix = create_field(rows,cols)
    for i in range(bombs):
        x = random.randint(1,cols)
        y = random.randint(1,rows)
        while matrix[y-1][x-1] == '*':
            x = random.randint(1,cols)
            y = random.randint(1,rows)
        matrix[y - 1][x - 1] = '*' 
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == '*':
                if i + 1 < rows and matrix[i + 1][j] != '*':
                    matrix[i + 1][j] += 1
                if j + 1 < cols and matrix[i][j + 1] != '*':
                    matrix[i][j + 1] += 1
                if i - 1 > - 1 and matrix[i - 1][j] != '*':
                    matrix[i - 1][j] += 1
                if j - 1 > - 1 and matrix[i][j - 1] != '*':
                    matrix[i][j - 1] += 1
                if i + 1 < rows and j + 1 < cols and matrix[i + 1][j + 1] != '*':
                    matrix[i + 1][j + 1] += 1
                if i - 1 > - 1 and j - 1 > -1 and matrix[i - 1][j - 1] != '*':
                    matrix[i - 1][j - 1] += 1
                if i + 1 < rows and j - 1 > - 1 and matrix[i + 1][j - 1] != '*':
                    matrix[i + 1][j - 1] += 1
                if i - 1 > - 1 and j + 1 < cols and matrix[i - 1][j + 1] != '*':
                    matrix[i - 1][j + 1] += 1
    return matrix




side = 30
font = pygame.font.SysFont('Arial', side - 10) 
GREEN = (0,255,0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
cols = 20
rows = 15
last_state = ''
flag_klick = 0
bombs = 3
GRAY = (127, 127,127)
screen = pygame.display.set_mode((cols * side, rows * side + 50))
time_on = False


def start_game():
    winner = cols * rows
    field = gen_field(rows, cols, bombs)
    click_field = create_field(rows,cols)
    state = 'game on'

    pygame.draw.rect(screen, WHITE,(0,0 ,cols * side, rows * side))

    for i in range(cols):
        pygame.draw.rect(screen, BLACK,(i * side - 1,0 ,2, rows * side))
    for i in range(rows):
        pygame.draw.rect(screen, BLACK,(0,i * side - 1, cols * side,2))
    pygame.draw.rect(screen, BLACK, (cols * side // 2 - 75, rows * side + 5, 150, 299))
    pygame.display.update()
    start = time.time()
    last = start
    restart_img = pygame.image.load("restart.jpg") 
    restart_img = pygame.transform.scale(restart_img, (side - 2, side - 2))
    screen.blit(restart_img,(cols * side // 2 + 85, rows * side + 5))

    stats_img = pygame.image.load("stats.jpg") 
    stats_img = pygame.transform.scale(stats_img, (side - 2, side - 2))
    screen.blit(stats_img,(10, rows * side + 5))
    show_col_bombs()
    return field, click_field, state, last, start,winner

# field, click_field, state, last, start, winner = start_game()

state = "menu"
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

def draw_zero():
    mark = True
    global winner
    while mark:
        mark = False
        for row in range(rows):
            for col in range(cols):
                if field[row][col] == 0 and click_field[row][col] == '/':
                    if row + 1 < rows and click_field[row + 1][col] == 0:
                        mark = True
                        if field[row + 1][col] == 0:                                            
                            pygame.draw.rect(screen, GRAY,(col * side, (row + 1) * side, side, side))
                        else:
                            text_simvol = font.render(str(field[row + 1][col]), False, BLACK)
                            screen.blit(text_simvol,(col  * side + int(0.4 * side), (row + 1) * side))
                        click_field[row + 1][col] = '/'  
                        winner -= 1
                    if col + 1 < cols and click_field[row][col + 1] == 0:
                        mark = True
                        if field[row][col + 1] == 0:                                            
                            pygame.draw.rect(screen, GRAY,((col + 1) * side, row * side, side, side))
                        else:
                            text_simvol = font.render(str(field[row][col + 1]), False, BLACK)
                            screen.blit(text_simvol,((col + 1) * side + int(0.4 * side), row * side))
                        click_field[row][col + 1] = '/'  
                        winner -= 1
                    if col - 1 >= 0  and click_field[row][col - 1] == 0:
                        mark = True
                        if field[row][col - 1] == 0:                                            
                            pygame.draw.rect(screen, GRAY,((col - 1) * side, row * side, side, side))
                        else:
                            text_simvol = font.render(str(field[row][col - 1]), False, BLACK)
                            screen.blit(text_simvol,((col - 1) * side + int(0.4 * side), row * side))
                        click_field[row][col - 1] = '/'  
                        winner -= 1
                    if row - 1 >= 0 and click_field[row - 1][col] == 0:
                        mark = True
                        if field[row - 1][col] == 0:                                            
                            pygame.draw.rect(screen, GRAY,(col * side, (row - 1) * side, side, side))
                        else:
                            text_simvol = font.render(str(field[row - 1][col]), False, BLACK)
                            screen.blit(text_simvol,(col  * side + int(0.4 * side), (row - 1) * side))
                        click_field[row - 1][col] = '/' 
                        winner -= 1 
                    if row - 1 >= 0 and col - 1 >= 0 and click_field[row - 1][col - 1] == 0: #--
                        mark = True
                        if field[row - 1][col - 1] == 0:                                            
                            pygame.draw.rect(screen, GRAY,((col - 1) * side, (row - 1) * side, side, side))
                        else:
                            text_simvol = font.render(str(field[row - 1][col - 1]), False, BLACK)
                            screen.blit(text_simvol,((col - 1)  * side + int(0.4 * side), (row - 1) * side))
                        click_field[row - 1][col - 1] = '/' 
                        winner -= 1
                    if row - 1 >= 0 and col + 1 < cols and click_field[row - 1][col + 1] == 0: # -+
                        mark = True
                        if field[row - 1][col + 1] == 0:                                            
                            pygame.draw.rect(screen, GRAY,((col + 1) * side, (row - 1) * side, side, side))
                        else:
                            text_simvol = font.render(str(field[row - 1][col + 1]), False, BLACK)
                            screen.blit(text_simvol,((col + 1)  * side + int(0.4 * side), (row - 1) * side))
                        click_field[row - 1][col + 1] = '/' 
                        winner -= 1
                    if row + 1 < rows and col + 1 < cols and click_field[row + 1][col + 1] == 0: # ++
                        mark = True
                        if field[row + 1][col + 1] == 0:                                            
                            pygame.draw.rect(screen, GRAY,((col + 1) * side, (row + 1) * side, side, side))
                        else:
                            text_simvol = font.render(str(field[row + 1][col + 1]), False, BLACK)
                            screen.blit(text_simvol,((col + 1) * side + int(0.4 * side), (row + 1) * side))
                        click_field[row + 1][col + 1] = '/'
                        winner -= 1 
                    if row + 1 < rows and col - 1 >= 0 and click_field[row + 1][col - 1] == 0: # +-
                        mark = True
                        if field[row + 1][col - 1] == 0:                                            
                            pygame.draw.rect(screen, GRAY,((col - 1) * side, (row + 1) * side, side, side))
                        else:
                            text_simvol = font.render(str(field[row + 1][col - 1]), False, BLACK)
                            screen.blit(text_simvol,((col - 1)  * side + int(0.4 * side), (row + 1) * side))
                        click_field[row + 1][col - 1] = '/' 
                        winner -= 1

def show_stats():
    results = read_results()
    pygame.draw.rect(screen, WHITE,(0,0 ,cols * side, rows * side))
    for i in range(rows):
        pygame.draw.rect(screen, BLACK,(0,i * side - 1, cols * side,1))
    mesto = 1
    pygame.draw.rect(screen, BLACK,(side + 5,0 ,1, rows * side - 30))
    pygame.draw.rect(screen, BLACK,(side + 450,0 ,1, rows * side - 30))

    text = "Легкий"
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (60,14 * side)) 
    pygame.draw.rect(screen, BLACK,(side + 170,420 ,1, side))

    text = "Средний"
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (262,14 * side)) 
    pygame.draw.rect(screen, BLACK,(side + 370,420 ,1, side))

    text = "Сложный"
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (465,14 * side)) 

    text = "№"
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (13,5)) 

    text = "Имя"
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (250,5)) 

    text = "Время"
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (510,5)) 

    for name, seconds in results.items():
        text = f"{mesto}"
        rendered_text = font.render(text, True, BLACK)
        screen.blit(rendered_text, (15,mesto * side)) 


        text = f"{name}"
        rendered_text = font.render(text, True, BLACK)
        screen.blit(rendered_text, (250,mesto * side)) 


        text = f"{seconds // 60}m {seconds % 60}c"
        rendered_text = font.render(text, True, BLACK)
        screen.blit(rendered_text, (510,mesto * side)) 
        mesto += 1   
    
def show_col_bombs():
    pygame.draw.rect(screen, BLACK,(cols * side - 35, rows * side + 30, 100, 100))
    show_bomb = str(bombs - flag_klick)
    x = font.render(show_bomb,True,WHITE)
    screen.blit(x, (cols * side - 30, rows * side + 30))



def update_screen(state):
    pygame.draw.rect(screen, WHITE,(0,0 ,cols * side, rows * side))
    for i in range(cols):
        pygame.draw.rect(screen, BLACK,(i * side - 1,0 ,2, rows * side))
    for i in range(rows):
        pygame.draw.rect(screen, BLACK,(0,i * side - 1, cols * side,2))
    for row in range(rows):
        for col in range(cols):
            if click_field[row][col] == "-":
                image_ = pygame.image.load("flag.jpg") 
                image_ = pygame.transform.scale(image_, (side - 2, side - 2))
                x = col * side
                y = row * side
                screen.blit(image_,(x,y))
    image_ = pygame.image.load("flag.jpg") 
    image_ = pygame.transform.scale(image_, (side - 2, side - 2))
    for row in range(rows):
        for col in range(cols):
            if click_field[row][col] == '/':
                if field[row][col] == 0:
                    pygame.draw.rect(screen, GRAY,(col * side, (row) * side, side, side))
                elif field[row][col] != '*':
                    text_simvol = font.render(str(field[row][col]), False, BLACK)
                    screen.blit(text_simvol,(col  * side + int(0.4 * side), (row) * side))
            if field[row][col] == '*':
                if state == "game off":
                    image = pygame.image.load("simvol_saper.png") 
                    image = pygame.transform.scale(image, (side, side))
                    x = col * side
                    y = row * side
                    screen.blit(image,(x,y))
                elif click_field[row][col] == "-":
                    image_ = pygame.image.load("flag.jpg") 
                    image_ = pygame.transform.scale(image_, (side - 2, side - 2))
                    x = col * side
                    y = row * side
                    screen.blit(image_,(x,y))




while True:
    events = pygame.event.get()
    for i in range(len(events)):
        if events[i].type == pygame.QUIT:
            exit()
        if events[i].type == pygame.MOUSEBUTTONDOWN and events[i].button == 1:
            x, y = events[i].pos
            
            restart_left = cols * side // 2 + 85
            restart_up = rows * side + 5
            if restart_left <= x <= restart_left + (side - 2) and restart_up <= y <= restart_up +(side - 2):
                field, click_field, state, last, start, winner = start_game()
                time_on = False
                pygame.draw.rect(screen, BLACK,(cols * side - 35, rows * side + 5, 50, 20)) # замазываем таймер

            stats_left = 10
            stats_up = rows * side + 5
            if stats_left <= x <= stats_left + (side - 2) and stats_up <= y <= stats_up +(side - 2):
                if state != "stats":
                    last_state = state
                    show_stats()
                    state = "stats"
                else:
                    state = last_state
                    update_screen(state)
        if state == 'game on':
            if events[i].type == pygame.MOUSEBUTTONDOWN:
                x, y = events[i].pos
                if y < rows * side:
                    if not time_on:
                        time_on = True
                        start = time.time()
                    x -= x % side
                    y -= y % side
                    if events[i].button == 1 and click_field[y // side][x // side] == 0:
                        if field[y // side][x // side] == '*':
                            state = 'game off'
                            font2 = pygame.font.SysFont('Times New Roman', 28) 
                            print_lose = font2.render('YOU LOSE!',True,YELLOW)
                            screen.blit(print_lose, (cols * side // 2 - 75, rows * side + 5))
                            image = pygame.image.load("simvol_saper.png") 
                            image = pygame.transform.scale(image, (side, side))
                            for row in range(rows):
                                for col in range(cols):
                                    if field[row][col] == '*':
                                        x = col * side
                                        y = row * side
                                        screen.blit(image,(x,y))
                        elif field[y // side][x // side] == 0 :  
                            click_field[y // side][x // side] = '/'
                            winner -= 1
                            draw_zero()                                              
                            pygame.draw.rect(screen, GRAY,(x,y, side, side))
                        else:
                            text_simvol = font.render(str(field[y // side][x // side]), False, BLACK)
                            screen.blit(text_simvol, (x + int(0.4 * side), y))
                            click_field[y // side][x // side] = '/'
                            winner -= 1
                    elif events[i].button == 3 and click_field[y // side][x // side] != '/':
                        if click_field[y // side][x // side] == "-":
                            click_field[y // side][x // side] = 0
                            pygame.draw.rect(screen, WHITE,(x + 1,y + 1,side - 2,side - 2))
                            flag_klick -= 1
                            show_col_bombs() 
                        else:
                            click_field[y // side][x // side] = '-'
                            image_ = pygame.image.load("flag.jpg") 
                            image_ = pygame.transform.scale(image_, (side - 2, side - 2))
                            flag_klick += 1
                            show_col_bombs()
                            screen.blit(image_,(x + 1,y + 1))
       
        if state == "menu":
            if events[i].type == pygame.MOUSEBUTTONDOWN and events[i].button == 1:
                x, y = events[i].pos

                if 100 <= x <= 200 and 300 <= y <= 400:
                    print("eazy")
                    bombs = 10
                    rows = 15
                    cols = 10
                    screen = pygame.display.set_mode((cols * side, rows * side + 50))
                    field, click_field, state, last, start, winner = start_game()
                if 240 <= x <= 340 and 300 <= y <= 400:
                    print("normal")
                    bombs = 40
                    rows = 20
                    cols = 15
                    screen = pygame.display.set_mode((cols * side, rows * side + 50))
                    field, click_field, state, last, start, winner = start_game()
                if 380 <= x <= 480 and 300 <= y <= 400:
                    print("hard")
                    bombs = 130
                    rows = 25
                    cols = 35
                    screen = pygame.display.set_mode((cols * side, rows * side + 50))
                    field, click_field, state, last, start, winner = start_game()    
            if events[i].type == pygame.KEYDOWN:
                letter = events[i].unicode
                if letter.isalpha():
                    player_name += letter
                    print_name()
                if events[i].key == 8:
                    player_name = player_name[:-1]
                    print_name()
    
    if state == "game on" and winner == bombs:
        p =int(time.time() - start)
        print('WIN!')
        state = 'game off'
        font2 = pygame.font.SysFont('Times New Roman', 28)
        print_win = font2.render('YOU WIN!',True,YELLOW)
        screen.blit(print_win, (cols * side // 2 - 75, rows * side + 5))
        pygame.display.update()
        # name = input("Введите свое имя: ")
        
        m = open("results.txt", "r", encoding="UTF-8")
        met = True
        results = []
        for stroka in m.readlines():
            name2,res2 = stroka.split(" --> ")
            res2 = int(res2)
            if player_name == name2:
                met = False
                if res2 > p:
                    res2 = p
            results.append((res2, name2))
        if met:
            results.append((p,player_name))
        results.sort()
        m.close()
        m = open("results.txt", "w", encoding="UTF-8")
        print(results)
        for place in results:
            player_name = place[1]
            p = place[0]
            m.write(f"{player_name} --> {p}\n")
        m.close()
        
    if (state == 'game on' or state == 'stats' and last_state == "game on") and time.time() - last >= 0.1 and time_on:
        pygame.draw.rect(screen, BLACK,(cols * side - 35, rows * side + 5, 50, 20))
        show_time = str(int(time.time() - start))
        x = font.render(show_time,True,WHITE)
        last = time.time()  
        screen.blit(x, (cols * side - 30, rows * side + 5))
    pygame.display.update()
