# A class created for all buttons in the program
class Button():
    def __init__(self, BG_IMAGE, POSITION, BUTTON_TEXT, FONT, BASE_COLOR, HOVER_COLOR):
        self.BG_IMAGE = BG_IMAGE
        self.X_POSITION = POSITION[0]
        self.Y_POSITION = POSITION[1]
        self.FONT = FONT
        self.BASE_COLOR, self.HOVER_COLOR = BASE_COLOR, HOVER_COLOR
        self.BUTTON_TEXT = BUTTON_TEXT
        self.TEXT = self.FONT.render(self.BUTTON_TEXT, True, self.BASE_COLOR)
        if self.BG_IMAGE is None:
            self.BG_IMAGE = self.TEXT
        self.RECT = self.BG_IMAGE.get_rect(center=(self.X_POSITION, self.Y_POSITION))
        self.TEXT_RECT = self.TEXT.get_rect(center=(self.X_POSITION, self.Y_POSITION))

    def update(self, screen):
        if self.BG_IMAGE is not None:
            screen.blit(self.BG_IMAGE, self.RECT)
        screen.blit(self.TEXT, self.TEXT_RECT)

    def checkForInput(self, position):
        if position[0] in range(self.RECT.left, self.RECT.right) and position[1] in range(self.RECT.top, self.RECT.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.RECT.left, self.RECT.right) and position[1] in range(self.RECT.top, self.RECT.bottom):
            self.TEXT = self.FONT.render(self.BUTTON_TEXT, True, self.HOVER_COLOR)
        else:
            self.TEXT = self.FONT.render(self.BUTTON_TEXT, True, self.BASE_COLOR)