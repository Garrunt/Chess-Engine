import pygame
import chess

# Constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQ_SIZE = WIDTH // COLS

# Unicode mapping for chess pieces
UNICODE_PIECES = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
}

def get_square_from_mouse(pos):
    """Converts pixel coordinates to a chess square (e.g., 'e2')"""
    col = pos[0] // SQ_SIZE
    row = 7 - (pos[1] // SQ_SIZE)
    return chess.square(col, row)

def draw_board(screen):
    """Draws the 8x8 checkerboard."""
    for r in range(ROWS):
        for c in range(COLS):
            color = pygame.Color("#eeeed2") if (r + c) % 2 == 0 else pygame.Color("#769656")
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, (7 - r) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board, font):
    """Draws the Unicode pieces onto the board."""
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            symbol = UNICODE_PIECES[piece.symbol()]
            # Set color based on piece team
            text_color = pygame.Color("white") if piece.color == chess.WHITE else pygame.Color("black")
            text = font.render(symbol, True, text_color)
            
            # Center text in square
            col = chess.square_file(square)
            row = chess.square_rank(square)
            screen.blit(text, (col * SQ_SIZE + 10, (7 - row) * SQ_SIZE - 5))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess GUI with Logic")
    font = pygame.font.SysFont("Arial", 75)
    
    board = chess.Board()
    running = True
    selected_square = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                sq = get_square_from_mouse(pos)
                
                if selected_square is None:
                    # Select a piece
                    if board.piece_at(sq):
                        selected_square = sq
                else:
                    # Attempt to move
                    move = chess.Move(selected_square, sq)
                    if move in board.legal_moves:
                        board.push(move)
                    # Reset selection
                    selected_square = None

        screen.fill(pygame.Color("white"))
        draw_board(screen)
        draw_pieces(screen, board, font)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()