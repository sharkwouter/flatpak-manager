import pygame
import pygameMenu
import flatpakmanager_steamos
import pyflatpak


class gui():

    def __init__(self, window_width, window_height, title):
        self.window_width = window_width
        self.window_height = window_height
        self.title = title

        self.framerate = 30
        self.running = False
        self.menu_available_page = 1
        self.menu_installed_page = 1

        self.__init_pygame()
        self.__init_joysticks()
        self.__flatpak_manager = pyflatpak.manager()
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
        self.menu_available = self.__generate_available_application_menu()

        #self.menu_installed = self.__generate_installed_application_menu()

        self.menu_main = self._create_menu(self.title)

        self.menu_main.add_option("Available Software", self.menu_available)
        #self.menu_main.add_option("Installed Software", self.menu_installed)
        self.menu_main.add_option("Exit", pygameMenu.events.EXIT)

    def __draw_background(self):
        self.window.fill(flatpakmanager_steamos.color.background)

    def __draw_splash_screen(self):
        self.__draw_background()

        # draw logo
        logo = pygame.image.load(flatpakmanager_steamos.config.logo)
        logo_x = self.window_width / 2 - logo.get_width() / 2
        logo_rect = pygame.Rect(logo_x, 0, logo.get_width(), logo.get_height())
        self.window.blit(logo, logo_rect)

        # draw title
        font = pygame.font.Font(flatpakmanager_steamos.config.font, 64)
        text = font.render(self.title, False, flatpakmanager_steamos.color.text_title)
        text_rectangle = text.get_rect()
        text_rectangle.center = (self.window_width / 2, self.window_height - 64)
        self.window.blit(text, text_rectangle)

        pygame.display.update()

    def __draw_load_screen(self, title):
        self.__draw_background()

        # draw title
        font = pygame.font.Font(flatpakmanager_steamos.config.font, 64)
        text = font.render(title, False, flatpakmanager_steamos.color.text_title)
        text_rectangle = text.get_rect()
        text_rectangle.center = (self.window_width / 2, self.window_height / 2)
        self.window.blit(text, text_rectangle)

        pygame.display.update()

    def __generate_available_application_menu(self, label=None, page=None):
        application_list = self.__flatpak_manager.applications_available

        # Create menu
        menu = self._create_menu("Available applications")

        # Change the page and make sure we're on an existing page
        if page > 1:
            print(page)
            self.menu_available_page = page

        # add page changer
        page_list = []
        last_page = len(application_list) / flatpakmanager_steamos.config.applications_per_page + 1
        for number in range(1, last_page + 1):
            page_list.append(("Page {}/{}".format(number, last_page), number))
        menu.add_selector("", page_list, onchange=self.__generate_available_application_menu,
                          selector_id='page_selector{}'.format(self.menu_available_page))

        # add application buttons to menu
        page_content = self.__get_page(application_list, self.menu_available_page)
        for application in page_content:
            menu.add_option(str(application), pygameMenu.events.BACK)

        return menu

    def _create_menu(self, title):
        return pygameMenu.Menu(self.window, self.window_width, self.window_height,
                               flatpakmanager_steamos.config.font, self.title,
                               dopause=False,
                               menu_width=self.window_width,
                               menu_height=self.window_height,
                               menu_color=flatpakmanager_steamos.color.background,
                               menu_color_title=flatpakmanager_steamos.color.title,
                               color_selected=flatpakmanager_steamos.color.selected,
                               menu_alpha=100
                               )

    def __get_page(self, application_list, page):
        output = []

        first_index = flatpakmanager_steamos.config.applications_per_page * (page - 1)
        last_index = first_index + flatpakmanager_steamos.config.applications_per_page

        for index in range(first_index, last_index):
            if not index < len(application_list):
                break
            output.append(application_list[index])

        print(output)
        return output

    def __read_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(flatpakmanager_steamos.config.framerate)
            self.menu_main.mainloop()
            pygame.display.update()

    def stop(self):
        self.running = False
