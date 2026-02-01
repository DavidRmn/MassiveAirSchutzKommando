import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, width: int, height: int,
                  text: str, text_color: str, text_font: str, text_size: int, text_length: float,
                  button_color: str, hover_color: str, click_color: str, accent_color: str,
                  outline_width: int, click_sound: str = None, release_sound: str = None, hover_sound: str = None, 
                  click_volume: float = 0.5, release_volume: float = 0.5, hover_volume: float = 0.5,
                  click_cooldown: int = 150):
        super().__init__()
        self.width = width
        self.height = height
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.accent_color = accent_color
        self.outline_width = outline_width
        
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect(center = (x, y))

        font = pygame.font.Font(text_font, text_size)
        self.text = font.render(text, antialias=False, color=text_color, wraplength=int(width * text_length))
        self.text_rect = self.text.get_rect(center=(width // 2, height // 2))

        # States
        self.is_pressed = False
        self.was_released = False
        self.action_ready = False 
        self.was_hovering = False
        self.suppress_hover_sound = False
        
        # Timing
        self.click_cooldown = click_cooldown
        self.last_pressed = 0

        # Audio
        self.click_sound = None
        self.hover_sound = None
        self.release_sound = None

        if click_sound: 
            self.click_sound = pygame.Sound(click_sound)
            self.click_sound.set_volume(click_volume)

        if release_sound: 
            self.release_sound = pygame.Sound(release_sound)
            self.release_sound.set_volume(release_volume)

        if hover_sound: 
            self.hover_sound = pygame.Sound(hover_sound)
            self.hover_sound.set_volume(hover_volume)

        self.__draw_button(button_color)

    def __draw_button(self, color):
        self.image.fill(self.accent_color)
        button_surf = pygame.Surface([self.width - self.outline_width * 2, self.height - self.outline_width * 2])
        button_surf.fill(color)
        self.image.blit(button_surf, (self.outline_width, self.outline_width))
        self.image.blit(self.text, self.text_rect)

    def __get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def __get_mouse_pressed(self):
        return pygame.mouse.get_just_pressed()[0]
    
    def __get_mouse_released(self):
        return pygame.mouse.get_just_released()[0]
    
    def __check_for_hover(self):
        return self.rect.collidepoint(self.__get_mouse_pos())
    
    def update(self):
        current_time = pygame.time.get_ticks()
        is_hovering = self.__check_for_hover()
        mouse_pressed = self.__get_mouse_pressed()
        mouse_released = self.__get_mouse_released()
        
        if is_hovering and mouse_pressed:
            self.is_pressed = True
            self.was_released = False
            self.action_ready = False
            self.suppress_hover_sound = True
            self.last_pressed = current_time
            self.__draw_button(self.click_color)
            if self.click_sound is not None:
                self.click_sound.play()
        
        elif is_hovering:
            if self.is_pressed and mouse_released and not self.was_released:
                self.was_released = True
                self.last_pressed = current_time
                if self.release_sound is not None:
                    self.release_sound.play()

            if self.is_pressed and self.was_released and current_time - self.last_pressed < self.click_cooldown:
                self.__draw_button(self.click_color)

            elif self.is_pressed and self.was_released:
                self.action_ready = True
                self.is_pressed = False
                self.was_released = False
                self.__draw_button(self.hover_color)
            
            elif self.is_pressed:
                self.__draw_button(self.click_color)
            
            else:
                self.__draw_button(self.hover_color)
                if self.hover_sound is not None and not self.was_hovering and not self.suppress_hover_sound:
                    self.hover_sound.play()
        
        else:
            if self.is_pressed and mouse_released:
                if self.release_sound is not None:
                    self.release_sound.play()
            
            self.is_pressed = False
            self.was_released = False
            self.action_ready = False
            self.suppress_hover_sound = False
            self.__draw_button(self.button_color)
        
        self.was_hovering = is_hovering

    def reset(self):
        """Reset button state"""
        self.is_pressed = False
        self.was_released = False
        self.action_ready = False
        self.was_hovering = False
        self.suppress_hover_sound = False
        self.last_pressed = 0
        self.__draw_button(self.button_color)