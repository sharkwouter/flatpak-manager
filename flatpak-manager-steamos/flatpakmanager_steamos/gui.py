import pygame
import pygameMenu
import flatpakmanager_steamos


class gui():

    def __init__(self, window_width, window_height, title):
        self.window_width = window_width
        self.window_height = window_height
        self.title = title

        self.framerate = 30
        self.running = False

        self.__init_pygame()
        self.__init_joysticks()
        self.__init_menu()

    def __init_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.__draw_splash_screen()

    def __init_joysticks(self):
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in joysticks:
            joystick.init()

    def __init_menu(self):
        self.menu_main = pygameMenu.TextMenu(self.window, self.window_width, self.window_height, flatpakmanager_steamos.config.font, self.title,
            bgfun=self.__draw_background)

        self.menu_main.add_option("Available Software", self.menu_main)
        self.menu_main.add_option("Installed Software", self.menu_main)
        self.menu_main.add_option("Exit", pygameMenu.events.EXIT)

    def __draw_background(self):
        self.window.fill(flatpakmanager_steamos.color.background)

    def __draw_splash_screen(self):
        self.__draw_background()

        # draw logo
        logo = pygame.image.load(flatpakmanager_steamos.config.logo)
        logo_x = self.window_width/2-logo.get_width()/2
        logo_rect = pygame.Rect(logo_x, 0, logo.get_width(), logo.get_height())
        self.window.blit(logo, logo_rect)

        # draw title
        font = pygame.font.Font(flatpakmanager_steamos.config.font, 64)
        text = font.render(self.title, False, flatpakmanager_steamos.color.text_title)
        text_rectangle = text.get_rect()
        text_rectangle.center = (self.window_width/2, self.window_height-64)
        self.window.blit(text, text_rectangle)

        pygame.display.update()

    def __read_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(flatpakmanager_steamos.config.framerate)
            self.menu_main.mainloop(disable_loop=True)
            pygame.display.update()

    def stop(self):
        self.running = False
