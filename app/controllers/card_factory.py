from app.models.card import Card;
from random import randint;
from uuid import uuid4;

class CardFactory:
    def __init__(self, total_cards:int, card_list:list[str]):
        self.__card_list = card_list;
        self.__cards = {};
        self.raffle(total_cards);
    
    def get(self)->dict[Card]:
        return self.__cards;

    def raffle(self, total_cards:int):
        languages_needed = total_cards//2;
        print(f"languages needed for total cards = {total_cards} is {languages_needed}");
        for i in range(languages_needed):
            language_picked = self.__card_list.pop(
                randint(0, len(self.__card_list)-1)
            );
            for card_type in ["code", "logo"]:
                new_id = str(uuid4())
                self.__cards[new_id] = Card(
                        new_id,
                        language_picked,
                        card_type,
                        language_picked+"_"+card_type
                    )
                
