from dataclasses import dataclass, field;

@dataclass
class Card:
    __card_id:str;

    __face_id:str;
    __card_type: str;
    __img:str;

    __flipped: bool = field(init=False, default_factory=lambda:False);

    @property
    def card_type(self)->str:
        return self.__card_type;

    @property
    def face_id(self):
        return self.__face_id;

    @property
    def img(self)->str:
        return self.__img;

    def flip(self):
        self.__flipped = True;

    def unflip(self):
        self.__flipped = False;