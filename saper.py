import pygame 
import random 

# Ініціалізація Pygame 
pygame.init() 
pygame.mixer.init() 
sound = pygame.mixer.Sound('muszik.mp3') 

# Відтворюємо звук 
sound.play() 
pygame.time.delay(50) 

# Параметри вікна гри 
WIDTH, HEIGHT = 700, 700 
ROWS, COLS = 10, 10 
CELL_SIZE = WIDTH // COLS 

# Кількість мін
MINES = 15

# Ініціалізація мін 
mines = [[0 for _ in range(COLS)] for _ in range(ROWS)] 
for _ in range(MINES): 
    row, col = random.randint(0, ROWS - 1), random.randint(0, COLS - 1) 
    mines[row][col] = 1 

# Колір клітинок та ліній 
WHITE = (255, 255, 255) 
GRAY = (200, 200, 200) 
BLACK = (0, 0, 0) 
GREEN = (0, 150, 0)
BLUE = (0, 0, 255) 
RED = (255, 0, 0) 

# Ініціалізація екрану 
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Сапер") 

# Завантаження фонового зображення 
space_img = pygame.image.load("space.png") 
space_img = pygame.transform.scale(space_img, (WIDTH, HEIGHT)) 

# Функція для отримання кількості сусідніх мін 
def count_neighboring_mines(row, col):
    count = 0
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if 0 <= r < ROWS and 0 <= c < COLS and mines[r][c] == 1:
                count += 1
    return count


# Функція для малювання клітинок та ліній 
def draw_grid():
    screen.blit(space_img, (0, 0))
    for row in range(ROWS):
        for col in range(COLS):
            if 0 <= row < ROWS and 0 <= col < COLS and revealed[row][col]:  # Перевірка меж
                x, y = col * CELL_SIZE, row * CELL_SIZE
                cell_color = GRAY if revealed[row][col] else BLACK
                pygame.draw.rect(screen, cell_color, (x, y, CELL_SIZE, CELL_SIZE))
                if 0 <= row < ROWS and 0 <= col < COLS and revealed[row][col] and not mines[row][col]:  # Перевірка меж
                    neighboring_mines = count_neighboring_mines(row, col)
                    if neighboring_mines:
                        font = pygame.font.Font(None, 24)
                        text = font.render(str(neighboring_mines), True, BLACK)
                        text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                        screen.blit(text, text_rect)
                if 0 <= row < ROWS and 0 <= col < COLS and revealed[row][col] and mines[row][col]:  # Перевірка меж
                    pygame.draw.rect(screen, RED, (x, y, CELL_SIZE, CELL_SIZE))

                if revealed[row][col] and mines[row][col]:
                    pygame.draw.rect(screen, RED, (x, y, CELL_SIZE, CELL_SIZE))

    for i in range(1, len(revealed)):
        pygame.draw.line(screen, RED, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))

    for j in range(1, len(revealed[0])):
        pygame.draw.line(screen, RED, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT))

# Функція для малювання кнопки "Почати гру" 
def draw_start_button(): 
    font = pygame.font.Font(None, 50) 
    text = font.render("Почати гру", True, WHITE) 
    button_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 350)) 
    pygame.draw.rect(screen, BLUE, button_rect) 
    screen.blit(text, button_rect) 

# Функція для малювання кнопки "Спробувати ще раз" 
def draw_try_again_button(): 
    font = pygame.font.Font(None, 36) 
    text = font.render("Спробувати ще раз", True, WHITE) 
    button_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2)) 
    pygame.draw.rect(screen, BLUE, button_rect) 
    screen.blit(text, button_rect) 

