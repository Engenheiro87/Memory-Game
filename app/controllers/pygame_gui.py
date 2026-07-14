from app.models.gui.color3 import Color3;
from app.models.gui.guiobject import UICoordinates, GuiObject, TextLabel, ImageLabel, InputBox;
from uuid import uuid4;
import pygame

class PygameGUI:
    def __init__(self, window, ):
        self.__window = window;

        self.__screen = {};
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

    def draw_screen(self):
        self.fill_background(
            Color3(88, 48, 112)
        );

        guiobject:GuiObject
        for guiobject in self.__screen.values():
            self.__window.blit(
                guiobject.surface,
                guiobject.rect
            );

        pygame.display.flip();

    def load_menu(self):
        self.clear_screen();

        # background image:
        self.add_object(
            ImageLabel(
                UICoordinates.from_scale(.5,.5),
                UICoordinates.from_scale(1,1),
                "sunburst.png"
            ).set_transparency(.8),
            "background_image"
        );

        # title
        h1 = self.__fonts['h1'];
        h2 = self.__fonts['h2'];
        h5 = self.__fonts['h5'];

        self.add_object(
            ImageLabel(
                UICoordinates.from_scale(.5, .5),
                UICoordinates(450,450),
                "logo.png"
            ).set_transparency(0),
            "menu_logo"
        );

        self.add_object(
            TextLabel(
                UICoordinates.from_scale(.5, .8),
                UICoordinates.from_scale(.4, .05),
                "<- INSERT PLAYER NAMES TO START ->",
                Color3.from_name("white"),
                h5,
                scaled=False
            ),
            "hint"
        );

        # player 1 name
        self.add_object(
            InputBox(
                UICoordinates.from_scale(.25, .9),
                UICoordinates.from_scale(.25, .1),
                Color3.from_name("white"),
                h5,
                "Your name here.",
                scaled=False
            )
        );

    def add_object(self, object:GuiObject, id:str=lambda: str(uuid4())):
        self.__screen[id] = object;
        return id;
    
    def fill_background(self, color:Color3):
        self.__window.fill(color.get_rgb());

    def clear_screen(self):
        self.__screen = {};