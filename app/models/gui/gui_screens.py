from abc import ABC, abstractmethod;
from app.models.gui.guiobject import *
import pygame_gui;

class GuiScreen(ABC):
    def __init__(self, dependencies:dict, manager:pygame_gui.UIManager):
        self.__dependencies = dependencies;
        self.__manager = manager;
        self.draw();

    @property
    def manager(self):
        return self.__manager;
    
    @abstractmethod
    def draw(self):
        pass;

    def add_object(self, object:UIObject):
        self.__dependencies["add_object"](object);

class MenuScreen(GuiScreen):
    def draw(self):
        self.add_object(
            UIImageLabel(
                UICoordinates.from_scale(.5, .35),
                UICoordinates(450,450),
                self.manager,
                "logo.png"
            )
        );
        
        self.add_object(
            UILabel(
                UICoordinates.from_scale(.5, .8),
                UICoordinates.from_scale(.4, .05),
                "<- INSERT PLAYER NAMES TO START ->",
                self.manager,
            )
        )

        # player boxes
        self.add_object(
            UITextBox(
                UICoordinates.from_scale(.25, .9),
                UICoordinates.from_scale(.25, .1),
                self.manager,
                "#playerbox1"
            )
        );

        self.add_object(
            UITextBox(
                UICoordinates.from_scale(.75, .9),
                UICoordinates.from_scale(.25, .1),
                self.manager,
                "#playerbox2"
            )
        );
    
        self.add_object(
            UIButton(
                UICoordinates.from_scale(.5, .65),
                UICoordinates.from_scale(.1, .1),
                self.manager,
                "START",
                name="#start"
            )
        );

class GameScreen(GuiScreen):
    def __init__(self, dependencies, manager, player_names):
        self.__player_names = player_names;
        self.__cards = {};
        super().__init__(dependencies, manager);

    def draw(self):
        # player names:
        self.add_object(
            UILabel(
                UICoordinates.from_scale(.2, .9),
                UICoordinates.from_scale(.2, .1),
                self.__player_names[0],
                self.manager
            )
        );
        self.add_object(
            UILabel(
                UICoordinates.from_scale(.8, .9),
                UICoordinates.from_scale(.2, .1),
                self.__player_names[1],
                self.manager
            )
        );

    def add_card(self, card_id:str, face_id:str):
        self.__cards[card_id] = UIButton(
            UICoordinates.from_scale(.5,.5),
            UICoordinates.from_scale(50,50),
            self.manager,
            text = face_id
            # img_adress="card.png"
        )