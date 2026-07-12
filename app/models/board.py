from dataclasses import dataclass, field;
from app.models.card import Card;

@dataclass
class Board:
    __cards:dict[Card];
    __order:tuple[int, int]
    __uncovered_card:Card|None = field(init=False, default_factory=lambda:None);
    __matched_cards:list[Card] = field(init=False, repr=False, default_factory=list);

    @property
    def cards(self)->dict[Card]:
        return self.__cards;
    
    def shuffle_cards(self):
        pass;

    def get_card(self, card_id:str)->Card|None:
        return self.__cards.get(card_id);

    def flip_card(self, card:Card)->bool|None:
        if not card or card in self.__matched_cards:
            return;
    
        card.flip() if not card.flipped else card.unflip();

        return card.flipped;

    def unflip_all(self, filter:list[Card]=[]):            
        for card in self.__cards.values():
            if card in filter or card in self.__matched_cards:
                continue;
            card.unflip();

    def add_match(self, *cards):
        for card in cards:
            if not card in self.__matched_cards:
                self.__matched_cards.append(card);
