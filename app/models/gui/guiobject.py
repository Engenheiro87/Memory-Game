from app.models.gui.color3 import Color3;
from dataclasses import dataclass, field;
from abc import ABC, abstractmethod;
import pygame;
import pygame_gui;

SCREEN_DIMENSIONS = (700, 500);

class UICoordinates:
    def __init__(self, x:int, y:int):
        self.__x = x;
        self.__y = y;
    
    @property
    def x(self)->int:
        return self.__x;

    @property
    def y(self)->int:
        return self.__y;

    def get_offset(self)->tuple[int, int]:
        return (self.__x, self.__y);

    def get_scale(self)->tuple[float, float]:
        return (
            self.__x/SCREEN_DIMENSIONS[0],
            self.__y/SCREEN_DIMENSIONS[1]
        );

    @staticmethod
    def from_scale(x_scale:float, y_scale:float)->UICoordinates:
        return UICoordinates(
            x_scale*SCREEN_DIMENSIONS[0],
            y_scale*SCREEN_DIMENSIONS[1]
        );


class GuiObject(ABC):
    def __init__(self, position:UICoordinates, size:UICoordinates, active=False):
        self.__position = position;
        self.__size = size;
        self.__active = active;
    
    @property
    def active(self):
        return self.__active;
    
    @property
    def position(self):
        return self.__position;

    @property
    def size(self):
        return self.__size;

    @property
    @abstractmethod
    def surface(self):
        pass;
    
    @property
    @abstractmethod
    def rect(self):
        pass;

    @abstractmethod
    def get_rect(self):
        pass;

    @abstractmethod
    def get_surface(self):
        pass;

class ImageLabel(GuiObject):
    def __init__(self, position, size, file_path:str):
        super().__init__(position, size, active=False);
        self.__file_path = file_path;
        self.__surface = self.get_surface();
        self.__rect = self.get_rect();
    
    @property
    def surface(self):
        return self.__surface;

    @property
    def rect(self):
        return self.__rect;
    
    def get_surface(self):
        surface = pygame.image.load(
            "app/static/img/"+self.__file_path,
        ).convert_alpha();
        return pygame.transform.scale(surface, self.size.get_offset());

    def get_rect(self):
        return self.__surface.get_rect(
            center=self.position.get_offset(),
            size=self.size.get_offset()
        );

    def set_transparency(self, transparency:float): # [0 is opaque] and [1 is transparent]
        self.surface.set_alpha(255-int(min(max(transparency, 0), 1)*255))
        return self;

class UIObject(ABC):
    def __init__(self, position:UICoordinates, size:UICoordinates, manager:pygame_gui.UIManager, name:str=None):
        self.__manager = manager;
        self.__rect = pygame.Rect(
            position.x - size.x/2,
            position.y-size.y/2,
            size.x,
            size.y
        );
        self.__name = name;
        self.__position = position;
        self.__size = size;
    
    @property
    def position(self):
        return self.__position;

    @property
    def size(self):
        return self.__size;

    @property
    def rect(self):
        return self.__rect;

    @property
    def name(self):
        return self.__name;

    @property
    def manager(self):
        return self.__manager;

    @abstractmethod
    def render_format(self):
        pass;


class UITextBox(UIObject):
    def __init__(self, position:UICoordinates, size:UICoordinates, manager:pygame_gui.UIManager, name:str=None):
        super().__init__(position, size, manager, name);
        self.__format = self.render_format();

    def render_format(self):
        return pygame_gui.elements.UITextEntryLine(
            relative_rect=self.rect,
            manager=self.manager,
            object_id=self.name
        );


class UILabel(UIObject):
    def __init__(self, position, size, text:str, manager:pygame_gui.UIManager, name = None):
        super().__init__(position, size, name);
        self.__text = text;
        self.__format = self.render_format();

    def render_format(self):
        return pygame_gui.elements.UILabel(
            relative_rect=self.rect,
            text = self.__text,
            manager = self.manager
        );

class UIImageLabel(UIObject):
    def __init__(self, position, size, manager, img_adress:str, name = None):
        super().__init__(position, size, manager, name)
        self.__img_adress = img_adress;

        self.__format = self.render_format();
    
    def get_surface(self):
        surface = pygame.image.load(
            "app/static/img/"+self.__img_adress
        ).convert_alpha();
        return pygame.transform.scale(surface, self.size.get_offset());


    def render_format(self):
        return pygame_gui.elements.UIImage(
            relative_rect=self.rect,
            image_surface=self.get_surface(),
            manager=self.manager,
            object_id=self.name
        );

class UIButton(UIObject):
    def __init__(self, position, size, manager, text:str="", img_adress:str=None, name = None):
        super().__init__(position, size, manager, name);
        self.__text = text;
        self.__img_adress = img_adress;
        self.__format = self.render_format();

    def render_format(self):
        button = pygame_gui.elements.UIButton(
            relative_rect=self.rect,
            text=self.__text,
            manager=self.manager,
            object_id=self.name,
        )
        if self.__img_adress:
            button.set_image(
                pygame.image.load("app/static/img/"+self.__img_adress)
                .convert_alpha()
            );