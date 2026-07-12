from dataclasses import dataclass, field;
from uuid import uuid4;

@dataclass
class Player:
    __user_id:str;
    __username: str = field(default_factory=lambda: f"Guest_{str(uuid4())}");
    __total_score: int = field(default_factory=lambda:0);
    __score: int = field(init=False, default_factory=lambda:0);

    @property
    def username(self)->str:
        return self.__username;

    @property
    def user_id(self)->str:
        return self.__user_id;

    def increment_score(self, increment:int):
        self.__score+=int(increment);

    def pack(self)->dict:
        return {
            "username": self.__username,
            "total_score":self.__total_score
        };

    def __str__(self)->str:
        return self.__username;
