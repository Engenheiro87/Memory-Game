from dataclasses import dataclass, field;
from app.controllers.card_factory import CardFactory, Card;
from app.models.player import Player;
from app.models.board import Board;
from random import randint;
from threading import Thread;
from time import sleep;

@dataclass
class Match:
    __players:list[Player];
    __order:tuple[int, int];
    __dependencies:dict[str:callable];
    __mode:str = field(default_factory=lambda:"normal");

    __flipped_card:Card|None = field(repr=False, init=False, default_factory=lambda:None);
    __board:Board = field(repr=False, init=False, default_factory=lambda:None);
    __current_turn:int = field(repr=False, init=False, default_factory=lambda:0);
    __match_paused: bool = field(repr=False, init=False, default_factory=lambda: False);

    @property
    def flipped_card(self):
        return self.__flipped_card;

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

    def flip_card(self, card_id:str):
        card = self.__board.get_card(card_id);
        card_flip = self.__board.flip_card(card);
        if card_flip == False: # card was hidden
            self.__flipped_card = None;
        elif card_flip == True: # card was revealed.
            flipped = self.__flipped_card;
            if flipped:
                matched = self.parse_matching(card, flipped);
                self.__flipped_card = None;
            else:
                self.__flipped_card = card;
    #TODO: Test card flipping mechanics.
    
    def parse_matching(self, card:Card, flipped_card:Card)-> bool:
        if flipped_card: # there's a flipped card
            matched = False;
            if flipped_card.face_id == card.face_id: # they match
                self.__board.add_match(card, flipped_card);
                self.__board.unflip_all();
                self.apply_points();
                matched = True;
            else: # they don't match
                def unmatched():
                    self.set_paused(True);
                    sleep(1); # time for the player to see the cards.
                    self.__board.unflip_all();
                    self.set_paused(False);
                
                new_thread = Thread(target=unmatched);
                new_thread.start();
                matched = False;
            self.change_turns();
            print(f"Now it's {self.get_turn().username}'s turn.")
            return matched;

    def apply_points(self, Player:Player=None):
        if not Player:
            Player = self.get_turn();
        Player.increment_score(5);
    
    def set_paused(self, paused:bool):
        self.__match_paused = paused;

    def get_turn(self)->Player|None:
        return self.__players[self.__current_turn];

    def check_end(self)->bool:
        if len(self.__matched_cards)==len(self.__board.cards):
            print("All cards have been matched.");
            self.set_paused(True);
            return True;
        return False;

    def get_winner(self)->Player:
        sorted_players = sorted(
            self.__players,
            key=lambda player: player.match_score,
            reverse=True # forces descending order
        );
        return sorted_players[0];
