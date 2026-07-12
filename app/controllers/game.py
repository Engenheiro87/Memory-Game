from app.controllers.data_record import DynamicData, StaticData;
from app.models.player import Player;
from app.controllers.match import Match;
from uuid import uuid4;
import pygame;

class Game:
    WINDOW_DIMENSIONS = (800,800);
    def __init__(self):

        # Pygame initiation
        pygame.init();
        self.__window = pygame.display.set_mode(Game.WINDOW_DIMENSIONS);
        pygame.display.set_caption("Memory Code");
        self.__clock = pygame.time.Clock();

        # attributes
        self.__players = {};
        self.__data = {
            "user_data":DynamicData("dynamic/user_data.json", self.pack_players),
            "card_data":StaticData("static/card_data.json")
        };
        self.__screen_gui = None;
        self.__current_match = None;
        self.__match_dependencies = {
            "get_card_data":self.get_card_data
        };
        self.__game_state = "N/A";

        self.load_players();

    # temporary property

    @property
    def match(self):
        return self.__current_match;

    @property
    def players(self):
        return self.__players;
    
    def load_players(self):
        self.__players = {
            user_id: Player(
                user_id,
                data['username'],
                data['total_score']
            )
            for user_id, data in self.__data['user_data']
            .read_data(default={})
            .items()
        };

    def get_player_from_id(self, id:str)->Player|None:
        return self.__players.get(id);

    def get_player_by_name(self, username:str)->Player|None:
        for player in self.__players.values():
            if player.username == username:
                return player;

    def start_match(self, *players):
        if self.__current_match:
            return;
        match = Match(
            [*players],
            (2, 4),
            self.__match_dependencies
        ).start();
        self.__current_match = match;
        return match;
    
    def get_data(self, data_name:str)->StaticData|DynamicData|None:
        return self.__data.get(data_name);

    def process_events(self):
        pass;
    
    def save(self):
        for data in self.__data.values():
            if type(data) == DynamicData:
                data.save();

    def get_leaderboard(self)->dict:
        return self.get_data("user_data").get_sorted();

    def register_player(self, username:str)->tuple[bool, str|Player]:
        existing = self.get_player_by_name(username);
        if existing:
            return False, "Player already exists.";
        new_id = str(uuid4());
        self.__players[new_id] = Player(
            new_id,
            username
        );
        self.get_data("user_data").save();

    def menu(self):
        pass;

    def pack_players(self)->dict:
        return {
            user_id:player.pack()
            for user_id, player in self.__players.items()
        };
        
    def get_card_data(self)->StaticData:
        return self.get_data("card_data");
