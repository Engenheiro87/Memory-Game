from app.models.gui.color3 import Color3;
from abc import ABC, abstractmethod;
import pygame;

SCREEN_DIMENSIONS = (700, 500);

class UICoordinates:
    def __init__(self, x:int, y:int):
        self.__x = x;
        self.__y = y;

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
    def __init__(self, position:UICoordinates, size:UICoordinates):
        self.__position = position;
        self.__size = size;
    
    @property
    def position(self):
        return self.__position;

    @property
    def size(self):
        return self.__size;

    @property
    def surface(self):
        pass;
    
    @property
    def rect(self):
        pass;

    @abstractmethod
    def get_rect(self):
        pass;

    @abstractmethod
    def get_surface(self):
        pass;

class TextLabel(GuiObject):
    def __init__(self, position:UICoordinates, size:UICoordinates, text:str, text_color:Color3, font:pygame.Font, scaled:bool=False):
        super().__init__(position, size);
        self.__text = text;
        self.__text_color = text_color;
        self.__font = font;
        self.__scaled = scaled;
        self.__surface = self.get_surface();
        self.__rectangle = self.get_rect();
        self.__rectangle.center = self.position.get_offset();

    @property
    def surface(self):
        return self.__surface;

    @property
    def rect(self):
        return self.__rectangle;

    def get_rect(self):
        return self.__surface.get_rect();

    def get_surface(self):
        surface = self.__font.render(
            self.__text,
            True,
            self.__text_color.get_rgb(),
        ).convert_alpha();
        if not self.__scaled:
            return surface;
        return pygame.transform.scale(
            surface,
            self.size.get_offset()
        );

class ImageLabel(GuiObject):
    def __init__(self, position, size, file_path:str):
        super().__init__(position, size);
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