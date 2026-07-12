from dataclasses import dataclass, field;
from app.models.card import Card;

@dataclass
class Board:
    __cards:dict[Card];
    __order:tuple[int, int]
    __uncovered_card:Card|None = field(init=False, default_factory=lambda:None);

    @property
    def cards(self)->dict[Card]:
        return self.__cards;
    
    def shuffle_cards(self):
        pass;

    def get_card(self, card_id:str)->Card|None:
        return self.__cards.get(card_id);