import pygame

pygame.init()
font = pygame.font.SysFont('Arial', 20)

def debug(message: str, pos_x: int = 0, pos_y: int = 0) -> None:
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(message, True, 'White', 'Black')
    debug_rect = debug_surf.get_rect(topleft=(pos_x, pos_y))
    display_surf.blit(debug_surf, debug_rect)
