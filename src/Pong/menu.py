import pygame

class Menu:
    def __init__(self):
        self.menu_items = ["One Player", "Settings", "Quit"]
        self.selected_item = 0
        self.screen = pygame.display.get_surface()
        self.w, self.h = self.screen.get_size()

    def draw(self):
        font = pygame.font.Font(None, 36)
        for index, item in enumerate(self.menu_items):
            if index == self.selected_item:
                text = font.render("-> " + item, True, (255, 255, 255))
            else:
                text = font.render(item, True, (255, 255, 255))
            self.screen.blit(text, (self.w // 2 - text.get_width() // 2, 200 + index * 50))

    def handle_input(self, event):
        if event.type == KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                return self.selected_item
        return None