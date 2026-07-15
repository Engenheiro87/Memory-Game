from app.controllers.data_record import DynamicData, StaticData;
from app.controllers.pygame_gui import PygameGUI;
from app.models.player import Player;
from app.controllers.match import Match;
from uuid import uuid4;
import pygame;
import pygame_gui;

class Game:
    WINDOW_DIMENSIONS = (700,500);
    FPS_TARGET = 30;
    def __init__(self):

        # Pygame initiation
        pygame.init();
        self.__window = pygame.display.set_mode(Game.WINDOW_DIMENSIONS);
        pygame.display.set_caption("Memory Code");
        self.__clock = pygame.time.Clock();
        self.__manager = pygame_gui.UIManager(Game.WINDOW_DIMENSIONS);

        # attributes
        self.__players = {};
        self.__data = {
            "user_data":DynamicData("dynamic/user_data.json", self.pack_players),
            "card_data":StaticData("static/card_data.json")
        };
        self.__screen_gui = PygameGUI(
            self.__window, 
            Game.WINDOW_DIMENSIONS,
            self.__manager
        );
        self.__current_match = None;
        self.__match_dependencies = {
            "get_card_data":self.get_card_data
        };
        self.__game_state = "N/A";
        self.__logged_players = {};
        self.__running = True;

        self.load_players();
        self.run();

    # temporary property

    @property
    def match(self):
        return self.__current_match;

    @property
    def players(self):
        return self.__players;

    def run(self):
        self.__screen_gui.load_screen("menu");
        while self.__running:

            UI_REFRESH_RATE = self.__clock.tick(Game.FPS_TARGET)/1000;

            self.process_events();

            self.__manager.update(UI_REFRESH_RATE);

            self.__screen_gui.draw_screen();

        
        print("pygame quit running.");
        pygame.quit();

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
        names = [player.username for player in players];
        ui_dependencies = self.__screen_gui.load_screen(
            "game",
            names
        );
        ui_dependencies["add_card"]("card_id", "idk");
        match = Match(
            [*players],
            (2, 3),
            self.__match_dependencies
        ).start();
        self.__current_match = match;
        return match;
    
    def get_data(self, data_name:str)->StaticData|DynamicData|None:
        return self.__data.get(data_name);

    def process_events(self):
        for event in pygame.event.get():
            event_type = event.type;
            match event_type:
                case pygame.QUIT:
                    self.__running = False;
                    break;
                case pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    object_id = event.ui_object_id;
                    if "#playerbox" in object_id:
                        self.log_player(
                            int(object_id[10:]),
                            event.text
                        );
                case pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "#start":
                        players = self.get_logged_players();
                        if players:
                            self.start_match(*players) 

            self.__manager.process_events(event);
    
    def get_logged_players(self)->tuple[Player]|False:
        parsed_players = [];
        for player_number, player_name in self.__logged_players.items():
            if player_name.strip()=="":
                return False;
            player = self.get_player_by_name(player_name);
            if not player:
                self.register_player(player_name);
                return self.get_logged_players();
            if player in parsed_players:
                return False;
            parsed_players.append(player);
        return parsed_players;

    def log_player(self, player_number:int, player_name:str):
        self.__logged_players[player_number] = player_name;
    
    def save(self):
        for data in self.__data.values():
            if type(data) == DynamicData:
                data.save();

    def get_leaderboard(self)->dict:
        user_list = [
            {
                "total_score":player.total_score,
                "username":player.username,
            }
            for player_id, player in self.__players.items()
        ]
        return sorted(user_list, key=lambda user:user.get("total_score", 0), reverse=True);

    def register_player(self, username:str)->tuple[bool, str|Player]:
        existing = self.get_player_by_name(username);
        if existing:
            return False, "Player already exists.";
        new_id = str(uuid4());
        new_player = Player(
            new_id,
            username
        );
        self.__players[new_id] = new_player

        self.get_data("user_data").save();

        return True, new_player;

    def menu(self):
        pass;

    def pack_players(self)->dict:
        return {
            user_id:player.pack()
            for user_id, player in self.__players.items()
        };
        
    def get_card_data(self)->StaticData:
        return self.get_data("card_data");
