import pygame

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQ_SIZE = WIDTH // COLS
COLORS = [pygame.Color("white"), pygame.Color("gray")]

def draw_board(screen):
    for r in range(ROWS):
        for c in range(COLS):
            color = COLORS[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess GUI")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() # (x, y)
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                print(f"Clicked on square: {row}, {col}")
        
        draw_board(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