# Функція для малювання кнопок вибору рівня складності
def draw_difficulty_buttons():
    font = pygame.font.Font(None, 36)
    
    easy_button_text = font.render("Легкий", True, WHITE)
    easy_button_rect = easy_button_text.get_rect(center=(WIDTH // 4, HEIGHT // 2))
    pygame.draw.rect(screen, BLUE, easy_button_rect)
    screen.blit(easy_button_text, easy_button_rect)

    medium_button_text = font.render("Середній", True, WHITE)
    medium_button_rect = medium_button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, BLUE, medium_button_rect)
    screen.blit(medium_button_text, medium_button_rect)

    hard_button_text = font.render("Важкий", True, WHITE)
    hard_button_rect = hard_button_text.get_rect(center=(WIDTH // 4 * 3, HEIGHT // 2))
    pygame.draw.rect(screen, BLUE, hard_button_rect)
    screen.blit(hard_button_text, hard_button_rect)

# Функція для оновлення розмірів списків
def update_board_size():
    global revealed, mines
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)] 
    mines = [[0 for _ in range(COLS)] for _ in range(ROWS)] 
    for _ in range(MINES): 
        row, col = random.randint(0, ROWS - 1), random.randint(0, COLS - 1) 
        mines[row][col] = 1 

# Початковий стан гри 
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)] 
game_started = False 
game_over = False 
score = 0 
retry_clicked = False  # Визначення retry_clicked перед початком головного циклу гри

# Змінна для зберігання тексту "Game Over"
game_over_text = None   

# Головний цикл гри
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not game_started:
                if WIDTH // 4 - 100 <= mouse_x <= WIDTH // 4 + 100 and HEIGHT // 2 - 25 <= mouse_y <= HEIGHT // 2 + 25:
                    ROWS, COLS = 8, 8  # Легкий рівень
                    MINES = 10
                    game_started = True
                    update_board_size()  # Оновити розміри списків
                elif WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100 and HEIGHT // 2 - 25 <= mouse_y <= HEIGHT // 2 + 25:
                    ROWS, COLS = 12, 12  # Середній рівень
                    MINES = 20
                    game_started = True
                    update_board_size()  # Оновити розміри списків
                elif WIDTH // 4 * 3 - 100 <= mouse_x <= WIDTH // 4 * 3 + 100 and HEIGHT // 2 - 25 <= mouse_y <= HEIGHT // 2 + 25:
                    ROWS, COLS = 16, 16  # Важкий рівень
                    MINES = 40
                    game_started = True
                    update_board_size()  # Оновити розміри списків
            elif game_over and WIDTH // 2 - 100 <= mouse_x <= WIDTH // 2 + 100 and HEIGHT // 2 - 25 <= mouse_y <= HEIGHT // 2 + 25:
                # Якщо гра закінчилася і користувач клікнув на кнопку "Спробувати ще раз"
                print("Ви програли! Очки:", score)
                game_over_text = font.render("Game Over", True, RED,)
                score_text = font.render("Score: " + str(score), True, WHITE)
                game_over = False
                revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
                game_started = False
                score = 0
                retry_clicked = True  # Встановлюємо retry_clicked в True, якщо користувач натиснув на кнопку "Спробувати ще раз"
            elif game_started: 
                row, col = mouse_y // CELL_SIZE, mouse_x // CELL_SIZE 
                if not revealed[row][col]: 
                    revealed[row][col] = True 
                    if mines[row][col]: 
                        if mines[row][col]: 
    # Якщо користувач натрапив на міну, гра закінчується
                            print("Ви програли! Очки:", score)
                            game_over_text = font.render("Game Over", True, BLACK)
                            score_text = font.render("Score: " + str(score), True, WHITE)
                            game_over = True
                            game_started = False  # Завершуємо гру
                            revealed = [[True for _ in range(COLS)] for _ in range(ROWS)]  # Показуємо всі клітинки

                    else:
                        # Якщо користувач натиснув на пусту клітинку, збільшуємо рахунок
                        score += 10

    draw_grid()
    if not game_started:
        draw_difficulty_buttons()  # Малюємо кнопки для вибору рівня складності
    elif game_over:
        draw_try_again_button()
        if game_over_text:
            screen.blit(game_over_text, (WIDTH // 2 - 60, HEIGHT // 7))
            screen.blit(score_text, (WIDTH // 2 - 50, HEIGHT // 6 + 50))
    else:
        # Показати рахунок
        font = pygame.font.Font(None, 44)
        score_text = font.render("Score: " + str(score), True, GREEN)
    if retry_clicked:  
            game_over_text = None  
            score_text = None  
            retry_clicked = False  
    else: 
        # Показати рахунок 
        font = pygame.font.Font(None, 36) 
        score_text = font.render("Score: " + str(score), True, GREEN) 
        screen.blit(score_text, (10, 10))  # показати рахунок у верхньому лівому куті екрану 

    pygame.display.flip() 

pygame.quit()
