from dataclasses import dataclass, field;
from app.controllers.card_factory import CardFactory, Card;
from app.models.player import Player;
from app.models.board import Board;
from random import randint;

@dataclass
class Match:
    __players:list[Player];
    __order:tuple[int, int];
    __dependencies:dict[str:callable];
    __mode:str = field(default_factory=lambda:"normal");

    __uncovered_card:Card|None = field(init=False, default_factory=lambda:None);
    __board:Board = field(init=False, default_factory=lambda:None);
    __current_turn:int = field(init=False, default_factory=lambda:0);

    @property
    def board(self):
        return self.__board;

    def load(self):
        card_data = self.__dependencies["get_card_data"]().read_data(self.__mode);
        self.__board = Board(
            CardFactory(
                self.__order[0]*self.__order[1],
                card_data
            ).get(),
            self.__order
        );

    def start(self):
        self.load();
        return self;
    
    def change_turns(self):
        current = self.__current_turn;
        if current+1>=len(self.__players):
            self.__current_turn = 0;
            return;
        self.__current_turn +=1;

    def uncover_card(self, card_id:str):
        pass;

    def get_turn(self)->Player|None:
        return self.__players[self.__current_turn];
