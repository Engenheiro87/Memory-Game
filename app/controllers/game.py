from app.controllers.data_record import DynamicData, StaticData;
from app.controllers.pygame_gui import PygameGUI;
from app.models.player import Player;
from app.controllers.match import Match;
from uuid import uuid4;
import pygame;

class Game:
    WINDOW_DIMENSIONS = (700,500);
    FPS_TARGET = 30;
    def __init__(self):

        # Pygame initiation
        # pygame.init();
        # self.__window = pygame.display.set_mode(Game.WINDOW_DIMENSIONS);
        # pygame.display.set_caption("Memory Code");
        # self.__clock = pygame.time.Clock();

        # attributes
        self.__players = {};
        self.__data = {
            "user_data":DynamicData("dynamic/user_data.json", self.pack_players),
            "card_data":StaticData("static/card_data.json")
        };
        # self.__screen_gui = PygameGUI(self.__window);
        self.__current_match = None;
        self.__match_dependencies = {
            "get_card_data":self.get_card_data
        };
        self.__game_state = "N/A";
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
        while self.__running:
            print(f"""
Jogo da Memória:
1 - Jogar
2 - Pódio
3 - Sair.
""");
            action1 = int(input("Digite um número: "));
            if action1 == 3:
                # print("Salvando e saindo...");
                # self.save();
                print("Saindo...");
                break;
            match action1:
                case 2:
                    leaderboard = self.get_leaderboard();
                    print("\nLEADERBOARD:");
                    for index, player_data in enumerate(leaderboard, start=1):
                        print("------------------------------------------");
                        print(f"{index}. {player_data.get("username", "???")} -- {player_data.get("total_score", "unknown")}");
                case 1:
                    players = [];

                    for i in range(2):
                        while True:
                            name = input(f"Nome jogador {i+1}: ");
                            player = self.get_player_by_name(name);
                            if not player:
                                print("\nJogador não registrado no sistema. Criando novo jogador...");
                                while True:
                                    sucess, player_error = self.register_player(name);
                                    if not sucess or type(player_error)!=Player:
                                        print("Erro:", player_error);
                                        continue;
                                    print("Sucesso.");
                                    player = player_error;
                                    break;
                            elif player in players:
                                print(f"Jogador \"{player.username}\" já logado. Por favor tente outro.");
                                continue;
                            print(f"Jogador \"{player.username}\" logado.");
                            players.append(player);
                            break;
                    print("Jogadores logados:");
                    player:Player
                    for player in players:
                        print(player.username);
    
                    self.start_match(*players);
                    self.menu_match();
                    self.__current_match = None;
        # self.__screen_gui.load_menu();
        # while self.__running:
        #     self.process_events();
        #     self.__screen_gui.draw_screen();
        #     self.__clock.tick(Game.FPS_TARGET);
        
        # print("pygame quit running.");
        # pygame.quit();

    def menu_match(self):
        current_match = self.__current_match;
        while not current_match.check_end():
            action = input("Next action | ");
            if action == "points":
                print("POINTS:");
                for player in current_match.players:
                    print(f"{player.username} .. {player.match_score}");
            elif action == "cards":
                for card_id, card in current_match.board.cards.items():
                    print(f"{card_id} = {card.img} FLIPPED = {card.flipped}");
            elif action == "flip":
                card_id = input("Cole o ID da carta: ");
                result = current_match.flip_card(card_id);
                while not result:
                    card_id = input("Não deu certo. Cole outro ID: ");
                    result = current_match.flip_card(card_id);
                print("Sucesso.");
        winner = current_match.get_winner();
        for player in current_match.players:
            if player == winner:
                player.increment_score(player.match_score);
            player.match_score = 0;
        print(f"\nA partida acabou. Vencedor: {winner}")

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
            (2, 3),
            self.__match_dependencies
        ).start();
        self.__current_match = match;
        return match;
    
    def get_data(self, data_name:str)->StaticData|DynamicData|None:
        return self.__data.get(data_name);

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False;
                break;
    
    def save(self):
        return;
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
        # return self.get_data("user_data").get_sorted();

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
