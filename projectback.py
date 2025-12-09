import pygame
import sys
import random

pygame.init()

#screen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Working Memory Game - Johanna Sabio")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

TITLE_FONT = pygame.font.SysFont("Times New Roman", 70)
TEXT_FONT = pygame.font.SysFont("Times New Roman", 36)





# quit with escape 
def check_quit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE: 
            pygame.quit()
            sys.exit()

# title 
def title_screen(duration_ms=10000):
    start_time = pygame.time.get_ticks()
    running = True
    while running:
        if pygame.time.get_ticks() - start_time > duration_ms:
            running = False
        screen.fill(WHITE)
        title_text = TITLE_FONT.render("Working Memory Game", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(title_text, title_rect)
        pygame.display.update()
      
        for event in pygame.event.get():
            check_quit(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False

#end screen 
def end_screen():
    end_time = pygame.time.get_ticks()
    running = True
    text_lines = [
        "This game is an adapted version of the Corsi",
        "Block tapping test. This task is used in",
        "cognitive neuroscience to measure visuospatial",
        "working memory. An average score for a",
        "healthy adult is around 6 blocks.",
        "This task can be performed either forwards",
        "or backwards in cognitive neuroscience research.",
        "Some regions of the brain that involve visuospatial",
        "memory include the parietal, prefrontal cortex, and", 
        "the hippocampus.",
        "",
        "Thanks for playing! Press ESC to exit!"
    ]



    while running:
        screen.fill(WHITE)
        y_offset = 120
        for line in text_lines:
            rendered_line = TEXT_FONT.render(line, True, BLACK)
            line_rect = rendered_line.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(rendered_line, line_rect)
            y_offset += 40  

        pygame.display.update()

        for event in pygame.event.get():
            check_quit(event)
       
           

# instructions
def show_instructions():
    reading = True
    while reading:
        screen.fill(WHITE)
        instructions = [
            "You will see blocks flash in a sequence.",
            "Your job is to repeat the sequence by",
            "clicking the same blocks in the same order.",
            "",
            "For every sequence entered correctly, the",
            "next sequence will increase by one block.",
            "",
            "The game will end when a sequence is entered",
            "incorrectly.", 
            "",
            "The game will start with a sequence of 2 blocks.",
            "",
            "Press SPACE to begin, ESC to exit."
        ]
        y_offset = 100
        for line in instructions:
            rendered_line = TEXT_FONT.render(line, True, BLACK)
            line_rect = rendered_line.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(rendered_line, line_rect)
            y_offset += 40  

        pygame.display.update()
        for event in pygame.event.get():
            check_quit(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reading = False
       
        
# https://www.pygame.org/docs/
# https://docs.python.org/3/library/random.html
def start_corsi_game(grid_size=3, sequence_length=3):
    # grid 
    margin = 50
    block_size = (SCREEN_WIDTH -100) // grid_size
    grid_positions = []
    for row in range(grid_size):
        for col in range(grid_size):
            x = margin + col * block_size
            y = margin + row * block_size
            grid_positions.append(pygame.Rect(x, y, block_size, block_size))

    sequence = random.sample(grid_positions, sequence_length)

    for block in sequence:
        screen.fill(WHITE)
        for rect in grid_positions:
            pygame.draw.rect(screen, BLACK, rect, 1)  
        pygame.draw.rect(screen, GREEN, block)   
        pygame.display.update()
        pygame.time.delay(800)
        screen.fill(WHITE)

        
        for rect in grid_positions:
            pygame.draw.rect(screen, BLACK, rect,1)
        pygame.display.update()
        pygame.time.delay(300)

       
    return sequence, grid_positions



def player_sequence(sequence, grid_positions):
    user_click = []
    userinput = True

    while userinput:
        screen.fill(WHITE)
        for rect in grid_positions:
            pygame.draw.rect(screen, BLACK, rect, 1)
        for block in user_click:
            pygame.draw.rect(screen, GREEN, block)
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_quit(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                user_pos = pygame.mouse.get_pos()
                for rect in grid_positions:
                    if rect.collidepoint(user_pos):
                        user_click.append(rect)
                        pygame.draw.rect(screen, GREEN, rect)
                        pygame.display.update()
                        pygame.time.delay(200)

        if len(user_click) == len(sequence):
            userinput = False
            
    correct_answer = user_click == sequence
    return correct_answer


title_screen(10000)
show_instructions()


# Loop 
running = True
sequence_length = 2
grid_size = 3

while running:
    sequence, grid_positions = start_corsi_game(grid_size, sequence_length)
    
    correct_answer = player_sequence(sequence, grid_positions)
    
    if correct_answer:
        sequence_length += 1
        screen.fill(WHITE)
        correct_text = TEXT_FONT.render("Correct! :)", True, BLACK)
        screen.blit(correct_text, correct_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        pygame.display.update()
        pygame.time.delay(2000)
    else:
        screen.fill(WHITE)
        incorrect_text = TEXT_FONT.render("Incorrect, game over:(", True, BLACK)
        screen.blit(incorrect_text, incorrect_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

end_screen()
