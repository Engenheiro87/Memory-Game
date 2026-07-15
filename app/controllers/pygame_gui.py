from app.models.gui.color3 import Color3;
from app.models.gui.guiobject import UICoordinates, UIObject, UITextBox, UILabel, UIImageLabel, UIButton;
from uuid import uuid4;
import app.models.gui.gui_screens as GUI;
import pygame
import pygame_gui;

class PygameGUI:
    def __init__(self, window, dimensions:tuple[int, int], gui_manager:pygame_gui.UIManager):
        self.__window = window;

        self.__manager = gui_manager;

        self.__focused_input = None;
        self.__fonts = {
            "h1":pygame.font.Font(
                None,
                90
            ),
            "h2":pygame.font.Font(
                None,
                60
            ),
            "h5":pygame.font.Font(
                None,
                25
            )
        };
        self.routes = {
            "menu":self.load_menu,
            "game":self.load_game
        };
        self.__screen_dependencies = {
            "add_object":self.add_object
        };
    
    def draw_screen(self):
        self.fill_background(
            Color3(88, 48, 112)
        );


        self.__manager.draw_ui(self.__window);
        
        pygame.display.flip();
    
    def load_screen(self, screen_name:str, *args):
        self.clear_screen();
        screen_route = self.routes.get(screen_name);
        if not screen_route:
            return;
        if args:
            return screen_route(*args);
        else:
            return screen_route();
    
    def load_menu(self):
        GUI.MenuScreen(
            self.__screen_dependencies,
            self.__manager
        );

    def load_game(self, player_names:tuple[str]):
        screen = GUI.GameScreen(
            self.__screen_dependencies,
            self.__manager,
            player_names
        );
        return {
            "add_card":screen.add_card
        }

    def add_object(self, object:UIObject, id:str=lambda: str(uuid4())):
        self.__screen[id] = object;
        return id;
    
    def fill_background(self, color:Color3):
        self.__window.fill(color.get_rgb());

    def clear_screen(self):
        self.__screen = {};
        self.__manager.clear_and_reset();